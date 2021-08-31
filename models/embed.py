from utils.log import log
import discord
from utils import exceptions

from models.provider import Provider


class Embed():
    def __init__(self, author: str, command: str, image: str, provider: Provider) -> None:
        log("Creating a new Embed message")
        self.author = str(author)
        self.command = str(command)
        self.image = str(image)
        if not isinstance(provider, Provider):
            message = "The given provider is an instance of {instance} and should be a models.provider.Provider".format(
                instance=provider.__class__.__name__)
            raise exceptions.WrongProvider(message)
        self.provider = provider
        discord.Embed(title="", description='Command: `.gifrandom`',
                      colour=discord.Colour.blue())

    def dump(self):
        embed = discord.Embed(
            title='From {}'.format(self.author),
            description="Command: `{command}`".format(command=self.command),
            colour=discord.Colour.blue()
        )
        embed.set_image(url=self.image)
        embed.set_footer(icon_url=self.provider.logo, text="Powered by {provider}".format(
            provider=self.provider.provider.title()))
        return embed

    def as_dict(self):
        return {
            "author": self.author,
            "command": self.command,
            "image": self.image,
            "provider": self.provider.as_dict()
        }
