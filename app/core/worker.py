from PySide6.QtCore import QObject, Signal, Slot

from app.core.xtts_engine import XTTSEngine
from app.core.text_splitter import TextSplitter

import os


class GenerateWorker(QObject):

    finished = Signal(str)
    error = Signal(str)
    progress = Signal(int)
    log = Signal(str)

    def __init__(self, engine=None):
        super().__init__()

        self.engine = engine if engine else XTTSEngine()
        self.splitter = TextSplitter()

        self._cancel = False

    # -------------------------------------------------
    # Stop generation
    # -------------------------------------------------

    def stop(self):
        self._cancel = True

    # -------------------------------------------------
    # Main generation slot
    # -------------------------------------------------

    @Slot(str, str, str)
    def generate(self, text, speaker, language="ar"):

        try:
            self._cancel = False

            os.makedirs("output", exist_ok=True)

            self.log.emit("📄 Splitting text...")

            parts = self.splitter.split(text)

            total = len(parts)
            files = []

            if total == 0:
                raise ValueError("No text to generate")

            for i, part in enumerate(parts):

                if self._cancel:
                    self.log.emit("⛔ Cancelled")
                    return

                self.log.emit(f"🎙 Part {i+1}/{total}")

                output_file = f"output/part_{i:03d}.wav"

                self.engine.generate(
                    text=part,
                    speaker=speaker,
                    output=output_file,
                    language=language
                )

                files.append(output_file)

                percent = int(((i + 1) / total) * 90)
                self.progress.emit(percent)

            self.log.emit("🔗 Merging audio...")

            final_output = "output/final.wav"

            self.engine.merge_files(files, final_output)

            self.progress.emit(100)
            self.log.emit("✅ Done")

            self.finished.emit(final_output)

        except Exception as e:
            self.error.emit(str(e))
            print("🔥 LOADED NEW WORKER FILE")