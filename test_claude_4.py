import os
from dotenv import load_dotenv
load_dotenv()

from claude_models import ClaudeSonnet

model = ClaudeSonnet()
reponse = model.generate('Test', 20)
print(reponse)