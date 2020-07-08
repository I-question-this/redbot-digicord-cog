from .digicord import Digicord

def setup(bot):
    bot.add_cog(Digicord(bot))

