import uvicorn

from src.app import create_app

application = create_app()

if __name__ == '__main__':
    uvicorn.run("main:application", reload=True)
