import uvicorn


def main():
    host = "127.0.0.1"
    port = 8001
    reload = True
    workers = 1
    uvicorn.run(app ="app.server:gym_management_app",
                host=host,
                port=port ,
                reload=reload,
                workers = workers,
                )

if __name__ == "__main__":
    main()