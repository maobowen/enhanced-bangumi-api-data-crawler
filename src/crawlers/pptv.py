import json
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


class PPTVCrawler(Crawler):
    """PPTV Crawler."""
    _API_URL = 'http://apis.web.pptv.com/show/videoList'  # https://github.com/bangumi-data/helper/blob/master/lib/crawlers/pptv.js#L52
    _CRAWLER_ID = 'pptv'
    _EPISODE_URL_PATTERN = r'v\.pptv\.com\/show\/(\w+).html'

    def crawl(self, args) -> tuple:
        """Crawl series on PPTV.

        :param args: arguments
        :return: source and episode records
        :rtype: tuple
        """
        output_episodes = []
        output_source = None
        try:
            # Initiate HTTP request
            response = requests.get(url=args.url, headers=HTTP_HEADERS)
            data = json.loads(re.search(r'webcfg\s*=\s*(\{.*\})', response.content.decode()).group(1))  # https://blog.csdn.net/chouzhou9701/article/details/105873321/
            # Gather subject information
            subject_url_id = data['id_encode']
            subject_name = data['title']
            # Initiate API request
            payload = {
                'pid': data['id'],
            }
            response = requests.get(url=self._API_URL, headers=HTTP_HEADERS, params=payload)
            data = response.json()
            if data['err'] == 0:
                # Reset counters
                count = 0
                free_count = 0
                for episode in data['data']['list']:
                    if not episode['isTrailer']:
                        # Gather episode information
                        episode_id = get_episode_id(count, args.episodes)
                        episode_url_id = re.search(self._EPISODE_URL_PATTERN, episode['url']).group(1)
                        # Build episode record
                        output_episodes.append(Episode(
                            subject_id=args.subject,
                            episode_id=episode_id,
                            service_id=SITE_SERVICE_ID[self._CRAWLER_ID],
                            episode_url_id=episode_url_id,
                            remark='EP%s-PP视频' % episode['epTitle'],
                        ))
                        # Update counters
                        count += 1
                        if episode['vip'] == '0':
                            free_count += 1
                # Check consistency of the number of episodes
                if count != len(args.episodes):
                    log.warning('Episodes mismatch')
                # Gather subject information
                paid = get_paid_status(count, free_count)
                # Build source record
                output_source = Source(
                    subject_id=args.subject,
                    service_id=SITE_SERVICE_ID[self._CRAWLER_ID],
                    paid=paid,
                    subject_url_id=subject_url_id,
                    subtitle_locales=['zh_CN'],
                    remark='%s-PP视频' % subject_name,
                )
        except (KeyError, ValueError):
            print(traceback.format_exc())
        return output_source, output_episodes
