from aiohttp.web import Response, Request


class TestHandler:
    async def ping(self, request: Request) -> Response:
        return Response(
            status=200,
            text="pong"
        )

    async def preflight_handler(self, request):
        return Response(status=200)
