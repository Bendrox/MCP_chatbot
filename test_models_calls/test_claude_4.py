import os
from dotenv import load_dotenv
load_dotenv()

from llm.claude_models import Claude4

model = Claude4()
reponse = model.generate('Test', 20)
print(f"Model version used: {reponse.model}" )
print(reponse)