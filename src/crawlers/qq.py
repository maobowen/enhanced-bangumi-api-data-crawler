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


class QQVideoCrawler(Crawler):
    """Tencent Video Crawler."""
    _API_URL = 'https://node.video.qq.com/x/api/float_vinfo2'  # https://github.com/ljm9104/tencent_video_spider/blob/master/tencent_video_spider.py#L25
    _CRAWLER_ID = 'qq'

    def crawl(self, args) -> tuple:
        """Crawl series on Tencent Video.

        :param args: arguments
        :return: source and episode records
        :rtype: tuple
        """
        output_episodes = []
        output_source = None
        try:
            # Initiate API request
            cid = re.search(SITE_URL_PATTERN[self._CRAWLER_ID], args.url).group(1)
            payload = {
                'cid': cid,
            }
            response = requests.get(url=self._API_URL, headers=HTTP_HEADERS, params=payload)
            data = response.json()
            for i in range(len(data['c']['video_ids'])):
                # Gather episode information
                episode_id = get_episode_id(i, args.episodes)
                # Build episode record
                output_episodes.append(Episode(
                    subject_id=args.subject,
                    episode_id=episode_id,
                    service_id=SITE_SERVICE_ID[self._CRAWLER_ID],
                    episode_url_id=data['c']['video_ids'][i],
                    remark='EP%d-腾讯视频' % (i + 1),
                ))
            # Check consistency of the number of episodes
            if len(data['c']['video_ids']) != len(args.episodes):
                log.warning('Episodes mismatch')
            # Build source record
            output_source = Source(
                subject_id=args.subject,
                service_id=SITE_SERVICE_ID[self._CRAWLER_ID],
                subject_url_id=cid,
                subtitle_locales=['zh_CN'],
                remark='%s-腾讯视频' % data['c']['title'],
            )
        except (KeyError, ValueError):
            print(traceback.format_exc())
        return output_source, output_episodes
