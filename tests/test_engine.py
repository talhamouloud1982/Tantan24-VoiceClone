print("START 1")

import torch
print("TORCH OK")

try:
    print("TRY IMPORT F5...")

    from f5_tts.api import F5TTS

    print("F5 IMPORT OK")

    tts = F5TTS()
    print("MODEL CREATED OK")

    tts.tts_to_file(
        text="اختبار صوتي",
        speaker_wav="models/reference.wav",
        file_path="output/test.wav"
    )

    print("DONE")

except Exception as e:
    print("❌ REAL ERROR:")
    print(e)