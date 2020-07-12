import discord
import logging
import os
import random
random.seed()
from redbot.core import checks, commands, Config
from redbot.core.data_manager import cog_data_path
from redbot.core.bot import Red
import shutil

from .database import Database
from .digimon import Individual, Species


LOG = logging.getLogger("red.digicord")

_DEFAULT_GLOBAL = {
    "spawn_chance": 1
    }
_DEFAULT_GUILD = {
    "spawn_channel": None,
    "current_digimon": None
}
_DEFAULT_USER = {
    "digimon": {},
    "selected_digimon": None
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
    str:
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
    str:
        The file path for the field image.
    """
    return os.path.join(FIELD_DIR, f"{digimon_number}.png")



class UnknownDigimonIdNumber(Exception):
    def __init__(self, user:discord.User, id_number:int):
        self.id_number = id_number

    def __str__(self):
        return f"Unknown Digimon id number {self.id_number} " \
                f"for user {user.id}"



class Digicord(commands.Cog):
    """Digicord cog"""

    def __init__(self, bot:Red):
        super().__init__()
        self.bot = bot
        self._conf = Config.get_conf(None, 90210, cog_name=f"{self.__class__.__name__}", force_registration=True)
        self._conf.register_global(**_DEFAULT_GLOBAL)
        self._conf.register_guild(**_DEFAULT_GUILD)
        self._conf.register_user(**_DEFAULT_USER)
        self.database = Database("")


    async def _embed_msg(self, ctx: commands.Context, title:str,
            description:str, file:discord.File=None) -> None:
        """Assemble and send an embedded message.
        Parameters
        ----------
        title: str
            Title of the embedded image
        description: str
            Description of the embed
        file: discord.File
            File object to embed within the message.
            This is optional.
        """
        # Assemble the contents of the message
        contents = dict(
                title=title, 
                type="rich", 
                description=description
            )
        embed = discord.Embed.from_dict(contents)
        # Attach file if it exists
        if file is not None:
            embed.set_image(url=f"attachment://{file.filename}")
        # Send the message
        await ctx.send(embed=embed, file=file)



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
        if random.randrange(0,100) < await self._conf.spawn_chance():
            await self.spawn_digimon(message.channel)


    async def spawn_digimon(self, channel:discord.TextChannel):
        """Spawns a random Digimon.
        Parameters
        ----------
        channel: discord.TextChannel
            The channel that the random Digimon will appear in.
        """
        # Get proper spawn channel
        channel_id = await self._conf.guild(channel.guild).spawn_channel()
        if channel_id is not None:
            channel = self.bot.get_channel(channel_id)

        # Randomly select a Digimon
        d = self.database.random_digimon()

        # Save this digimon's existence so it can be caught
        await self._conf.guild(channel.guild).current_digimon.set(
                d.to_dict())

        LOG.info(f"Spawned Digimon: \"{d.to_dict()}\" in guild " \
                f"{channel.guild.id}, channel {channel.id}")
        # Send the data
        await self._embed_msg(
                ctx=channel,
                title="A Wild Digimon has Appeared!",
                description="",
                file=discord.File(field_path(d.number))
            )


    @commands.group()
    async def admin(self, ctx: commands.Context) -> None:
        """Admin commands"""


    @commands.guild_only()
    @commands.admin()
    @admin.command(name="set_spawn_channel")
    async def set_spawn_channel(self, ctx: commands.Context, channel:discord.TextChannel=None):
        """Sets which channel the bot spawns Digimon in. If no argument is given 
            then Digimon will spawn in any channel.
        Parameters
        ----------
        channel: discord.TextChannel
            The channel that digimon will appear in.
            The optional is None and will result in the Digimon appearing
            in any channel
        """
        if channel is None:
            await self._conf.guild(ctx.guild).spawn_channel.set(None)
            LOG.info(f"In guild {ctx.guild.id} set spawn channel to: any")
            await self._embed_msg(
                    ctx=ctx,
                    title="Set Spawn Channel: Success",
                    description=f"Spawn channel set to any"
                )
        else:
            await self._conf.guild(ctx.guild).spawn_channel.set(channel.id)
            LOG.info(f"In guild {ctx.guild.id} set spawn channel to: "\
                    f"{channel.id}")
            await self._embed_msg(
                    ctx=ctx,
                    title="Set Spawn Channel: Success",
                    description=f"Spawn channel set to {channel.name}"
                )


    @checks.is_owner()
    @admin.command(name="set_spawn_chance")
    async def set_spawn_chance(self, ctx: commands.Context, spawn_chance:int):
        """Sets the spawn chance.

        Parameters
        ----------
        spawn_chance: int
            Set chance in which a digimon will spawn after a message is sent.
        """
        if 0 < spawn_chance <= 100:
            await self._conf.spawn_chance.set(spawn_chance)
            LOG.info(f"Set spawn chance to {spawn_chance}%")
            title="Set Spawn Chance: Success"
            description=f"Spawn chance set to {spawn_chance}%"
        else:
            title="Set Spawn Chance: Failure"
            description=f"Spawn chance has to be (0,100], which is not {spawn_chance}"
        await self._embed_msg(ctx, title, description)


    @commands.guild_only()
    @commands.is_owner()
    @admin.command(name="spawn_digimon")
    async def command_spawn_digimon(self, ctx: commands.Context):
        """Spawns a random Digimon in the current server.
        """
        await self.spawn_digimon(ctx)


    @commands.group()
    @commands.guild_only()
    async def digimon(self, ctx: commands.Context) -> None:
        """Digimon commands"""


    async def new_id_number(self, user:discord.User) -> int:
        """Returns the next id number to be used for a new Digimon
        
        Parameters
        ----------
        user: discord.User
            The user to return this information for.

        Returns
        -------
        int:
            The new (max+1) id number to be used for a new Digimon
        """
        caught_digimon = await self._conf.user(user).digimon()
        return str(len(caught_digimon) + 1)


    async def register_digimon(self, user:discord.User, digi:Individual):
        """Register a given Digimon to a given user.
        
        Parameters
        ----------
        user: discord.User
            The user to register the Digimon to.
        digi: Individual
            The Individual Digimon to register
        """
        caught_digimon = await self._conf.user(user).digimon()
        new_id = await self.new_id_number(user)
        caught_digimon[new_id] = digi.to_dict()
        await self._conf.user(user).digimon.set(caught_digimon)


    async def get_user_digimon(self, user:discord.User, digimon_id:int)\
        -> (Individual, Species):
        """Register a given Digimon to a given user.
        
        Parameters
        ----------
        user: discord.User
            The user to get the Digimon of.
        digimon_id: int
            The ID number of the Digimon in reference to the User
        Returns
        -------
        Individual:
            The Digimon, at least it's Individual information
        Species:
            The species information of the selected Digimon
        Raises
        ------
        UnknownDigimonIdNumber
           Indicates the given digimon_id does not exist in
           reference to this user.
           This is expect to happen since this function
           will be passed user input. Users of this function
           beware.
        """
        # It's saved as a string in the JSON config file
        digimon_id = str(digimon_id)
        caught_digimon = await self._conf.user(user).digimon()
        ind_info = caught_digimon.get(digimon_id, None)
        if ind_info is None:
            raise UnknownDigimonIdNumber(user, digimon_id)
        else:
            ind = Individual.from_dict(ind_info)
            spec = self.database.species_information(ind.number)
            return ind, spec


    @commands.command(name="catch")
    async def catch(self, ctx: commands.Context, guess: str):
        """Attempt to catch a Digimon via guessing it's name.
        
        Parameters
        ----------
        guess: str
            The guessed name.
        """
        cur = await self._conf.guild(ctx.guild).current_digimon()
        if cur is None:
            # There is no current digimon to be caught
            return
        # Execute to get the current digimon
        cur = Individual.from_dict(cur)
        guess = guess.lower()
        real_name = self.database.species_information(cur.number).name.lower()
        if guess == real_name:
            await self.register_digimon(ctx.author, cur)
            await self._conf.guild(ctx.guild).current_digimon.set(None)
            LOG.info(f"User {ctx.author.id} in guild {ctx.guild.id} "\
                    f"caught Digimon: \"{cur.to_dict()}\"")
            await self._embed_msg(
                    ctx=ctx,
                    title=f"Congratulations!",
                    description=f"{ctx.author.mention} caught a level"\
                            f" {cur.level} {real_name.capitalize()}"
                )


    @digimon.command(name="select")
    async def select(self, ctx: commands.Context, digimon_id:int):
        """Selects a Digimon as the "default" for operations.
        
        Parameters
        ----------
        digimon_id: int
            The id of the Digimon to select.
        """
        try:
            selection = await self.get_user_digimon(ctx.author, digimon_id)
            await self._conf.user(ctx.author).selected_digimon.set(digimon_id)
            log.info(f"{ctx.author.id} selected {digimon_id}")
            title="Selection Successful"
            if selection[0].nickname is not None:
                nickname = selection[0].nickname
            else:
                nickname = selection[1].name
            description=f"{ctx.author.mention}: Selected "\
                    f"{nickname}({selection[1].name})"
            await self._embed_msg(ctx, title, description)
        except UnknownDigimonIdNumber:
            log.error(f"No such id {id} for user {ctx.author.id}")
            title="Selection Failed"
            description=f"{ctx.author.mention}: No such Digimon with that"\
                    " ID exists"
            await self._embed_msg(ctx, title, description)

