from llm.openai_models import OpenAI_5_mini

openai=OpenAI_5_mini()

reponse = openai.generate("test")
print(reponse)