from __future__ import annotations

from discord.ui import View
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from imp.better import BetterBot

class BetterView(View):
    def __init__(
            self,
            client: BetterBot,
            timeout: Optional[int] = None
    ):
        super().__init__(timeout=timeout)
        self.client: BetterBot = client
