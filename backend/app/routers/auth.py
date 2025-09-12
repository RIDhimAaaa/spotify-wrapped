# app/routers/auth.py
import random
import string
import urllib.parse
import requests # Add this import
from fastapi import APIRouter, Request # Add Request
from fastapi.responses import RedirectResponse
from app.core.config import settings

router = APIRouter()

@router.get("/login")
def login_to_spotify():
    # ... (this function remains the same)
    scope = "user-top-read playlist-modify-public"
    state = ''.join(random.choices(string.ascii_letters + string.digits, k=16))

    auth_params = {
        'response_type': 'code',
        'client_id': settings.SPOTIFY_CLIENT_ID,
        'scope': scope,
        'redirect_uri': settings.REDIRECT_URI,
        'state': state
    }

    auth_url = f"https://accounts.spotify.com/authorize?{urllib.parse.urlencode(auth_params)}"
    return RedirectResponse(url=auth_url)


# NEW: Add the /callback endpoint
@router.get("/callback")
def get_spotify_token(request: Request):
    code = request.query_params.get('code')
    state = request.query_params.get('state')

    if state is None:
        return {"error": "state_mismatch"}
    else:
        token_url = "https://accounts.spotify.com/api/token"

        payload = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': settings.REDIRECT_URI,
        }

        # The Authorization header requires a base64 encoded string of client_id:client_secret
        response = requests.post(
            token_url,
            data=payload,
            auth=(settings.SPOTIFY_CLIENT_ID, settings.SPOTIFY_CLIENT_SECRET)
        )

        token_info = response.json()

        # For now, we'll just return the token info to see it work
        return token_info