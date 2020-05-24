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


class ViuCrawler(Crawler):
    """Viu Crawler."""
    _API_URL = 'https://www.viu.com/ott/%s/index.php'  # https://github.com/hklcf/ViuTV-API/blob/master/ott/API#L3
    _CRAWLER_ID = 'viu'

    def crawl(self, args) -> tuple:
        """Crawl series on Viu.

        :param args: arguments
        :return: source and episode records
        :rtype: tuple
        """
        output_episodes = []
        output_source = None
        try:
            country_code, video_id = re.search(SITE_URL_PATTERN[self._CRAWLER_ID], args.url).groups()
            payload = {
                'r': 'vod/ajax-detail',
                'platform_flag_label': 'web',
                'product_id': video_id,
            }
            response = requests.get(url=self._API_URL % country_code, headers=HTTP_HEADERS, params=payload)
            data = response.json()
            # Gather subject information
            series = data['data']['series']
            service_id = '%s_%s' % (SITE_SERVICE_ID[self._CRAWLER_ID], country_code)
            # Reset counters
            count = 0
            free_count = 0
            series['product'].sort(key=lambda episode: int(episode['product_id']))
            for episode in series['product']:
                # Gather episode information
                episode_id = get_episode_id(count, args.episodes)
                # Build episode record
                output_episodes.append(Episode(
                    subject_id=args.subject,
                    episode_id=episode_id,
                    service_id=service_id,
                    episode_url_id=episode['product_id'],
                    remark='EP%s-Viu%s' % (episode['number'], country_code.upper()),
                ))
                # Update counters
                count += 1
                if episode['free_time'] == 0:
                    free_count += 1
            # Check consistency of the number of episodes
            if count != len(args.episodes):
                log.warning('Episodes mismatch')
            # Gather subject information
            paid = get_paid_status(count, free_count)
            # Build source record
            output_source = Source(
                subject_id=args.subject,
                service_id=service_id,
                paid=paid,
                subject_url_id=video_id,
                subtitle_locales=['zh_%s' % country_code.upper()],
                remark='%s-Viu%s' % (series['name'], country_code.upper()),
            )
        except (KeyError, ValueError):
            print(traceback.format_exc())
        return output_source, output_episodes
