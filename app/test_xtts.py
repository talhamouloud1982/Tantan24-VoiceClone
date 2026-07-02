from TTS.api import TTS
import os

print("🚀 STARTING XTTS")

tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")

print("✅ MODEL LOADED")

os.makedirs("output", exist_ok=True)

tts.tts_to_file(
    text="ففي تطور أثار الكثير من التساؤلات، تم إلغاء صفقة تهيئة شارع الحسن الثاني بعد امتناع الشركة الفائزة بالصفقة عن الشروع في الأشغال، دون تقديم توضيحات كافية حول الأسباب الحقيقية التي دفعتها إلى عدم مباشرة تنفيذ المشروع، رغم استكمال الإجراءات المرتبطة بإسناد الصفقة",
    speaker_wav="models/reference.wav",
    file_path="output/test.wav",
    language="ar"
)

print("🎉 DONE - check output/test.wav")