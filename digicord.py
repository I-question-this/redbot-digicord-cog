import discord
import logging

from redbot.core import checks, commands, Config
from redbot.core.data_manager import cog_data_path
from redbot.core.bot import Red

log = logging.getLogger("red.digicord")

class Digicord(commands.Cog):
    """Digicord cog"""

    def __init__(self, bot: Red):
        super().__init__()
        self.bot = bot

