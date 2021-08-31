from utils import exceptions
from random import choice
from models.provider import Provider, Giphy, Tenor


class Results():
    def __init__(self, query: str, results, provider: Provider, random: bool = False) -> None:
        self.query = str(query)
        self.is_random = bool(random) # either a bool or an int

        if not isinstance(provider, Provider):
            message = "The given provider is an instance of {instance} and should be a models.provider.Provider".format(
                instance=provider.__class__.__name__)
            raise exceptions.WrongProvider(message)
        if isinstance(provider, Giphy):
            if self.is_random:
                results = [results['data'].get('images', {}).get('original', {}).get('url', None)]
            else:    
                results = [response.get('images', {}).get('original', {}).get('url', None) for response in results['data']]
            self.results = list(set([str(response) for response in results if response is not None]))
        elif isinstance(provider, Tenor):
            results = [response.get('media', [])[0].get('gif', {}).get('url', None) for response in results['results'] if len(response['media']) > 0]
            self.results = list(set([str(response) for response in results if response is not None]))
        elif isinstance(results, (list, tuple, set)):
            self.results = list(set([str(response) for response in results if response is not None]))
        else:
            message = "The given provider {instance} is not supported by EasyGif for now".format(
                instance=provider.__class__.__name__)
            raise exceptions.WrongProvider(message)

    @property
    def random(self):
        return choice(self.results)