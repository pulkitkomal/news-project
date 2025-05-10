from openai import AsyncOpenAI
from config.log import logger


class OpenAIService:
    def __init__(self, OPENAI_API_KEY):
        self.client = AsyncOpenAI(
            # This is the default and can be omitted
            api_key=OPENAI_API_KEY,
        )

    async def generate_response(self, text, context):
        """Get embeddings from OpenAI API for the given text."""
        completion = await self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "developer",
                    "content": "Talk like a respected news anchor telling news personally to one person.",
                },
                {
                    "role": "system",
                    "content": f"""Given the context give a summary report in 300 words, always give response in simple text. Emphasis on important news, DONOT GIVE ANY INFORMATION NOT PRESENT IN THE CONTEXT
                    \n {context} \n""",
                },
                {
                    "role": "user",
                    "content": text,
                },
            ],
        )

        logger.info(completion.choices[0].message.content)

        return completion.choices[0].message.content

    async def get_keywords(self, text):
        """Get embeddings from OpenAI API for the given text."""
        completion = await self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "developer",
                    "content": "You are a linguisitc expert and will extract Keyphrases",
                },
                {
                    "role": "system",
                    "content": f"Give response as shown in the given example. e.g. India, City",
                },
                {
                    "role": "user",
                    "content": text,
                },
            ],
        )

        return completion.choices[0].message.content

    def convert_to_input_chat(messages):
        converted_messages = []
        for message in messages:
            if message.role == "user":
                converted_messages.append(message.content)
            else:
                continue
        return " ".join(converted_messages)
