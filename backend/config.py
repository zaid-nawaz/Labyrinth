import os
from dotenv import load_dotenv

load_dotenv()

SUPADATA_API_KEY=os.getenv("SUPADATA_API_KEY")
OPENROUTER_API_KEY=os.getenv("OPENROUTER_API_KEY")  