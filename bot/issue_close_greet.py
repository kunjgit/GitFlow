import asyncio
import os
import sys
import traceback
import aiohttp
from aiohttp import web
from gidgethub import aiohttp as gh_aiohttp
from gidgethub import routing
from gidgethub import sansio
from gidgethub import apps


router = routing.Router()


@router.register("issues", action="closed")
async def issue_opened_event(event, gh, *args, **kwargs):

    installation_id = event.data["installation"]["id"]

    installation_access_token = await apps.get_installation_access_token(
        gh,
        installation_id=installation_id,
        app_id=os.environ.get("APP_ID"),
        private_key=os.environ.get("PRIVATE_KEY")
    )
    url = event.data['issue']['comments_url']
    author = event.data['issue']['user']['login']
    message = f"Thanks for contributing to this issue @{author}! We are pleased to have your valuable contribution 💗."
    
    await gh.post(url, data={
        'body': message,
        },
        oauth_token=installation_access_token["token"]
                 )
