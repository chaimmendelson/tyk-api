from horizon_fastapi_template import general_create_app
from .src import add_routers

app = general_create_app()

add_routers(app)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)