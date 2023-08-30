import subprocess
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from book.config import settings
from book.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        subprocess.run(
            [
                "tailwindcss",
                "-i",
                str(settings.STATIC_DIR / "src" / "input.css"),
                "-o",
                str(settings.STATIC_DIR / "css" / "main.css"),
            ]
        )
    except Exception as e:
        print(f"Error running tailwindcss: {e}")

    yield


app = FastAPI(
    lifespan=lifespan,
    default_response_class=HTMLResponse,
    openapi_url=None,
    docs_url=None,
    redoc_url=None,
)

app.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")
app.include_router(router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
