import uvicorn
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    uvicorn.run("k4api.wsgi:application", port=8121, log_level='info')