import cloudscraper
import json
import logging
import re
import traceback

from .common import *
from .interfaces import Crawler
from ..consts import *
from ..models.episode import Episode
from ..models.source import Source

log = logging.getLogger(__name__)


class NetflixCrawler(Crawler):
    """Netflix Crawler."""
    _CRAWLER_ID = 'netflix'

    def crawl(self, args) -> tuple:
        """Crawl series on Netflix.

        :param args: arguments
        :return: source and episode records
        :rtype: tuple
        """
        output_episodes = []
        output_source = None
        try:
            # Initiate API request
            scraper = cloudscraper.create_scraper(browser={
                'browser': 'firefox',
                'platform': 'darwin',
                'mobile': False,
            })
            response = scraper.get(args.url)
            react_context = json.loads(re.search(r'netflix.reactContext = ({.*});', response.text).group(1).replace('\\x', '\\u00'))  # https://stackoverflow.com/a/4296045
            # Gather season information
            section_data = react_context['models']['nmTitleUI']['data']['sectionData']
            subject_name = None
            seasons_and_episodes = None
            for e in section_data:
                if e['type'] == 'hero':
                    subject_name = e['data']['title']
                elif e['type'] == 'seasonsAndEpisodes':
                    seasons_and_episodes = e['data']['seasons']
                if subject_name is not None and seasons_and_episodes:
                    break
            seasons = {}
            for season in seasons_and_episodes:
                seasons[season['seasonId']] = {
                    'season_name': season['seasonName'],
                    'season_num': season['num'],
                    'episodes': season['episodes'],
                }
            arg_season_id = getattr(args, 'nflx_season', None)
            if (seasons.get(arg_season_id) is None and len(seasons) > 1) or (arg_season_id is not None and arg_season_id not in seasons):
                error_message = 'The season specified was not found, or multiple seasons were detected but none was specified. Available seasons:\n\n'
                for season_id in seasons:
                    error_message += '\tID: %s\tName: %s\tSeason: %s\n' % (season_id, seasons[season_id]['season_name'], seasons[season_id]['season_num'])
                error_message += '\nUse --nflx-season flag to specify a valid season ID. Visit %s for more information.' % response.url
                log.error(error_message)
                return output_source, output_episodes
            if arg_season_id not in seasons:
                arg_season_id = list(seasons)[0]
            episodes = seasons[arg_season_id]['episodes']
            # Reset counters
            count = 0
            for episode in episodes:
                # Gather episode information
                episode_id = get_episode_id(count, args.episodes)
                # Build episode record
                output_episodes.append(Episode(
                    subject_id=args.subject,
                    episode_id=episode_id,
                    service_id=SITE_SERVICE_ID[self._CRAWLER_ID],
                    episode_url_id=str(episode['episodeId']),
                    remark='EP%s-Netflix' % episode['episodeNum'],
                ))
                # Update counters
                count += 1
            # Check consistency of the number of episodes
            if count != len(args.episodes):
                log.warning('Episodes mismatch')
            # Build source record
            output_source = Source(
                subject_id=args.subject,
                service_id=SITE_SERVICE_ID[self._CRAWLER_ID],
                paid=2,
                subject_url_id=str(react_context['models']['nmTitleUI']['data']['videoId']),
                subtitle_locales=['en_US'],
                remark='%s-Netflix' % subject_name,
            )
        except (KeyError, ValueError):
            print(traceback.format_exc())
        return output_source, output_episodes
