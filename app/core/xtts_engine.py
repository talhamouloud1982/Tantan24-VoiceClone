import os
import subprocess
from TTS.api import TTS


class XTTSEngine:

    def __init__(self):

        print("🚀 Loading XTTS v2 model...")

        self.tts = TTS(
            "tts_models/multilingual/multi-dataset/xtts_v2",
            gpu=True
        )

        print("✅ XTTS Loaded")

        self.reference_cache = {}

    # -------------------------------------------------
    # Clean reference audio
    # -------------------------------------------------

    def prepare_reference(self, input_path, output_path="output/ref_clean.wav"):

        os.makedirs("output", exist_ok=True)

        if input_path in self.reference_cache:
            return self.reference_cache[input_path]

        command = [
            "ffmpeg",
            "-y",
            "-i", input_path,
            "-ac", "1",
            "-ar", "22050",
            "-af",
            "highpass=f=70,lowpass=f=12000,"
            "loudnorm=I=-16:TP=-1.5:LRA=11,"
            "acompressor=threshold=-18dB:ratio=3:attack=5:release=50",

            output_path
        ]

        subprocess.run(command, check=True)

        self.reference_cache[input_path] = output_path

        return output_path

    # -------------------------------------------------
    # Text cleaner (important for natural speech)
    # -------------------------------------------------

    def clean_text(self, text: str):

        text = text.strip()

        text = text.replace("  ", " ")
        text = text.replace(",", ", ")
        text = text.replace(".", ". ")
        text = text.replace("!", "! ")
        text = text.replace("?", "? ")

        return text

    # -------------------------------------------------
    # Generate speech
    # -------------------------------------------------

    def generate(self, text, speaker, output, language="ar"):

        os.makedirs("output", exist_ok=True)

        speaker_wav = self.prepare_reference(speaker)

        text = self.clean_text(text)

        print("🎙 Generating ...")

        self.tts.tts_to_file(
            text=text,
            speaker_wav=speaker_wav,
            language=language,
            file_path=output,

            temperature=0.25,        # 🎯 Natural voice
            length_penalty=1.2,      # 🎯 Better rhythm
            repetition_penalty=6.0,  # 🎯 Avoid repetition
            top_k=20,                # 🎯 More stable output
            top_p=0.7,               # 🎯 Focused sampling
        )

        print("✅ XTTS done:", output)


        return output

    # -------------------------------------------------
    # Post processing (voice enhancement)
    # -------------------------------------------------

    def post_process(self, input_path, output_path):

        command = [
            "ffmpeg",
            "-y",
            "-i", input_path,
            "-af",
            "highpass=f=70,"
            "lowpass=f=12000,"
            "loudnorm=I=-14:TP=-1.5:LRA=11,"
            "acompressor=threshold=-18dB:ratio=3:attack=5:release=50,"
            "dynaudnorm=f=150:g=15",

            output_path
        ]

        subprocess.run(command, check=True)