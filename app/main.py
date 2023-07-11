from fastapi import FastAPI
from paste.router import router as router_posts


app = FastAPI(title='Pastebin')

app.include_router(router_posts)
