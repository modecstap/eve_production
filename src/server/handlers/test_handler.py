from fastapi import Response, Request


class TestHandler:
    async def ping(self) -> Response:
        return Response(
            content="pong"
        )

    async def preflight_handler(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "OPTIONS, GET, POST, PUT, DELETE"
        response.headers["Access-Control-Allow-Headers"] = "*"
        return response
