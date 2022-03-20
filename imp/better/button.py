from __future__ import annotations
from discord.ui import Button
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from imp.better.interaction import BetterInteraction

class CheckValue:
    def __init__(self, value: Any = None, failed: bool = False):
        self.value = value
        self.failed = failed

class BetterButton(Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = None

    @staticmethod
    def cv(value: Any = None, failed: bool = False):
        return CheckValue(value, failed)

    async def check(self, interaction: BetterInteraction) -> CheckValue:
        return self.cv()

    async def on_click(self, interaction: BetterInteraction, check_value: CheckValue):
        pass

    async def on_fail(self, interaction: BetterInteraction, check_value: CheckValue):
        pass

    async def callback(self, interaction: BetterInteraction):
        check = await self.check(interaction)
        if check.failed:
            return await self.on_fail(interaction, check)

        return await self.on_click(interaction, check)

    def __init__button__(self, parent):
        self.parent = parent
