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

# LABEL = 'review_needed' # label name
LABEL1 = 'GSSoC23'
LABEL2 = 'CX'

@router.register("issues", action="opened")
async def issue_opened_event(event, gh, *args, **kwargs):
	label = event.data['issue']['labels_url']

	installation_id = event.data["installation"]["id"]

	issue_body = event.data["issue"]["body"]

	installation_access_token = await apps.get_installation_access_token(
		gh,
		installation_id=installation_id,
		app_id=os.environ.get("APP_ID"),
		private_key=os.environ.get("PRIVATE_KEY")
	)

	if(issue_body.find("Community Exchange") == -1):
		pass
	else:
		await gh.post(label, data=[LABEL2],
		oauth_token=installation_access_token["token"]
				 )

	if(issue_body.find("GSSOC23") == -1):
		pass
	else:
		await gh.post(label, data=[LABEL1],
		oauth_token=installation_access_token["token"])