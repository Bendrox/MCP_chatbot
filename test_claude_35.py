import os
from dotenv import load_dotenv
load_dotenv()

from claude_models import Claude35

model = Claude35()
reponse = model.generate('Test', 20)
print(reponse)