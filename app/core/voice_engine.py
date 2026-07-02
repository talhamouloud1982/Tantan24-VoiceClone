from TTS.api import TTS
import os


class VoiceEngine:
    def __init__(self):
        print("🔄 Loading XTTS model...")

        # XTTS v2 (أفضل نسخة حالياً)
        self.tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")

        print("✅ XTTS loaded")

    def generate_voice(self, text, reference_path, output_path="output/output.wav"):

        if not os.path.exists(reference_path):
            raise FileNotFoundError("Reference audio not found")

        if not text.strip():
            raise ValueError("Text is empty")

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        print("🎙️ Generating voice...")

        self.tts.tts_to_file(
            text=text,
            speaker_wav=reference_path,
            file_path=output_path,
            language="ar"
        )

        print("✅ Done:", output_path)

        return output_path