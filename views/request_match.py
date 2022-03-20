from discord import ui, Member
from discord import ButtonStyle, Interaction, InteractionResponse

from imp.better import BetterView, BetterBot
from typing import Optional

class RequestMatch(BetterView):
    def __init__(
        self,
        client: BetterBot,
        requester: Member,
        target: Member,
    ):
        super().__init__(client, 30)
        self.requester: Member = requester
        self.target: Member = target
        self.accepted: Optional[bool] = None
        self.canceled: bool = False

    def cancel_invite(self):
        self.canceled = True

    @ui.button(
        label="Join",
        style=ButtonStyle.green,
        emoji="\U00002705"
    )
    async def accept_request(
            self,
            button: ui.Button,
            interaction: Interaction
    ):
        if isinstance(interaction.response, InteractionResponse):
            if self.canceled:
                return await interaction.response.send_message(
                    content="Your invite got canceled!",
                    ephemeral=True
                )

            await interaction.response.send_message(
                f"You joined {self.requester.mention}'s UNO-Game",
                ephemeral=True
            )

        await interaction.message.delete()
        self.accepted = True
        self.stop()

    async def interaction_check(
        self,
        interaction: Interaction
    ) -> bool:
        return interaction.user == self.target

    @ui.button(
        label="Don't Join",
        style=ButtonStyle.red,
        emoji="\U0000274c"
    )
    async def decline_request(
        self,
        button: ui.Button,
        interaction: Interaction
    ):
        if isinstance(interaction.response, InteractionResponse):
            if self.canceled:
                return await interaction.response.send_message(
                    content="Your invite got canceled!",
                    ephemeral=True
                )

            await interaction.response.send_message(
                f"You did not join {self.requester.mention}'s UNO-Game",
                ephemeral=True
            )

        await interaction.message.delete()
        self.accepted = False
        self.stop()
