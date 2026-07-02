from PySide6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QPushButton,
    QTextEdit, QLineEdit, QFileDialog,
    QVBoxLayout, QHBoxLayout,
    QProgressBar, QComboBox, QMessageBox
)

from PySide6.QtCore import Qt, QThread

from app.core.xtts_engine import XTTSEngine
from app.core.worker import GenerateWorker


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("🎙 Tantan24 Voice Studio V2")
        self.resize(1400, 900)

        # =========================
        # Engine + Worker Thread
        # =========================

        self.engine = XTTSEngine()

        self.thread = QThread()
        self.worker = GenerateWorker(self.engine)
        self.worker.moveToThread(self.thread)

        self.thread.start()

        # Signals
        self.worker.finished.connect(self.on_finished)
        self.worker.error.connect(self.on_error)
        self.worker.progress.connect(self.on_progress)
        self.worker.log.connect(self.on_log)

        # =========================
        # UI
        # =========================

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)

        # -------------------------
        # Reference voice
        # -------------------------

        self.editReference = QLineEdit()
        self.editReference.setPlaceholderText("Choose reference voice...")

        self.btnBrowse = QPushButton("Browse")

        ref_layout = QHBoxLayout()
        ref_layout.addWidget(self.editReference)
        ref_layout.addWidget(self.btnBrowse)

        layout.addLayout(ref_layout)

        # -------------------------
        # Language
        # -------------------------

        self.comboLanguage = QComboBox()
        self.comboLanguage.addItems(["Arabic", "French", "English", "Darija"])

        layout.addWidget(self.comboLanguage)

        # -------------------------
        # Text input
        # -------------------------

        self.textEditInput = QTextEdit()
        self.textEditInput.setPlaceholderText("Write your text...")
        self.textEditInput.setMinimumHeight(200)

        layout.addWidget(self.textEditInput)

        # -------------------------
        # Progress
        # -------------------------

        self.progress = QProgressBar()
        self.progress.setValue(0)

        layout.addWidget(self.progress)

        # -------------------------
        # Buttons
        # -------------------------

        self.btnGenerate = QPushButton("🎙 Generate")
        self.btnStop = QPushButton("⛔ Stop")

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btnGenerate)
        btn_layout.addWidget(self.btnStop)

        layout.addLayout(btn_layout)

        # -------------------------
        # Status
        # -------------------------

        self.lblStatus = QLabel("Ready")
        self.lblStatus.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.lblStatus)

        # =========================
        # Signals
        # =========================

        self.btnBrowse.clicked.connect(self.browse_file)
        self.btnGenerate.clicked.connect(self.start_generation)
        self.btnStop.clicked.connect(self.stop_generation)

    # -------------------------------------------------
    # Browse file
    # -------------------------------------------------

    def browse_file(self):

        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Choose Voice",
            "",
            "Audio Files (*.wav *.mp3)"
        )

        if file_name:
            self.editReference.setText(file_name)

    # -------------------------------------------------
    # Start generation (FIXED)
    # -------------------------------------------------

    def start_generation(self):

        text = self.textEditInput.toPlainText().strip()
        speaker = self.editReference.text().strip()

        language = self.comboLanguage.currentText()

        lang_map = {
            "Arabic": "ar",
            "French": "fr",
            "English": "en",
            "Darija": "ar"
        }

        language = lang_map.get(language, "ar")

        # -------------------------
        # DEBUG SAFE
        # -------------------------

        print("START GENERATION")
        print("TEXT:", text)
        print("SPEAKER:", speaker)
        print("LANG:", language)

        # -------------------------
        # VALIDATION
        # -------------------------

        if not text:
            QMessageBox.warning(self, "Error", "Write text first")
            return

        if not speaker:
            QMessageBox.warning(self, "Error", "Choose reference voice")
            return

        self.progress.setValue(0)
        self.lblStatus.setText("Generating...")

        # تشغيل worker
        self.worker.generate(text, speaker, language)

    # -------------------------------------------------
    # Stop generation
    # -------------------------------------------------

    def stop_generation(self):
        self.worker.stop()
        self.lblStatus.setText("Stopping...")

    # -------------------------------------------------
    # Worker signals
    # -------------------------------------------------

    def on_progress(self, value):
        self.progress.setValue(value)

    def on_log(self, msg):
        self.lblStatus.setText(msg)

    def on_finished(self, output):

        self.progress.setValue(100)
        self.lblStatus.setText("Done ✅")

        QMessageBox.information(
            self,
            "Success",
            f"Saved:\n{output}"
        )

    def on_error(self, error):

        self.progress.setValue(0)
        self.lblStatus.setText("Error ❌")

        QMessageBox.critical(
            self,
            "Error",
            error
        )

    # -------------------------------------------------
    # CLEAN EXIT (FIX QTHREAD WARNING)
    # -------------------------------------------------

    def closeEvent(self, event):

        self.worker.stop()
        self.thread.quit()
        self.thread.wait()

        event.accept()