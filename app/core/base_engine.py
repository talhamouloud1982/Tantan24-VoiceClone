from abc import ABC, abstractmethod


class BaseVoiceEngine(ABC):
    """
    Interface لجميع محركات الصوت (XTTS / F5 / CosyVoice)
    """

    @abstractmethod
    def load_model(self):
        """تحميل النموذج في الذاكرة"""
        pass

    @abstractmethod
    def generate(
        self,
        text: str,
        speaker_wav: str,
        output_path: str,
        language: str = "ar"
    ) -> str:
        """
        توليد الصوت وإرجاع مسار الملف الناتج
        """
        pass

    @abstractmethod
    def unload(self):
        """تفريغ GPU / RAM"""
        pass