import discord
import logging
import random
random.seed()
from redbot.core import checks, commands, Config
from redbot.core.data_manager import cog_data_path
from redbot.core.bot import Red

log = logging.getLogger("red.digicord")


class Digicord(commands.Cog):
    """Digicord cog"""

    def __init__(self, bot:Red):
            super().__init__()
            self.bot = bot


    @commands.Cog.listener()
    async def on_message(self, message:discord.Message):
        # Make sure it's not a bot, ourself, or a DM
        if isinstance(message.channel, discord.abc.PrivateChannel):
            return
        author = message.author
        valid_user = isinstance(author, discord.Member) and not author.bot
        if not valid_user:
            return
        if await self.bot.is_automod_immune(message):
            return

        # Maybe spawn Digimon 
        if random.randrange(0,100) < 10:
            await self.spawn_digimon(message.channel)


    async def spawn_digimon(self, channel:discord.TextChannel):
        contents = dict(
                title="A Wild Digimon has Appeared!",
                description="Not really, but maybe in the future!"
                )
        embed = discord.Embed.from_dict(contents)
        await channel.send(embed=embed)

