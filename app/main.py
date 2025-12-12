from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth, OAuthError
from .config import CLIENT_ID, CLIENT_SECRET
from fastapi.staticfiles import StaticFiles

from . import booking
from db.database import Base, engine
Base.metadata.create_all(bind=engine)




app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="hdpd07")
app.mount("/static",StaticFiles(directory="static"),name="static")




oauth = OAuth()
oauth.register(
    name='google',
    server_metadata_url = 'https://accounts.google.com/.well-known/openid-configuration',
    client_id = CLIENT_ID,
    client_secret = CLIENT_SECRET,
    client_kwargs={
        'scope': 'email openid profile',
        'redirect_url': 'http://localhost:8000/auth'
    }
)

templates = Jinja2Templates(directory="templates")

app.include_router(booking.router)

@app.get("/")
def index(request:Request):
    user = request.session.get('user')
    if user:
        return RedirectResponse('main')
    return templates.TemplateResponse(
        name="login.html",
        context={"request":request}
    )

@app.get("/main")
def welcome(request:Request):
    user = request.session.get('user')
    if not user:
        return RedirectResponse('/')
    return templates.TemplateResponse(
        name = "main.html",
        context={'request':request, 'user':user}
    )


@app.get("/login")
async def login(request:Request):
    url = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, url)

@app.get("/auth")
async def auth(request : Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as e:
        return templates.TemplateResponse(
            name="error.html",
            context={'request':request, 'error':e.error}
        )
    user = token.get('userinfo')
    if user:
        request.session['user'] = dict(user)
    
    print("User object from google ",user)
    return RedirectResponse('main')


@app.get("/logout")
def logout(request : Request):
    request.session.pop('user')
    return RedirectResponse('/')