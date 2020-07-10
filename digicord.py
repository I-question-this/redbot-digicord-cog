import discord
import logging
import os
import random
random.seed()
from redbot.core import checks, commands, Config
from redbot.core.data_manager import cog_data_path
from redbot.core.bot import Red
import shutil

log = logging.getLogger("red.digicord")
_DEFAULT_GUILD = {
    "spawn_channel": None
}

# Determine image folder locations
FILE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(FILE_DIR, "images")
SPRITES_DIR = os.path.join(IMAGES_DIR, "sprites")
FIELD_DIR = os.path.join(IMAGES_DIR, "field")

def sprite_path(digimon_number:int) -> str:
    """Returns the file path for the sprite given a Digimon number.
    Parameters
    ----------
    digimon_number: int
        The number to get the sprite image for.
    Returns
    -------
        The file path for the sprite image.
    """
    return os.path.join(SPRITES_DIR, f"{digimon_number}.png")


def field_path(digimon_number:int):
    """Returns the file path for the field image given a Digimon number.
    Parameters
    ----------
    digimon_number: int
        The number to get the field image for.
    Returns
    -------
        The file path for the field image.
    """
    return os.path.join(FIELD_DIR, f"{digimon_number}.png")


class Digicord(commands.Cog):
    """Digicord cog"""

    def __init__(self, bot:Red):
            super().__init__()
            self.bot = bot
            self._conf = Config.get_conf(None, 90210, cog_name=f"{self.__class__.__name__}", force_registration=True)
            self._conf.register_guild(**_DEFAULT_GUILD)


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
        # Get proper spawn channel
        channel_id = await self._conf.guild(channel.guild).spawn_channel()
        if channel_id is not None:
            channel = self.bot.get_channel(channel_id)

        # Send the data
        contents = dict(
                title="A Wild Digimon has Appeared!",
                description="Not really, but maybe in the future!"
                )
        embed = discord.Embed.from_dict(contents)
        await channel.send(embed=embed)


    @commands.guild_only()
    @commands.admin()
    @commands.command(name="set_spawn_channel")
    async def set_spawn_channel(self, ctx: commands.Context, channel:discord.TextChannel):
        """Sets which channel the bot spawns Digimon in.
        Parameters
        ----------
        channel: discord.TextChannel
            The channel that digimon will appear in.
        """
        await self._conf.guild(ctx.guild).spawn_channel.set(channel.id)

        contents = dict(
            title="Set Spawn Channel: Success",
            description=f"Spawn channel set to {channel.name}"
            )
        embed = discord.Embed.from_dict(contents)
        await ctx.send(embed=embed)

