import asyncio
import json
from tempfile import template

from fastapi import APIRouter, HTTPException
from redis.commands.search.reducers import count
from starlette.requests import Request
from sse_starlette.sse import EventSourceResponse
from starlette.templating import Jinja2Templates

from contants import TEMPLATES_FOLDER

# Simulated database
fake_db = {
    '1': {'name': 'John', 'age': 25},
    '2': {'name': 'Jane', 'age': 22},
    '3': {'name': 'Jim', 'age': 30},
    '4': {'name': 'Jack', 'age': 27},
    '5': {'name': 'Jill', 'age': 24},
}

router_sse = APIRouter(tags=["sse"])
STREAM_DELAY = 5  # second
RETRY_TIMEOUT = 15000  # milliseconds
count = 0

def new_messages(is_intercept: bool = False):
    global count
    count += 1
    return {"event": "new_message", "id": count, "data": "Hello, world!", "is_intercept": "is_intercept"}


@router_sse.get("/main_stream")
async def main_stream(request: Request):
    async def event_generator():
        while True:
            if await request.is_disconnected():
                break

            message = new_messages(request.query_params.get('is_intercept') == 'true')
            if message:
                yield {
                    "event": message['event'],
                    "id": message['id'],
                    "retry": RETRY_TIMEOUT,
                    "data": message,
                }

            await asyncio.sleep(STREAM_DELAY)

    return EventSourceResponse(event_generator())


@router_sse.get("/second_stream")
async def second_stream(request: Request):# Simulate a new message
    async def event_generator():
        while True:
            if await request.is_disconnected():
                break

            message = new_messages()
            if message:
                yield {
                    "event": message['event'],
                    "id": message['id'],
                    "retry": RETRY_TIMEOUT,
                    "data": message['data']
                }

            await asyncio.sleep(STREAM_DELAY)

    return EventSourceResponse(event_generator())


def dashboard_streams(request: Request):
    template_name = "sse_dashboard.html"
    templates = Jinja2Templates(directory=TEMPLATES_FOLDER)

    def get_streams(routes):
        streams = []
        for route in routes:
            # TODO: Fix this check isinstance(route, APIRoute)
            if hasattr(route, 'tags') and "sse" in route.tags:
                streams.append(
                    {
                        "id": route.name,
                        "name": " ".join([el.title() for el in route.name.split('_')]),
                        "url": route.path
                    }
                )
        return streams

    context = {
        "streams": get_streams(request.app.routes),
        "auth_url": request.app.url_path_for('access_token'),
    }
    return templates.TemplateResponse(
        request=request, name=template_name, context=context
    )
