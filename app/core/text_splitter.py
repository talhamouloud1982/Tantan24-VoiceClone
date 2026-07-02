import re


class TextSplitter:

    def __init__(self, max_words=20):
        self.max_words = max_words

    def split(self, text):

        text = text.replace("\n", " ")

        # تقسيم أولي حسب علامات الوقف
        sentences = re.split(r'(?<=[.!؟!])\s+', text)

        parts = []

        for sentence in sentences:

            sentence = sentence.strip()

            if not sentence:
                continue

            words = sentence.split()

            # إذا كانت الجملة قصيرة
            if len(words) <= self.max_words:
                parts.append(sentence)
                continue

            # إذا كانت طويلة نقسمها
            current = []

            for word in words:

                current.append(word)

                if len(current) >= self.max_words:

                    parts.append(" ".join(current))
                    current = []

            if current:
                parts.append(" ".join(current))

        return parts