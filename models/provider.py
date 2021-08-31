from utils.log import log
from config import ASSETS_DOMAIN


class Provider():
    def __init__(self, provider, logo) -> None:
        log("Creating a new Provider")
        self.provider = str(provider).lower()
        self.logo = str(logo)

    def as_dict(self):
        return {
            "provider": self.provider,
            "logo": self.logo
        }


class Giphy(Provider):
    def __init__(self) -> None:
        super().__init__("Giphy",
                         "{domain}/assets/public/logos/giphy/giphy-logo.png".format(domain=ASSETS_DOMAIN))


class Tenor(Provider):
    def __init__(self) -> None:
        super().__init__("Tenor",
                         "{domain}/assets/public/logos/tenor/tenor-logo.png".format(domain=ASSETS_DOMAIN))
