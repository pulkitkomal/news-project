import string
import re
import nltk
from nltk.corpus import stopwords


nltk.download("stopwords")


class TextProcessor:
    def __init__(self):
        self.stop_words = set(stopwords.words("english"))

    @staticmethod
    def clean_text(text):
        """Clean the text by removing URLs, punctuation, and unnecessary formatting."""

        if not text:
            return False

        # Remove URLs
        text = re.sub(r"http\S+|www\S+|https\S+", "", text, flags=re.MULTILINE)

        # Convert to lowercase
        text = text.lower()

        # Remove punctuation
        text = text.translate(str.maketrans("", "", string.punctuation))

        # Remove extra whitespace
        text = re.sub(r"\s+", " ", text).strip()

        return text

    def split_text(self, text, max_length=500):
        """Split long text into smaller chunks."""
        cleaned_text = self.clean_text(text)
        words = cleaned_text.split()
        return [
            " ".join(words[i : i + max_length])
            for i in range(0, len(words), max_length)
        ]
