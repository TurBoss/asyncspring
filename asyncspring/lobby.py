import asyncio
import importlib
import logging

from asyncblink import signal

from asyncspring.protocol import LobbyProtocolWrapper, LobbyProtocol, connections
from asyncspring.plugins import core

loop = asyncio.get_event_loop()

plugins = []

log = logging.getLogger(__name__)


def plugin_registered_handler(plugin_name):
    plugins.append(plugin_name)


signal("plugin-registered").connect(plugin_registered_handler)


def load_plugins(*plugins):
    for plugin in plugins:
        if plugin not in plugins:
            importlib.import_module(plugin)


async def connect(server, port=8200, use_ssl=False):
    """
    Connect to an SpringRTS Lobby server. Returns a proxy to an LobbyProtocol object.
    """
    protocol = None
    while protocol is None:
        try:
            transport, protocol = await loop.create_connection(LobbyProtocol, host=server, port=port, ssl=use_ssl)
        except ConnectionRefusedError as conn_error:
            log.info("HOST DOWN! retry in 10 secs {}".format(conn_error))
            await asyncio.sleep(10)

    # self.logger.info("connected")
    protocol.wrapper = LobbyProtocolWrapper(protocol)
    protocol.server_info = {"host": server, "port": port, "ssl": use_ssl}
    protocol.netid = "{}:{}:{}{}".format(id(protocol), server, port, "+" if use_ssl else "-")

    signal("netid-available").send(protocol)

    connections[protocol.netid] = protocol.wrapper

    return protocol.wrapper


async def reconnect(client_wrapper):
    protocol = None
    server_info = client_wrapper.server_info

    log.info("reconnecting")
    while protocol is None:
        await asyncio.sleep(10)
        try:
            transport, protocol = await loop.create_connection(LobbyProtocol, **server_info)
            client_wrapper.protocol = protocol

            signal("netid-available").send(protocol)

            signal("reconnected").send()

        except ConnectionRefusedError as conn_error:
            pass
            log.info("HOST DOWN! retry in 10 secs {}".format(conn_error))
