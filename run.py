import uvicorn
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    uvicorn.run("zenik_backend.asgi:application", port=8121, log_level='info')