import asyncio
import aiohttp
import aiohttp.web

try:
    import ujson as json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        import json

from .types import Database


# GET /node?prefix=127.0.0.0/8
async def lookup_node(request):
    database = request.app['database']

    try:
        prefix, record = database.search_single(request.GET['prefix'])
    except KeyError:
        raise aiohttp.web.HTTPNoContent()

    output = {
        'prefix': prefix,
        'record': record
    }

    return aiohttp.web.Response(text=json.dumps(output), content_type='application/json')


# PUT /node?prefix=127.0.0.0/8
# [data]
async def upsert_node(request):
    database = request.app['database']

    try:
        with aiohttp.Timeout(0.250):
            record = await request.json()
    except:
        raise aiohttp.web.HTTPInternalServerError()

    prefix = request.GET['prefix']
    database.upsert(request.GET['prefix'], record)

    output = {
        'prefix': prefix,
        'record': record
    }

    return aiohttp.web.Response(text=json.dumps(output), content_type='application/json')


# GET /children?prefix=127.0.0.0/8
async def search_children(request):
    database = request.app['database']

    try:
        records = database.search_children(request.GET['prefix'])
    except KeyError:
        raise aiohttp.web.HTTPNoContent()

    output = [{'prefix': k, 'record': v} for k, v in records.items()]

    return aiohttp.web.Response(text=json.dumps(output), content_type='application/json')


# GET /parents?prefix=127.1.2.3
async def search_parents(request):
    database = request.app['database']

    try:
        records = database.search_parents(request.GET['prefix'])
    except KeyError:
        raise aiohttp.web.HTTPNoContent()

    output = [{'prefix': k, 'record': v} for k, v in records.items()]

    return aiohttp.web.Response(text=json.dumps(output), content_type='application/json')


def make_app(loop=None, aiohttp_middlewares=[], middlewares=[]):
    if not loop:
        loop = asyncio.get_event_loop()

    app = aiohttp.web.Application(middlewares=aiohttp_middlewares)
    app['loop'] = loop
    app['database'] = Database()

    app.router.add_route('GET', '/node', lookup_node)
    app.router.add_route('PUT', '/node', upsert_node)
    app.router.add_route('GET', '/children', search_children)
    app.router.add_route('GET', '/parents', search_parents)

    # XXX - handle middleware instantiation

    return app
