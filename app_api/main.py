#app_api/main.py

from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

# def main():
#     print("Hello from app-api!")


# if __name__ == "__main__":
#     main()
