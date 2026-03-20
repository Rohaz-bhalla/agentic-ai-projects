from dotenv import load_dotenv
from .main import app
import uvicorn

load_dotenv()

def main():
    uvicorn.run(app, port=8080, host="0.0.0.0")

main()