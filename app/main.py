from fastapi import FastAPI
from paste.router import router as router_posts
from pages.router import router as router_pages


app = FastAPI(title='Pastebin')

app.include_router(router_posts)
app.include_router(router_pages)
