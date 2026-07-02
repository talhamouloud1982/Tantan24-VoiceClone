import torch
import torchaudio
from TTS.api import TTS

from app.core.base_engine import BaseVoiceEngine
from app.core.logger import logger


class XTTSVoiceEngine(BaseVoiceEngine):
    """
    XTTS Engine (Coqui TTS)
    Clean Architecture version
    """

    def __init__(self, device: str = "cuda"):
        self.device = device
        self.model = None
        self.loaded = False

    # -----------------------------
    # Load Model
    # -----------------------------
    def load_model(self):
        try:
            logger.info("Loading XTTS model...")

            self.model = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
            self.model.to(self.device)

            self.loaded = True
            logger.info("XTTS model loaded successfully")

        except Exception as e:
            logger.error(f"Failed to load XTTS model: {e}")
            raise

    # -----------------------------
    # Generate Speech
    # -----------------------------
    def generate(
        self,
        text: str,
        speaker_wav: str,
        output_path: str,
        language: str = "ar"
    ) -> str:

        if not self.loaded:
            self.load_model()

        try:
            logger.info("Generating speech with XTTS...")

            # تنظيف النص (حل مشكلة text undefined سابقًا)
            text = str(text).strip()

            if not text:
                raise ValueError("Text is empty")

            # توليد الصوت
            self.model.tts_to_file(
                text=text,
                speaker_wav=speaker_wav,
                language=language,
                file_path=output_path
            )

            logger.info(f"Audio saved to: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"XTTS generation error: {e}")
            raise

    # -----------------------------
    # Unload Model
    # -----------------------------
    def unload(self):
        try:
            logger.info("Unloading XTTS model...")

            del self.model
            self.model = None
            self.loaded = False

            if torch.cuda.is_available():
                torch.cuda.empty_cache()

            logger.info("XTTS unloaded successfully")

        except Exception as e:
            logger.error(f"Unload error: {e}")