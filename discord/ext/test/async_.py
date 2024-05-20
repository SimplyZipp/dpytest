import asyncio
import typing
from typing import Optional, Any, Dict

import aiohttp
import discord
from discord.webhook import async_ as dasync
from discord.webhook.async_ import async_context
import discord.http as dhttp
from . import callbacks


class FakeAdapter(dasync.AsyncWebhookAdapter):
    """
        A mock implementation of an ``AsyncWebhookAdapter``. Instead of actually sending webhook requests to discord,
        it ...
    """

    async def request(
        self,
        route: dhttp.Route,
        *args,
        **kwargs
    ) -> typing.NoReturn:
        """
            Overloaded to raise a NotImplemented error informing the user that the requested operation
            isn't yet supported by ``dpytest``. To fix this, the method call that triggered this error should be
            overloaded below to instead trigger a callback and call the appropriate backend function.

        :param args: Arguments provided to the request
        :param kwargs: Keyword arguments provided to the request
        """
        raise NotImplementedError(
            f"Operation occurred in FakeAdapter that isn't captured by the tests framework. This is dpytest's fault, "
            f"please report an issue on github. Debug Info: {route.method} {route.url} with {kwargs}"
        )

    # TODO: Override other methods

    async def create_interaction_response(
        self,
        interaction_id: int,
        token: str,
        *,
        session: aiohttp.ClientSession,
        proxy: Optional[str] = None,
        proxy_auth: Optional[aiohttp.BasicAuth] = None,
        params: dhttp.MultipartParameters
    ) -> None:
        # TODO: Use callback system
        # Setup callbacks in runner.py configure()
        # Use callbacks.dispatch_event from here
        # TODO: Follow discord API?
        # https://discord.com/developers/docs/interactions/receiving-and-responding#create-interaction-response
        #
        raise NotImplementedError(f'create_interaction_response not yet implemented.')


class FakeInteraction(discord.Interaction):

    def __init__(self, *args, **kwargs):
        # Setup the FakeAdapter. This cannot be done in any dpytest configuration because it's a ContextVar
        async_context.set(FakeAdapter())
        super().__init__(*args, **kwargs)
