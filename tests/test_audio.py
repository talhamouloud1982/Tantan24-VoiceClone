from app.core.audio_processor import AudioProcessor

processor = AudioProcessor()

processor.enhance(
    "output/test.wav",
    "output/final.wav"
)

print("✅ Audio Enhanced")