from fastapi import Response


class TestHandler:
    async def ping(self) -> Response:
        return Response(
            content="pong"
        )

    async def preflight_handler(self):
        return Response()
