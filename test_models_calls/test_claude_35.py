import os
from dotenv import load_dotenv
load_dotenv()

from llm.claude_models import Claude35, Claude4

model = Claude35()
reponse = model.generate('Test', 20)
print(f"Model version used: {reponse.model}" )
print(reponse)

def test_claude(model_choose):
    """ 
    Models to choose : "Claude35" , "Claude4"
    """
    model=model_choose()
    reponse = model.generate('Test', 10)
    