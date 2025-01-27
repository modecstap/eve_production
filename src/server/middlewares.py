import json
from typing import Type, Callable

from aiohttp import web
from aiohttp.web import HTTPBadRequest, HTTPInternalServerError, HTTPOk, Response
from pydantic import BaseModel

EMPTY = object()


class Middlewares:
    @web.middleware
    async def response_status(self, request: web.Request, handler):
        try:
            response = await handler(request)
            if response and isinstance(response, list):
                return Response(body=json.dumps([item.model_dump(mode='json', by_alias=True) for item in response]))
            elif response and isinstance(response, BaseModel):
                return Response(body=json.dumps(response.model_dump(mode='json', by_alias=True)))
            elif response is not None:
                return response
            else:
                return HTTPOk()
        except Exception as e:
            print(str(e))
            return HTTPInternalServerError(reason=str(e))

    @web.middleware
    async def model_type(self, request: web.Request, handler) -> web.Response:
        request_model = None
        try:
            request_type = self.__get_request_type(handler)
            if request_type:
                request_body = await request.json()
                if hasattr(request_type, '__origin__') and request_type.__origin__ == list:
                    item_type = request_type.__args__[0]
                    request_model = [item_type(**data) for data in request_body]
                else:
                    request_model = request_type(**request_body)
        except json.JSONDecodeError as e:
            print(str(e))
            return HTTPBadRequest(reason='Invalid JSON format')

        if not request_model:
            return await handler(request)

        return await handler(request, request_model)

    def __get_request_type(self, handler: Callable) -> Type | None:
        annotations: dict = handler.__annotations__
        for field_name in annotations.keys():
            if field_name == 'request' or field_name == 'return':
                continue
            return annotations.get(field_name)

        return None
