import traceback
from PyQt6.QtCore import QThread, pyqtSignal

from app.core.logger import logger


class VoiceWorker(QThread):
    """
    Worker Thread آمن لتوليد الصوت بدون تجميد الواجهة
    """

    # signals
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    progress = pyqtSignal(str)

    def __init__(self, engine, text, speaker_wav, output_path, language="ar"):
        super().__init__()

        self.engine = engine
        self.text = text
        self.speaker_wav = speaker_wav
        self.output_path = output_path
        self.language = language

        self._is_running = True

    # -----------------------------
    # Stop safely
    # -----------------------------
    def stop(self):
        self._is_running = False
        self.terminate()  # fallback safety

    # -----------------------------
    # Main execution
    # -----------------------------
    def run(self):
        try:
            self.progress.emit("Starting generation...")

            # حماية من النص الفارغ
            if not self.text or not self.text.strip():
                raise ValueError("Text is empty")

            if not self._is_running:
                return

            self.progress.emit("Loading engine...")

            # تحميل الموديل إذا لم يكن محملاً
            if hasattr(self.engine, "load_model"):
                self.engine.load_model()

            if not self._is_running:
                return

            self.progress.emit("Generating audio...")

            # توليد الصوت
            result_path = self.engine.generate(
                text=self.text,
                speaker_wav=self.speaker_wav,
                output_path=self.output_path,
                language=self.language
            )

            if not self._is_running:
                return

            self.progress.emit("Done")
            self.finished.emit(result_path)

        except Exception as e:
            err = traceback.format_exc()
            logger.error(err)
            self.error.emit(str(e))