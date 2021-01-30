import json
import logging
import os
import re
import requests
import traceback
import urllib.parse

from .common import *
from .interfaces import Crawler
from ..consts import *
from ..models.episode import Episode
from ..models.source import Source

log = logging.getLogger(__name__)


class IqiyiCrawler(Crawler):
    """iQIYI Crawler."""
    _API_URL = 'http://cache.video.qiyi.com/jp/avlist/%s/1/50/'  # https://github.com/bangumi-data/helper/blob/master/lib/crawlers/iqiyi.js#L81
    _CN_PROXY_ENV_VAR_KEY = 'CN_PROXY'
    _CRAWLER_ID = 'iqiyi'
    _GEO_CHECK_API_URL = 'http://ipservice.163.com/isFromMainland'

    def crawl(self, args) -> tuple:
        """Crawl series on iQIYI.

        :param args: arguments
        :return: source and episode records
        :rtype: tuple
        """
        output_episodes = []
        output_source = None
        try:
            # Geo Check
            use_proxy = False
            geo_check_response = requests.get(url=self._GEO_CHECK_API_URL)
            if 'true' not in geo_check_response.text:
                if not os.getenv(self._CN_PROXY_ENV_VAR_KEY):
                    log.error('You must have a Chinese IP address. Use %s environment variable to set a proxy API.' % self._CN_PROXY_ENV_VAR_KEY)
                    return output_source, output_episodes
                else:
                    use_proxy = True
            # Gather information
            is_tw = 'tw.iqiyi' in args.url
            service_id_prefix = 'tw.' if is_tw else ''
            service_id = '%s%s' % (service_id_prefix, SITE_SERVICE_ID[self._CRAWLER_ID])
            remark = '愛奇藝' if is_tw else '爱奇艺'
            locale_suffix = 'HK' if is_tw else 'CN'
            # Initiate API requests
            response1 = requests.get(url=args.url, headers=HTTP_HEADERS)
            album_id = re.search(r'album-?(?:I|i)d\s*(?::|=)\s*"?(\d+)"?', response1.text).group(1)  # https://github.com/ytdl-org/youtube-dl/blob/master/youtube_dl/extractor/iqiyi.py#L315
            api_url = self._API_URL % album_id
            if use_proxy:
                api_url = os.getenv(self._CN_PROXY_ENV_VAR_KEY) % urllib.parse.quote(string=api_url, safe='')
            response2 = requests.get(url=api_url, headers=HTTP_HEADERS)
            data = json.loads(re.search(r'var\stvInfoJs=(.*)', response2.text).group(1))
            if data['code'] == 'A00000':
                # Gather subject information
                subject_name = data['data']['vlist'][0]['vn'].split()[0]
                # Reset counters
                count = 0
                free_count = 0
                for episode in data['data']['vlist']:
                    if episode['type'] == '1':
                        # Gather episode information
                        episode_id = get_episode_id(count, args.episodes)
                        episode_url_id = re.search(r'https?://(?:www\.)?iqiyi\.com\/(v_\w+)\.html', episode['vurl']).group(1)
                        vns = episode['vn'].split(subject_name)
                        episode_name = vns[1] if len(vns) > 1 else vns[0]
                        match = re.search(r'第(\d+(?:\.\d+)?)', episode_name)
                        episode_index = match.group(1) if match else episode_name
                        # Build episode record
                        output_episodes.append(Episode(
                            subject_id=args.subject,
                            episode_id=episode_id,
                            service_id=service_id,
                            episode_url_id=episode_url_id,
                            remark='EP%s-%s' % (episode_index, remark),
                        ))
                        # Update counters
                        count += 1
                        if episode['purType'] == 0:
                            free_count += 1
                # Check consistency of the number of episodes
                if count != len(args.episodes):
                    log.warning('Episodes mismatch')
                # Gather subject information
                paid = 0 if is_tw else get_paid_status(count, free_count)
                subject_url_id = re.search(SITE_URL_PATTERN[self._CRAWLER_ID], args.url).group(1)
                # Build source record
                output_source = Source(
                    subject_id=args.subject,
                    service_id=service_id,
                    paid=paid,
                    subject_url_id=subject_url_id,
                    subtitle_locales=['zh_%s' % locale_suffix],
                    remark='%s-%s' % (subject_name, remark),
                )
        except (KeyError, ValueError):
            print(traceback.format_exc())
        return output_source, output_episodes
