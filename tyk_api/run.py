from horizon_fastapi_template import general_create_app

app = general_create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)