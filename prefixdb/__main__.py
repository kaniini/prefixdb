import asyncio
import aiohttp
import aiohttp.web
from . import make_app


loop = asyncio.get_event_loop()


app = make_app()
aiohttp.web.run_app(app)
