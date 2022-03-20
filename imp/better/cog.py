from __future__ import annotations
from discord.ext.commands import Cog

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from imp.better import BetterBot

class BetterCog(Cog):
    def __init__(
            self,
            client: BetterBot
    ):
        self.client: BetterBot = client
