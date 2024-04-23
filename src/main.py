import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from starlette.middleware.base import BaseHTTPMiddleware
from .apis import upload,query,download


app = FastAPI()

# 静态资源目录
app.mount("/public/assets", StaticFiles(directory="public\\assets"), name="public")

# 前端 history 路由处理
class SpaFallbackMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        if response.status_code == 404 and not "." in request.url.path:
            if not os.path.exists(os.path.join(os.getcwd(),"public/assets/index.html")):
                return HTMLResponse(content="not found")
            return FileResponse("public/assets/index.html")
        if not 'apis' in request.url.path:
            return FileResponse(f"public/assets{request.url.path}")
        return response

app.add_middleware(SpaFallbackMiddleware)
app.include_router(upload.router)
app.include_router(query.router)
app.include_router(download.router)

