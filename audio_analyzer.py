import sys
import os
import stat
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, 
    QFileDialog, QMessageBox, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QPalette, QColor, QFontDatabase, QIcon
from pydub import AudioSegment
import pyloudnorm as pyln
import numpy as np

class AudioAnalyzerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Función para obtener la ruta absoluta del recurso
        def resource_path(relative_path):
            """Return the absolute path of the resource, used with PyInstaller."""
            try:
                base_path = sys._MEIPASS
            except AttributeError:
                base_path = os.path.abspath(".")
            return os.path.join(base_path, relative_path)

        # Función para asegurar permisos de ejecución
        def ensure_ffmpeg_executable(ffmpeg_path):
            if os.path.exists(ffmpeg_path):
                st = os.stat(ffmpeg_path)
                os.chmod(ffmpeg_path, st.st_mode | stat.S_IEXEC)
                return True
            return False

        # Configurar FFmpeg inicial
        ffmpeg_binary = 'ffmpeg.exe' if sys.platform.startswith('win') else 'ffmpeg'
        self.ffmpeg_path = resource_path(ffmpeg_binary)

        try:
            if not os.path.exists(self.ffmpeg_path):
                raise FileNotFoundError(f"FFmpeg no encontrado en: {self.ffmpeg_path}")
            if not ensure_ffmpeg_executable(self.ffmpeg_path):
                raise PermissionError(f"No se pudieron establecer permisos para FFmpeg en: {self.ffmpeg_path}")
            if not os.access(self.ffmpeg_path, os.X_OK):
                raise PermissionError(f"FFmpeg no es ejecutable en: {self.ffmpeg_path}")

            AudioSegment.converter = self.ffmpeg_path
            AudioSegment.ffmpeg = self.ffmpeg_path
            # No configuramos ffprobe para evitar dependencia
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al configurar FFmpeg inicial:\n{str(e)}\nRuta intentada: {self.ffmpeg_path}")
            sys.exit(1)

        # Configuración de la ventana principal
        self.setWindowTitle("Audio Analyzer (by CeleroLab.Com)")
        self.setGeometry(100, 100, 400, 500)
        self.setMinimumSize(400, 300)

        # Cargar tipografía moderna
        self.default_font = QFont("Roboto", 11) if "Roboto" in QFontDatabase.families() else QFont("Arial", 11)

        # Tema oscuro
        self.set_dark_theme()

        # Crear el widget central y el layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Encabezado
        header_label = QLabel("Audio Analyzer")
        header_label.setFont(QFont("Roboto", 24, QFont.Weight.Bold) if "Roboto" in QFontDatabase.families() else QFont("Arial", 24, QFont.Weight.Bold))
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(header_label)

        # Botón para cargar archivo de audio
        self.load_button = self.create_styled_button("Load Audio File")
        self.load_button.setFont(QFont("Roboto", 12, QFont.Weight.Bold) if "Roboto" in QFontDatabase.families() else QFont("Arial", 12, QFont.Weight.Bold))
        self.load_button.setMinimumHeight(60)
        self.load_button.clicked.connect(self.load_audio_file)
        main_layout.addWidget(self.load_button)

        # Campo para mostrar la ruta actual de ffmpeg
        self.ffmpeg_path_label = QLabel(f"FFmpeg Path: {self.ffmpeg_path}")
        self.ffmpeg_path_label.setFont(self.default_font)
        self.ffmpeg_path_label.setStyleSheet("padding: 8px; border-radius: 4px; background-color: rgba(255, 255, 255, 0.1);")
        main_layout.addWidget(self.ffmpeg_path_label)

        # Etiqueta para mostrar la información del audio
        self.audio_info_label = QLabel("Select an audio file to analyze.")
        self.audio_info_label.setFont(self.default_font)
        self.audio_info_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.audio_info_label.setStyleSheet("padding: 15px; border-radius: 8px; background-color: rgba(255, 255, 255, 0.05);")
        self.audio_info_label.setWordWrap(True)
        main_layout.addWidget(self.audio_info_label, stretch=1)

        # Botón para cambiar la ruta de ffmpeg
        self.ffmpeg_button = self.create_styled_button("Change FFmpeg Path")
        self.ffmpeg_button.setFont(QFont("Roboto", 10, QFont.Weight.Bold) if "Roboto" in QFontDatabase.families() else QFont("Arial", 10, QFont.Weight.Bold))
        self.ffmpeg_button.clicked.connect(self.change_ffmpeg_path)
        main_layout.addWidget(self.ffmpeg_button)

    def create_styled_button(self, text):
        button = QPushButton(text)
        button.setFont(self.default_font)
        button.setStyleSheet("""
            QPushButton {
                background-color: #6200EE;
                color: white;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #7F39FB;
            }
            QPushButton:pressed {
                background-color: #3700B3;
            }
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(2, 2)
        button.setGraphicsEffect(shadow)
        button.clicked.connect(lambda: self.animate_button(button))
        return button

    def animate_button(self, button):
        anim = QPropertyAnimation(button, b"geometry")
        anim.setDuration(100)
        original_geometry = button.geometry()
        anim.setStartValue(original_geometry)
        shrunk_geometry = original_geometry.adjusted(2, 2, -2, -2)
        anim.setEndValue(shrunk_geometry)
        anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        anim.start()
        anim.finished.connect(lambda: button.setGeometry(original_geometry))

    def set_dark_theme(self):
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.ColorRole.Window, QColor(30, 30, 30))
        dark_palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Base, QColor(45, 45, 45))
        dark_palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Button, QColor(70, 70, 70))
        dark_palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(98, 0, 238))
        QApplication.setPalette(dark_palette)

    def change_ffmpeg_path(self):
        new_path, _ = QFileDialog.getOpenFileName(self, "Select FFmpeg Executable", "", "Executable Files (*.exe)" if sys.platform.startswith('win') else "All Files (*)")
        if new_path:
            try:
                if not os.path.exists(new_path):
                    raise FileNotFoundError(f"El archivo seleccionado no existe: {new_path}")
                if not os.access(new_path, os.X_OK):
                    os.chmod(new_path, os.stat(new_path).st_mode | stat.S_IEXEC)
                    if not os.access(new_path, os.X_OK):
                        raise PermissionError(f"No se pudo hacer ejecutable: {new_path}")

                # Actualizar la configuración de pydub
                AudioSegment.converter = new_path
                AudioSegment.ffmpeg = new_path
                self.ffmpeg_path = new_path
                self.ffmpeg_path_label.setText(f"FFmpeg Path: {self.ffmpeg_path}")

                # Prueba para asegurar que funciona
                test_audio = AudioSegment.silent(duration=100)
                if not test_audio:
                    raise RuntimeError("El nuevo FFmpeg no funciona correctamente")
                
                QMessageBox.information(self, "Éxito", "Ruta de FFmpeg actualizada correctamente.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al cambiar la ruta de FFmpeg:\n{str(e)}")

    def load_audio_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Audio File", "", "Audio Files (*.mp3 *.wav *.ogg *.flac)")
        if file_path:
            try:
                audio = AudioSegment.from_file(file_path)

                # Obtener información básica directamente desde AudioSegment
                duration = len(audio) / 1000.0
                loudness = audio.dBFS
                peak_db = audio.max_dBFS
                channels = audio.channels
                sample_rate = audio.frame_rate

                # Normalización para LUFS
                audio_array = np.array(audio.get_array_of_samples(), dtype=float)
                if audio.sample_width == 2:
                    audio_array /= 32768.0
                elif audio.sample_width == 3:
                    audio_array /= 8388608.0
                elif audio.sample_width == 4:
                    audio_array /= 2147483648.0

                meter = pyln.Meter(sample_rate)
                lufs = meter.integrated_loudness(audio_array.reshape(-1, channels))

                audio_info = f"""
                <b>Audio Properties:</b><br><br>
                <b>File:</b> {os.path.basename(file_path)}<br>
                <b>Sample Rate:</b> {sample_rate} Hz<br>
                <b>Channels:</b> {channels}<br>
                <b>Duration:</b> {duration:.2f} seconds<br>
                <b>Loudness (dBFS):</b> {loudness:.2f}<br>
                <b>Peak dB:</b> {peak_db:.2f}<br>
                <b>LUFS:</b> {lufs:.2f}<br>
                """
                self.audio_info_label.setText(audio_info)

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load audio file: {str(e)}")

def main():
    app = QApplication(sys.argv)
    
    if getattr(sys, 'frozen', False):
        icon_path = os.path.join(sys._MEIPASS, 'icono.ico')
    else:
        icon_path = "icono.ico"
    app.setWindowIcon(QIcon(icon_path))
    
    window = AudioAnalyzerApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()