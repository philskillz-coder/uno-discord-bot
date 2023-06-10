from typing import List

import discord
from discord import Member

from imp.better import BetterView, BetterBot, BetterButton, BetterInteraction, CheckValue


class StartGame(BetterButton):
    def __init__(self, client: BetterBot, host: Member):
        super().__init__(
            style=discord.ButtonStyle.green,
            label="Start",
            emoji="\U00002705"
        )
        self.client = client
        self.host = host

    async def check(self, interaction: BetterInteraction) -> CheckValue:
        return self.cv(failed=interaction.user != self.host)

    async def on_fail(self, interaction: BetterInteraction, check_value: CheckValue):
        await interaction.response.send_message(
            content="You are not the host of this game!",
            ephemeral=True
        )

    async def on_click(self, interaction: BetterInteraction, check_value: CheckValue):
        game = await self.client.game_manager.start_game(self.host)

        await interaction.response.send_message(
            content="You started your UNO-Game!",
            ephemeral=True
        )


class StopGame(BetterButton):
    def __init__(self, client: BetterBot, host: Member):
        super().__init__(
            style=discord.ButtonStyle.red,
            label="Stop",
            emoji="\U0000274c"
        )
        self.client = client
        self.host = host

    async def check(self, interaction: BetterInteraction) -> CheckValue:
        return self.cv(failed=interaction.user != self.host)

    async def on_fail(self, interaction: BetterInteraction, check_value: CheckValue):
        await interaction.response.send_message(
            content="You are not the host of this game!",
            ephemeral=True
        )

    async def on_click(self, interaction: BetterInteraction, check_value: CheckValue):
        game = await self.client.game_manager.stop_game(self.host)

        await interaction.response.send_message(
            content="You stopped your UNO-Game!",
            ephemeral=True
        )


class ReportCard(BetterButton):
    def __init__(self, client: BetterBot, host: Member):
        super().__init__(
            style=discord.ButtonStyle.secondary,
            label="Report placed card",
            emoji="\U00002757"
        )
        self.client = client
        self.host = host

    async def check(self, interaction: BetterInteraction) -> CheckValue:
        return self.cv(failed=not self.client.game_manager.get_game(self.host).has_participant(interaction.user))

    async def on_fail(self, interaction: BetterInteraction, check_value: CheckValue):
        await interaction.response.send_message(
            content="You are not participating in this game!",
            ephemeral=True
        )

    async def on_click(self, interaction: BetterInteraction, check_value: CheckValue):
        card = await self.client.game_manager.report_card(
            self.client.game_manager.get_game(self.host).get_participant(interaction.user))

        await interaction.response.send_message(
            content=f"You reported {card.placer.user.mention}'s card.",
            ephemeral=True
        )


class DrawCard(BetterButton):
    def __init__(self, client: BetterBot, host: Member):
        super().__init__(
            style=discord.ButtonStyle.secondary,
            label="Take a card",
            emoji="\U0001f90f"
        )
        self.client = client
        self.host = host

    async def check(self, interaction: BetterInteraction) -> CheckValue:
        game = self.client.game_manager.get_game(self.host)
        has_participant = game.has_participant(interaction.user)

        if has_participant:
            participant = game.get_participant(interaction.user)
            is_turn = game.is_turn(participant)
            took_card = participant.took_card

        else:
            is_turn = False
            took_card = False

        print(f"{has_participant=} {is_turn=} {took_card=}")

        return self.cv(
            (has_participant, is_turn, took_card),
            not (has_participant and is_turn and not took_card)
        )

    async def on_fail(self, interaction: BetterInteraction, check_value: CheckValue):
        if not check_value.value[0]:
            return await interaction.response.send_message(
                content="You are not participating in this game!",
                ephemeral=True
            )

        if not check_value.value[1]:
            return await interaction.response.send_message(
                content="It's not your turn.",
                ephemeral=True
            )

        if check_value.value[2]:
            return await interaction.response.send_message(
                content="You already took a card!",
                ephemeral=True
            )

    async def on_click(self, interaction: BetterInteraction, check_value: CheckValue):
        game = self.client.game_manager.get_player_game(interaction.user)
        participant = game.get_participant(interaction.user)

        card = await self.client.game_manager.draw_card(game, participant)

        await interaction.response.send_message(
            content=f"You took a card and got {card.name}",
            ephemeral=True
        )

class SkipMe(BetterButton):
    def __init__(self, client: BetterBot, host: Member):
        super().__init__(
            style=discord.ButtonStyle.secondary,
            label="Skip me",
            emoji="\U000023e9"
        )
        self.client = client
        self.host = host

    async def check(self, interaction: BetterInteraction) -> CheckValue:
        game = self.client.game_manager.get_game(self.host)
        has_participant = game.has_participant(interaction.user)

        if has_participant:
            participant = game.get_participant(interaction.user)
            is_turn = game.is_turn(participant)
            took_card = participant.took_card

        else:
            is_turn = False
            took_card = False

        print(f"{has_participant=} {is_turn=} {took_card=}")
        return self.cv(
            (has_participant, is_turn, took_card),
            not (has_participant and is_turn and took_card)
        )

    async def on_fail(self, interaction: BetterInteraction, check_value: CheckValue):
        if not check_value.value[0]:
            return await interaction.response.send_message(
                content="You are not participating in this game!",
                ephemeral=True
            )

        if not check_value.value[1]:
            return await interaction.response.send_message(
                content="It's not your turn.",
                ephemeral=True
            )

        if not check_value.value[2]:
            return await interaction.response.send_message(
                content="You must take a card before you skip!",
                ephemeral=True
            )

    async def on_click(self, interaction: BetterInteraction, check_value: CheckValue):
        game = self.client.game_manager.get_player_game(interaction.user)
        participant = game.get_participant(interaction.user)

        await self.client.game_manager.skip_participant(game)

        await interaction.response.send_message(content="You skipped.", ephemeral=True)


class GameInitView(BetterView):
    def __add__button__(self, button: BetterButton):
        self.__buttons.append(button)

    def __init__buttons__(self):
        for b in self.__buttons:
            b.__init__button__(self)

        for b in self.__buttons:
            self.add_item(b)

    def __init__(self, client: BetterBot, host: Member):
        super().__init__(client)
        self.host = host
        self.__buttons: List[BetterButton] = []

        self.__start_button = StartGame(client, host)
        self.__stop_button = StopGame(client, host)

        self.__add__button__(self.__start_button)
        self.__add__button__(self.__stop_button)

        self.__init__buttons__()


class GameView(BetterView):
    def __add__button__(self, button: BetterButton):
        self.__buttons.append(button)

    def __init__buttons__(self):
        for b in self.__buttons:
            b.__init__button__(self)

        for b in self.__buttons:
            self.add_item(b)

    def __init__(self, client: BetterBot, host: Member):
        super().__init__(client)
        self.host = host
        self.__buttons: List[BetterButton] = []

        self.__stop_button = StopGame(client, host)
        self.__report_button = ReportCard(client, host)
        self.__draw_button = DrawCard(client, host)
        self.__skip_button = SkipMe(client, host)

        self.__add__button__(self.__stop_button)
        self.__add__button__(self.__report_button)
        self.__add__button__(self.__draw_button)
        self.__add__button__(self.__skip_button)

        self.__init__buttons__()


class GameStopView(BetterView):
    pass
