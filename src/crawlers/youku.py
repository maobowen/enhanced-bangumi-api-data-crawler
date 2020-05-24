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


class YoukuCrawler(Crawler):
    """Youku Crawler."""
    _API_URL = 'https://openapi.youku.com/v2/shows/videos.json'  # https://github.com/bangumi-data/helper/blob/master/lib/crawlers/youku.js#L91
    _CRAWLER_ID = 'youku'

    def crawl(self, args) -> tuple:
        """Crawl series on Youku.

        :param args: arguments
        :return: source and episode records
        :rtype: tuple
        """
        output_episodes = []
        output_source = None
        try:
            # Initiate API request
            show_id = re.search(SITE_URL_PATTERN[self._CRAWLER_ID], args.url).group(1)
            payload = {
                'client_id': 'f8c97cdf52e7a346',
                'count': 100,
                'show_id': show_id,
            }
            response = requests.get(url=self._API_URL, headers=HTTP_HEADERS, params=payload)
            data = response.json()
            if 'error' not in data:
                # Reset counters
                count = 0
                free_count = 0
                for episode in data['videos']:
                    # Gather episode information
                    episode_id = get_episode_id(count, args.episodes)
                    # Build episode record
                    output_episodes.append(Episode(
                        subject_id=args.subject,
                        episode_id=episode_id,
                        service_id=SITE_SERVICE_ID[self._CRAWLER_ID],
                        episode_url_id=episode['id'],
                        remark='EP%s-优酷' % episode['stage'],
                    ))
                    # Update counters
                    count += 1
                    if episode['paid'] == 0:
                        free_count += 1
                # Check consistency of the number of episodes
                if len(data['videos']) != len(args.episodes):
                    log.warning('Episodes mismatch')
                # Gather subject information
                paid = get_paid_status(count, free_count)
                # Build source record
                output_source = Source(
                    subject_id=args.subject,
                    service_id=SITE_SERVICE_ID[self._CRAWLER_ID],
                    paid=paid,
                    subject_url_id=show_id,
                    subtitle_locales=['zh_CN'],
                    remark='<名称>-优酷',
                )
        except (KeyError, ValueError):
            print(traceback.format_exc())
        return output_source, output_episodes
