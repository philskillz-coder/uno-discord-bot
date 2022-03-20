from __future__ import annotations

from discord import app_commands
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from imp.better import BetterBot

class BetterAppCommandGroup(app_commands.Group):
    def __init__(
            self,
            client: BetterBot
    ):
        super().__init__()
        self.client: BetterBot = client
