from typing import List

import discord
from discord import app_commands, Member

from imp.better import BetterBot, BetterAppCommandGroup, BetterInteraction
from imp.game import checks
from imp.game.classes import Participant, UNOGame, Card, CardTransformer
from views.request_match import RequestMatch


class Uno(BetterAppCommandGroup):
    def __init__(self, client: BetterBot):
        super().__init__(client)

    @app_commands.command(
        name="create_game",
        description="Create a new UNO-Game"
    )
    @checks.IsNotHost()
    @checks.IsNotParticipant()
    async def create_match(
            self,
            interaction: BetterInteraction
    ):
        message = await interaction.channel.send(
            embed=discord.Embed(
                title="UNO-Game",
                colour=discord.Colour.orange()
            )
        )

        await self.client.game_manager.create_game(interaction.user, message)
        await interaction.response.send_message(
            content="You created a UNO-Game! Invite players with `/uno invite_player`",
            ephemeral=True
        )


    @app_commands.command(
        name="turn_order",
        description="Show the turn order of your game"
    )
    @checks.IsParticipant()
    async def turn_order(
        self,
        interaction: BetterInteraction
    ):
        game: UNOGame = self.client.game_manager.get_player_game(interaction.user)
        return await interaction.response.send_message(
            content=f"Turn order:\n{game.turn_order()}",
            ephemeral=True
        )


    @app_commands.command(
        name="invite_player",
        description="Invite a player into your game."
    )
    @app_commands.describe(
        user="The user you want to invite"
    )
    @checks.IsHost()
    async def invite_player(
        self,
        interaction: BetterInteraction,
        user: Member
    ):
        if interaction.user == user:  # user inviting itself
            return await interaction.response.send_message(
                content="You can't invite yourself to this UNO-Game!",
                ephemeral=True
            )

        if user.bot:  # user inviting a bot
            return await interaction.response.send_message(
                content="You can't invite a bot to this UNO-Game",
                ephemeral=True
            )

        if self.client.game_manager.is_player(user):
            return await interaction.response.send_message(
                content="This player is already participating in a other game!",
                ephemeral=True
            )

        game: UNOGame = self.client.game_manager.get_game(interaction.user)
        if game.is_pending_invite(user):
            return await interaction.response.send_message(
                content="This player already has a invite. You must wait for him to confirm/decline",
                ephemeral=True
            )

        await interaction.response.defer(ephemeral=True, thinking=True)

        if isinstance(interaction.channel, discord.TextChannel):
            match_request = RequestMatch(self.client, interaction.user, user)
            game.add_pending_invite(user, match_request)

            await interaction.channel.send(
                content=f"Hey {user.mention}, {interaction.user.mention} wants to participate in his UNO-Game!\nClick the buttons below to accept/decline.",
                view=match_request
            )

            await match_request.wait()

            # noinspection PyTypeChecker
            wh: discord.Webhook = interaction.followup
            if match_request.canceled:
                self.client.game_manager.set_game(interaction.user, game)
                return await wh.send(
                    content="Invite canceled!",
                    ephemeral=True
                )

            game.remove_pending_invite(user)

            if match_request.accepted is None:
                await interaction.message.delete()
                self.client.game_manager.set_game(interaction.user, game)
                return await wh.send(
                    content=f"Hey {interaction.user.mention}, {user.mention} didn't respond in time. Maybe he's afk :/",
                    ephemeral=True
                )

            if not match_request.accepted:
                self.client.game_manager.set_game(interaction.user, game)
                return await wh.send(
                    content=f"Hey {interaction.user.mention}, {user.mention} didn't want to participate in your UNO-Game :/",
                    ephemeral=True
                )

            await wh.send(
                content=f"Hey {interaction.user.mention}, {user.mention} is now participating in your UNO-Game!",
                ephemeral=True
            )

            game.add_participant(Participant.from_user(user))
            await game.update_message(
                show_turn=False,
                show_top_card=False,
                show_stats=False
            )
            self.client.game_manager.set_game(interaction.user, game)


    @app_commands.command(
        name="cancel_invite",
        description="Cancel a invite for a player."
    )
    @app_commands.describe(
        player="The player you want to cancel invite"
    )
    @checks.IsHost()
    async def cancel_invite(
        self,
        interaction: BetterInteraction,
        player: Member
    ):
        game: UNOGame = self.client.game_manager.get_game(interaction.user)
        if not game.is_pending_invite(player):
            return await interaction.response.send_message(
                content="This player has no pending invite.",
                ephemeral=True
            )

        game.remove_pending_invite(player, cancel=True)
        await interaction.response.send_message(
            content=f"Canceled {player.mention}'s Invite to your UNO-Game!",
            ephemeral=True
        )


    @app_commands.command(
        name="kick_player",
        description="Kick a player from your UNO-Game"
    )
    @app_commands.describe(
        player="The player you want to kick"
    )
    @checks.IsHost()
    @checks.GameNotStarted()
    async def kick_player(
        self,
        interaction: BetterInteraction,
        player: Member
    ):
        game: UNOGame = self.client.game_manager.get_game(interaction.user)
        if game.started:
            return await interaction.response.send_message(
                content="The game has already started. You can only vote kick now. (`/uno vote_kick`)",
                ephemeral=True
            )

        if not game.has_participant(player):
            return await interaction.response.send_message(
                content="This user is not participating in this UNO-Game.",
                ephemeral=True
            )

        game.remove_participant(game.get_participant(player))
        self.client.game_manager.set_game(interaction.user, game)

        await interaction.response.send_message(
            content=f"You kicked {player.mention} out of this UNO-Game!",
            ephemeral=True
        )


    @app_commands.command(
        name="list_participants",
        description="List the participants in your game."
    )
    @checks.IsParticipant()
    async def list_participants(
        self,
        interaction: BetterInteraction
    ):
        game: UNOGame = self.client.game_manager.get_player_game(interaction.user)
        _participants = [participant.mention for participant in game.participants if participant != interaction.user]

        if not _participants:
            return await interaction.response.send_message(
                content="No other users are participating in your UNO-Game!",
                ephemeral=True
            )

        participants = "\n".join(_participants)
        await interaction.response.send_message(
            content=f"{len(_participants)} other users are participating in your UNO-Game: \n{participants}",
            ephemeral=True
        )


    @app_commands.command(
        name="deck",
        description="Show your card deck"
    )
    @checks.IsParticipant()
    @checks.GameStarted()
    async def card_deck(
        self,
        interaction: BetterInteraction
    ):
        game: UNOGame = self.client.game_manager.get_player_game(interaction.user)
        participant = game.get_participant(interaction.user)
        cards = participant.stack.cards

        return await interaction.response.send_message(
            content="Your cards:\n" + "\n".join(card.name for card in cards),
            ephemeral=True
        )


    @app_commands.command(
        name="place_card",
        description="Place a card onto the stack"
    )
    @app_commands.describe(
        card="The card you want to place"
    )
    @checks.IsParticipant()
    @checks.GameStarted()
    @checks.PlayerTurn()
    async def place_card(
        self,
        interaction: BetterInteraction,
        card: app_commands.Transform[Card, CardTransformer]
    ):
        game = self.client.game_manager.get_player_game(interaction.user)
        participant = game.get_participant(interaction.user)

        if card is None:
            return

        await self.client.game_manager.place_card(game, game.get_participant(interaction.user), card)

        if participant.has_no_cards():
            await interaction.response.send_message(
                content="You won the game!",
                ephemeral=True
            )

            return await self.client.game_manager.stop_game(game.host, won=participant)

        await interaction.response.send_message(
            content=f"You placed a **{card.name}**",
            ephemeral=True
        )

    @place_card.autocomplete(name="card")
    async def autocomplete(
        self,
        interaction: BetterInteraction,
        value: str,
    ) -> List[app_commands.Choice[str]]:
        if not self.client.game_manager.is_player(interaction.user):
            return []

        game = self.client.game_manager.get_player_game(interaction.user)
        participant = game.get_participant(interaction.user)

        return [
            app_commands.Choice(name=card.name, value=card.name)
            for card in participant.stack.cards if value.lower() in card.name.lower()
        ]
