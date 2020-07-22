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


class NiconicoCrawler(Crawler):
    """Niconico Crawler."""
    _CRAWLER_ID = 'niconico'

    def crawl(self, args) -> tuple:
        """Crawl series on Niconico.

        :param args: arguments
        :return: source and episode records
        :rtype: tuple
        """
        output_episodes = []
        output_source = None
        try:
            # Initiate HTTP request
            payload = {
                'order': 'a',
                'page': 1,
                'sort': 'f',
            }
            # Reset counters
            count = 0
            free_count = 0
            last_page = False
            while not last_page:
                response = requests.get(url=args.url + '/video', headers=HTTP_HEADERS, params=payload)
                soup = BeautifulSoup(response.content.replace(b'<!--/li-->', b'</li>'), 'html.parser')
                subject_name = soup.select('nav h1.channel_name a')[0].decode_contents()
                for episodeDOM in soup.select('section.video ul.items li.item'):
                    # Gather episode information
                    episode_name = episodeDOM.select('div.item_right h6.title a')[0].decode_contents().split(subject_name)
                    episode_name = episode_name[1] if len(episode_name) > 1 else episode_name[0]
                    if 'PV' not in episode_name:
                        episode_id = get_episode_id(count, args.episodes)
                        episode_url = episodeDOM.select('div.item_right h6.title a')[0].get('href')
                        episode_url_id = re.search(r'https?://(?:www\.)?nicovideo\.jp\/watch\/(\w+)', episode_url).group(1)
                        match_numeric = re.search(r'(\d+(\.\d+)?)', episode_name)
                        match_kanji = re.search(u'([一二三四五六七八九十]+)', episode_name)
                        episode_index = match_numeric.group(1) if match_numeric else match_kanji.group(1) if match_kanji else episode_name.strip()
                        # Build episode record
                        output_episodes.append(Episode(
                            subject_id=args.subject,
                            episode_id=episode_id,
                            service_id=SITE_SERVICE_ID[self._CRAWLER_ID],
                            episode_url_id=episode_url_id,
                            remark='EP%s-niconico' % episode_index,
                        ))
                        # Update counters
                        count += 1
                        if not episodeDOM.select('div.item_left a.thumb_video span.all_pay'):
                            free_count += 1
                # Check last page
                next_page_DOM = soup.select('footer menu.pager ul li.next')
                if len(next_page_DOM) == 0 or "disabled" in next_page_DOM[0]['class']:
                    last_page = True
                else:
                    payload['page'] += 1
            # Check consistency of the number of episodes
            if count != len(args.episodes):
                log.warning('Episodes mismatch')
            # Gather subject information
            paid = get_paid_status(count, free_count)
            subject_url_id = re.search(SITE_URL_PATTERN[self._CRAWLER_ID], args.url).group(1)
            # Build source record
            output_source = Source(
                subject_id=args.subject,
                service_id=SITE_SERVICE_ID[self._CRAWLER_ID],
                paid=paid,
                subject_url_id=subject_url_id,
                subtitle_locales=['ja_JP'],
                remark='%s-niconico' % subject_name,
            )
        except (KeyError, ValueError):
            print(traceback.format_exc())
        return output_source, output_episodes
