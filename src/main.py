import asyncio
import signal
import sys

from src.config import Settings
from src.server import MainServer
from src.storage import Database


async def main():
    Settings()
    await Database().create_all()

    server = MainServer()
    await server.start()

    loop = asyncio.get_event_loop()

    stop = asyncio.Event()
    if sys.platform != 'win32':
        loop.add_signal_handler(signal.SIGTERM, stop.set)
        loop.add_signal_handler(signal.SIGINT, stop.set)
    else:
        loop.create_task(_windows_wait_for_ctrl_c(stop))

    await stop.wait()
    await server.stop()


async def _windows_wait_for_ctrl_c(stop_event):
    """Ожидание Ctrl+C на Windows."""
    try:
        while True:
            await asyncio.sleep(0.1)
    except KeyboardInterrupt:
        stop_event.set()


if __name__ == '__main__':
    asyncio.run(main())
