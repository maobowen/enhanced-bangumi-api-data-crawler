from bs4 import BeautifulSoup
import logging
import re
import requests
import traceback

from .common import *
from .interfaces import Crawler
from ..consts import *
from ..models.episode import Episode
from ..models.source import Source

log = logging.getLogger(__name__)


class AnimadCrawler(Crawler):
    """Animad Crawler."""
    _CRAWLER_ID = 'animad'

    def crawl(self, args) -> tuple:
        """Crawl series on Animad.

        :param args: arguments
        :return: source and episode records
        :rtype: tuple
        """
        output_episodes = []
        output_source = None
        try:
            # Initiate HTTP requests
            response1 = requests.get(url=args.url, headers=HTTP_HEADERS)
            soup = BeautifulSoup(response1.content, 'html.parser')
            subject_name = soup.select('div.ACG-mster_box1 h1')[0].decode_contents()
            episode1_url = 'https:%s' % (soup.select('div.ACG-list5 div.seasonACG ul li a')[0].get('href'))
            response2 = requests.get(url=episode1_url, headers=HTTP_HEADERS)
            soup = BeautifulSoup(response2.content, 'html.parser')
            # Reset counters
            count = 0
            for episodeDOM in soup.select('div.anime-option section.season ul li'):
                # Gather episode information
                episode_id = get_episode_id(count, args.episodes)
                episode_url = episodeDOM.select('a')[0].get('href')
                episode_url_id = re.search(r'sn=(\d+)', episode_url).group(1)
                episode_index = episodeDOM.select('a')[0].decode_contents()
                # Build episode record
                output_episodes.append(Episode(
                    subject_id=args.subject,
                    episode_id=episode_id,
                    service_id=SITE_SERVICE_ID[self._CRAWLER_ID],
                    episode_url_id=episode_url_id,
                    remark='EP%s-动画疯' % episode_index,
                ))
                # Update counters
                count += 1
            # Check consistency of the number of episodes
            if count != len(args.episodes):
                log.warning('Episodes mismatch')
            # Gather subject information
            subject_url_id = re.search(SITE_URL_PATTERN[self._CRAWLER_ID], args.url).group(1)
            # Build source record
            output_source = Source(
                subject_id=args.subject,
                service_id=SITE_SERVICE_ID[self._CRAWLER_ID],
                paid=0,
                subject_url_id=subject_url_id,
                subtitle_locales=['zh_HK'],
                remark='%s-动画疯' % subject_name,
            )
        except (KeyError, ValueError):
            print(traceback.format_exc())
        return output_source, output_episodes
