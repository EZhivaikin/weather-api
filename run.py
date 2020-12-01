from application import app
import uvicorn

from application.config.application import settings

app = app.init(settings)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
