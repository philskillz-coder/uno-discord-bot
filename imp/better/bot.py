from __future__ import annotations
from discord.ext.commands import Bot
from imp.data.config import Config

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from imp.game.classes import GameManager

class BetterBot(Bot):
    config: Config = Config
    game_manager: GameManager
