from imp import better, data
from cogs.uno import Uno
from imp.game.classes import GameManager


class Bot(better.BetterBot):
    async def startup(self):
        await self.wait_until_ready()
        await self.tree.sync(guild=self.config.guilds[0])
        await self.tree.sync(guild=self.config.guilds[1])

        print("Sucessfully synced applications commands")
        print(f"Connected as {self.user}")

    async def setup_hook(self) -> None:
        self.loop.create_task(self.startup())


bot = Bot("OASD/T")

bot.game_manager = GameManager(bot)
bot.tree.add_command(Uno(bot), guilds=bot.config.guilds)

bot.run(data.Config.token)
