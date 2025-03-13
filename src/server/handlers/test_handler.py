from fastapi import Response, Request


class TestHandler:
    async def ping(self) -> Response:
        return Response(
            content="pong"
        )

    async def preflight_handler(self, request: Request):
        return Response(
            content="",
            status_code=204,
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS, GET, POST, PUT, DELETE",
                "Access-Control-Allow-Headers": "*",
            }
        )
