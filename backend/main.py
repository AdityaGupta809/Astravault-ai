import uvicorn
from dotenv import load_dotenv
from backend.api import app

load_dotenv()

def main():
    uvicorn.run(app, host="localhost", port=8000)

if __name__ == "__main__":
    main()