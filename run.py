from application import app
import uvicorn

app = app.init()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
