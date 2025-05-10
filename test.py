from config.configs import settings
from main import get_context


# input = 'Tell me about Pakistan and the on going war.'
input = 'Tell me about Jio.'

keywords = openai_obj.get_keywords(text=input)
context = get_context(keywords, settings.mongo_uri, settings.db_name)
openai_obj.generate_response(text=input, context=context)