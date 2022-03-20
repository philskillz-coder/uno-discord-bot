from imp.better import BetterInteraction
from discord import app_commands
from imp.better import errors


def IsHost(message: str = None):
    message = message or "You must be a game host for this."

    async def predicate(interaction: BetterInteraction):
        fulfilled = interaction.client.game_manager.is_host(interaction.user)

        if not fulfilled:
            await interaction.response.send_message(
                content=message,
                ephemeral=True
            )
            raise errors.HostCheckError(message)

        return True

    return app_commands.check(predicate)

def IsNotHost(message: str = None):
    message = message or "You mustn't be a game host for this."

    async def predicate(interaction: BetterInteraction):
        fulfilled = not interaction.client.game_manager.is_host(interaction.user)

        if not fulfilled:
            await interaction.response.send_message(
                content=message,
                ephemeral=True
            )
            raise errors.HostCheckError(message)

        return True

    return app_commands.check(predicate)


def IsParticipant(message: str = None):
    message = message or "You must participate in a game for this."

    async def predicate(interaction: BetterInteraction):
        fulfilled = interaction.client.game_manager.is_player(interaction.user)

        if not fulfilled:
            await interaction.response.send_message(
                content=message,
                ephemeral=True
            )
            raise errors.ParticipantCheckError(message)

        return True

    return app_commands.check(predicate)

def IsNotParticipant(message: str = None):
    message = message or "You mustn't participate in a game for this."

    async def predicate(interaction: BetterInteraction):
        fulfilled = not interaction.client.game_manager.is_player(interaction.user)

        if not fulfilled:
            await interaction.response.send_message(
                content=message,
                ephemeral=True
            )
            raise errors.ParticipantCheckError(message)

        return True

    return app_commands.check(predicate)


def GameStarted(message: str = None):
    message = message or "The game must be started for this."

    async def predicate(interaction: BetterInteraction):
        fulfilled = interaction.client.game_manager.get_player_game(interaction.user).started

        if not fulfilled:
            await interaction.response.send_message(
                content=message,
                ephemeral=True
            )
            raise errors.GameCheckError(message)

        return True

    return app_commands.check(predicate)

def GameNotStarted(message: str = None):
    message = message or "The game mustn't be started for this."

    async def predicate(interaction: BetterInteraction):
        fulfilled = not interaction.client.game_manager.get_player_game(interaction.user).started

        if not fulfilled:
            await interaction.response.send_message(
                content=message,
                ephemeral=True
            )
            raise errors.GameCheckError(message)

        return True

    return app_commands.check(predicate)


def PlayerTurn(message: str = None):
    message = message or "It's not your turn!"

    async def predicate(interaction: BetterInteraction):
        game = interaction.client.game_manager.get_player_game(interaction.user)
        fulfilled = game.is_turn(game.get_participant(interaction.user))

        if not fulfilled:
            await interaction.response.send_message(
                content=message,
                ephemeral=True
            )
            raise errors.PlayerTurnCheckError(message)

        return True

    return app_commands.check(predicate)
