from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QFileDialog
from PyQt5.QtCore import pyqtSignal, QThread
import sys
import subprocess

class FFmpegThread(QThread):
    output_signal = pyqtSignal(str)  # Signaali merkkijonon välittämiseen

    def __init__(self, cmd):
        super().__init__()
        self.cmd = cmd

    def run(self):
        process = subprocess.Popen(
            self.cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
        )
        for line in process.stdout:
            self.output_signal.emit(line.strip())


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(700, 300, 500, 500)
        self.initUI()

    def initUI(self):
        # Tekstilaatikko logia varten
        self.text_edit = QTextEdit(self)
        self.text_edit.setGeometry(50, 50, 400, 100)
        self.text_edit.setReadOnly(True)

        # Nappi FFmpeg-komennolle
        button = QPushButton('Activate FFmpeg', self)
        button.setGeometry(150, 200, 200, 100)
        button.clicked.connect(self.on_button_click)

        button_select = QPushButton('Valitse tiedosto', self)
        button_select.setGeometry(150, 150, 200, 40)
        button_select.clicked.connect(self.select_file)

    def on_button_click(self):
        # FFmpeg-komento (muokkaa tarpeen mukaan)
        cmd = ["ffmpeg", "-i", self.input_file, "output.avi"]
        
        # Luo säie ja yhdistä signaali tekstilaatikkoon
        self.ffmpeg_thread = FFmpegThread(cmd)
        self.ffmpeg_thread.output_signal.connect(self.text_edit.append)
        self.ffmpeg_thread.start()

    def select_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Valitse videon tiedosto",
            "",
            "Video files (*.mp4 *.avi *.mkv);;All Files (*)",
            options=options
        )
        if file_name:
            self.input_file = file_name
            self.text_edit.append(f"Valittu tiedosto: {file_name}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
