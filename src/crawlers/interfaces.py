from abc import *


class Crawler(ABC):
    """Crawler interface."""
    @property
    @classmethod
    @abstractmethod
    def _CRAWLER_ID(cls):
        """Crawler ID."""
        raise NotImplementedError

    @abstractmethod
    def crawl(self, args):
        """Crawl series.

        :param args:
        :return:
        """
        raise NotImplementedError
