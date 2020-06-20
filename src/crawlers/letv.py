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


class LeTVCrawler(Crawler):
    """LeTV Crawler."""
    _ALBUM_API_URL = 'http://static.meizi.app.m.letv.com/android/mod/mob/ctl/album/act/detail/id/%s/pcode/010410000/version/2.1.mindex.html'  # https://github.com/afirez/WeVideo/blob/master/app/src/main/java/com/afirez/wevideo/api/LetvApi.java#L55
    _VIDEO_LIST_API_URL = 'http://static.app.m.letv.com/android/mod/mob/ctl/videolist/act/detail/id/%s/vid/0/b/1/s/100/o/-1/m/1/pcode/010410000/version/2.1.mindex.html'  # https://github.com/afirez/WeVideo/blob/master/app/src/main/java/com/afirez/wevideo/api/LetvApi.java#L61
    _CRAWLER_ID = 'letv'

    def crawl(self, args) -> tuple:
        """Crawl series on LeTV.

        :param args: arguments
        :return: source and episode records
        :rtype: tuple
        """
        output_episodes = []
        output_source = None
        try:
            # Initiate API request to get subject
            album_id = re.search(SITE_URL_PATTERN[self._CRAWLER_ID], args.url).group(1)
            response = requests.get(url=self._ALBUM_API_URL % album_id, headers=HTTP_HEADERS)
            data = response.json()
            # Gather subject information
            subject_name = '<名称>'
            if data['header']['status'] == '1':
                subject_name = data['body']['nameCn']
            # Initiate API request to get episodes
            response = requests.get(url=self._VIDEO_LIST_API_URL % album_id, headers=HTTP_HEADERS)
            data = response.json()
            if data['header']['status'] == '1':
                # Reset counters
                count = 0
                free_count = 0
                for episode in data['body']['videoInfo']:
                    if episode['videoType'] == '0001':
                        # Gather episode information
                        episode_id = get_episode_id(count, args.episodes)
                        # Build episode record
                        output_episodes.append(Episode(
                            subject_id=args.subject,
                            episode_id=episode_id,
                            service_id=SITE_SERVICE_ID[self._CRAWLER_ID],
                            episode_url_id=episode['id'],
                            remark='EP%s-乐视视频' % episode['episode'],
                        ))
                        # Update counters
                        count += 1
                        if episode['pay'] == '0':
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
                    subject_url_id=album_id,
                    subtitle_locales=['zh_CN'],
                    remark='%s-乐视视频' % subject_name,
                )
        except (KeyError, ValueError):
            print(traceback.format_exc())
        return output_source, output_episodes
