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


class BilibiliCrawler(Crawler):
    """Bilibili Crawler."""
    _API_URL = 'https://bangumi.bilibili.com/view/web_api/media'  # https://github.com/bangumi-data/helper/blob/master/lib/crawlers/bilibili.js#L34
    _CRAWLER_ID = 'bilibili'

    def crawl(self, args) -> tuple:
        """Crawl series on Bilibili.

        :param args: arguments
        :return: source and episode records
        :rtype: tuple
        """
        output_episodes = []
        output_source = None
        try:
            # Initiate API request
            media_id = re.search(SITE_URL_PATTERN[self._CRAWLER_ID], args.url).group(1)
            payload = {
                'media_id': media_id,
            }
            response = requests.get(url=self._API_URL, headers=HTTP_HEADERS, params=payload)
            data = response.json()
            if data['code'] == 0:
                # Gather subject information
                service_id_suffix = 'cn'
                remark_suffix = '大陆'
                if '僅限' in data['result']['chn_name']:
                    service_id_suffix = 'hk'
                    if '僅限港澳台' in data['result']['chn_name']:
                        remark_suffix = '港台'
                    elif '僅限台灣' in data['result']['chn_name']:
                        remark_suffix = '台湾'
                    elif '僅限港澳' in data['result']['chn_name']:
                        remark_suffix = '香港'
                service_id = '%s_%s' % (SITE_SERVICE_ID[self._CRAWLER_ID], service_id_suffix)
                # Reset counters
                count = 0
                free_count = 0
                for episode in data['result']['episodes']:
                    if episode['section_type'] == 0:
                        # Gather episode information
                        episode_id = get_episode_id(count, args.episodes)
                        episode_url_id = episode['bvid']
                        if episode['page'] != 1:
                            episode_url_id += '/index_%d.html' % episode['page']
                        # Build episode record
                        output_episodes.append(Episode(
                            subject_id=args.subject,
                            episode_id=episode_id,
                            service_id=service_id,
                            episode_url_id=episode_url_id,
                            remark='EP%s-B站%s' % (episode['index'], remark_suffix),
                        ))
                        # Update counters
                        count += 1
                        if episode['episode_status'] == 2:
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
                    subject_url_id=media_id,
                    subtitle_locales=['zh_%s' % service_id_suffix.upper()],
                    remark='%s-B站%s' % (data['result']['chn_name'], remark_suffix),
                )
        except (KeyError, ValueError):
            print(traceback.format_exc())
        return output_source, output_episodes
