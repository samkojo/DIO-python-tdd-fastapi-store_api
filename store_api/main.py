from fastapi import FastAPI
from store_api.core.config import settings


class App(FastAPI):
    def __init__(self, *args, **kwards) -> None:
        super().__init__(
            *args,
            **kwards,
            version="0.0.1",
            title=settings.PROJECT_NAME,
            root_path=settings.ROOT_PATH,
        )


app = App()
