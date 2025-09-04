from llm.openai_models import OpenAI_5_nano

openai=OpenAI_5_nano()

reponse = openai.generate("test")
print(reponse)

reponse = openai.generate_with_tools("test", )    
print(reponse)