from google import genai
from google.genai import types
from config.configs import settings

client = genai.Client(api_key=settings.google_api_key)


class EmbeddingGenerator:
    @staticmethod
    def get_embedding(text):
        result = client.models.embed_content(model="text-embedding-004", contents=text)

        return result.embeddings[0]
