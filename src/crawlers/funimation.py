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


class FunimationCrawler(Crawler):
    """Funimation Crawler."""
    _API_URL = 'https://prod-api-funimationnow.dadcdigital.com/api/funimation/episodes/'  # https://github.com/ytdl-org/youtube-dl/issues/14569
    _CRAWLER_ID = 'funimation'

    def crawl(self, args) -> tuple:
        """Crawl series on Funimation.

        :param args: arguments
        :return: source and episode records
        :rtype: tuple
        """
        output_episodes = []
        output_source = None
        try:
            # Initiate API request
            title_id = re.search(SITE_URL_PATTERN[self._CRAWLER_ID], args.url).group(1)
            payload = {
                'limit': 99999,
                'title_id': title_id,
            }
            response = requests.get(url=self._API_URL, headers=HTTP_HEADERS, params=payload)
            data = response.json()
            # Gather season information
            seasons = {}
            for episode in data['items']:
                if episode['item']['seasonId'] not in seasons:
                    seasons[episode['item']['seasonId']] = {
                        'season_title': episode['item']['seasonTitle'],
                        'season_num': episode['item']['seasonNum'],
                    }
            arg_season_id = getattr(args, 'funi_season', None)
            if (seasons.get(arg_season_id) is None and len(seasons) > 1) or (arg_season_id is not None and arg_season_id not in seasons):
                error_message = 'The season specified was not found, or multiple seasons were detected but none was specified. Available seasons:\n\n'
                for season_id in seasons:
                    error_message += '\tID: %s\tName: %s\tSeason: %s\n' % (season_id, seasons[season_id]['season_title'], seasons[season_id]['season_num'])
                error_message += '\nUse --funi-season flag to specify a valid season ID. Visit %s for more information.' % response.url
                log.error(error_message)
                return output_source, output_episodes
            if arg_season_id not in seasons:
                arg_season_id = list(seasons)[0]
            # Select eligible episodes
            eligible_episodes = []
            for episode in data['items']:
                if episode['item']['seasonId'] == arg_season_id and episode['mediaCategory'] != 'commentary':  # https://code.acr.moe/kazari/funimation-downloader/commit/3d83230e32263f28c57719e508919f9d8e341791#8ec9a00bfd09b3190ac6b22251dbb1aa95a0579d_33_44
                    eligible_episodes.append(episode)
            eligible_episodes.sort(key=lambda episode: episode['item']['episodeOrder'])
            # Reset counters
            count = 0
            free_count = 0
            for episode in eligible_episodes:
                # Gather episode information
                episode_id = get_episode_id(count, args.episodes)
                # Build episode record
                output_episodes.append(Episode(
                    subject_id=args.subject,
                    episode_id=episode_id,
                    service_id=SITE_SERVICE_ID[self._CRAWLER_ID],
                    episode_url_id=episode['item']['episodeSlug'],
                    remark='EP%s-Funimation' % episode['item']['episodeNum'],
                ))
                # Update counters
                count += 1
                if not (episode.get('mostRecentAvodJpnUs', {}).get('subscriptionRequired', False) or episode.get('mostRecentSvodJpnUs', {}).get('subscriptionRequired', False)):
                    free_count += 1
            # Check consistency of the number of episodes
            if count != len(args.episodes):
                log.warning('Episodes mismatch')
            # Gather subject information
            paid = get_paid_status(count, free_count)
            subject_name = eligible_episodes[0]['item']['titleName']
            if len(seasons) > 1:
                subject_name += ' %s' % eligible_episodes[0]['item']['seasonTitle']
            # Build source record
            output_source = Source(
                subject_id=args.subject,
                service_id=SITE_SERVICE_ID[self._CRAWLER_ID],
                paid=paid,
                subject_url_id=eligible_episodes[0]['item']['titleSlug'],
                subtitle_locales=['en_US'],
                remark='%s-Funimation' % subject_name,
            )
        except (KeyError, ValueError):
            print(traceback.format_exc())
        return output_source, output_episodes
