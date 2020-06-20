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


class AcFunCrawler(Crawler):
    """AcFun Crawler."""
    _API_URL = 'https://www.acfun.cn/album/abm/bangumis/video'  # https://github.com/bangumi-data/helper/blob/master/lib/crawlers/acfun.js#L31
    _CRAWLER_ID = 'acfun'

    def crawl(self, args) -> tuple:
        """Crawl series on AcFun.

        :param args: arguments
        :return: source and episode records
        :rtype: tuple
        """
        output_episodes = []
        output_source = None
        try:
            # Initiate API request
            album_id = re.search(SITE_URL_PATTERN[self._CRAWLER_ID], args.url).group(1)
            payload = {
                'albumId': album_id,
                'num': 1,
                'size': 1000,
            }
            response = requests.get(url=self._API_URL, headers=HTTP_HEADERS, params=payload)
            data = response.json()
            if data['code']:
                for i in range(len(data['data']['content'])):
                    episode = data['data']['content'][i]['videos'][0]
                    # Gather episode information
                    episode_id = get_episode_id(i, args.episodes)
                    episode_index = str(episode['sort'] / 10) if episode['sort'] % 10 > 1 else str(episode['sort'] // 10)
                    # Build episode record
                    output_episodes.append(Episode(
                        subject_id=args.subject,
                        episode_id=episode_id,
                        service_id=SITE_SERVICE_ID[self._CRAWLER_ID],
                        episode_url_id='%d_%d' % (episode['groupId'], episode['id']),
                        remark='EP%s-A站' % episode_index,
                    ))
                # Check consistency of the number of episodes
                if len(data['data']['content']) != len(args.episodes):
                    log.warning('Episodes mismatch')
                # Build source record
                output_source = Source(
                    subject_id=args.subject,
                    service_id=SITE_SERVICE_ID[self._CRAWLER_ID],
                    paid=0,
                    subject_url_id=album_id,
                    subtitle_locales=['zh_CN'],
                    remark='<名称>-A站',
                )
        except (KeyError, ValueError):
            print(traceback.format_exc())
        return output_source, output_episodes
