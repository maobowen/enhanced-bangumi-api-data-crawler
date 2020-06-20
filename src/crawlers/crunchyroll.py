import cloudscraper
import json
import logging
import os
import re
import requests
import traceback
import uuid

from .common import *
from .interfaces import Crawler
from ..consts import *
from ..models.episode import Episode
from ..models.source import Source

log = logging.getLogger(__name__)


class CrunchyrollCrawler(Crawler):
    """Crunchyroll Crawler."""
    _AUTHENTICATE_URL = 'https://api.crunchyroll.com/start_session.0.json'  # https://github.com/ThePBone/CrunchyrollDownloaderPy/blob/master/core.py#L63
    _COLLECTION_API_URL = 'https://api.crunchyroll.com/list_collections.0.json'  # https://github.com/ThePBone/CrunchyrollDownloaderPy/blob/master/core.py#L189
    _CRAWLER_ID = 'crunchyroll'
    _LOGIN_URL = 'https://api.crunchyroll.com/login.2.json'  # https://github.com/ThePBone/CrunchyrollDownloaderPy/blob/master/core.py#L94
    _MATURITY_WALL_QUERY_STRING = '?skip_wall=1'
    _MEDIA_API_URL = 'https://api.crunchyroll.com/list_media.0.json'  # https://github.com/ThePBone/CrunchyrollDownloaderPy/blob/master/core.py#L245
    _MEDIA_URL = 'https://www.crunchyroll.com/media-%s' + _MATURITY_WALL_QUERY_STRING
    # https://github.com/CloudMax94/crunchyroll-api/wiki

    def crawl(self, args) -> tuple:
        """Crawl series on Crunchyroll.

        :param args: arguments
        :return: source and episode records
        :rtype: tuple
        """
        output_episodes = []
        output_source = None
        try:
            # First authentication
            payload_auth = {
                'device_id': uuid.uuid1().hex,
                'device_type': "com.crunchyroll.crunchyroid",
                'access_token': "WveH9VkPLrXvuNm",
                'version': '1.1',
            }
            response_auth = requests.get(url=self._AUTHENTICATE_URL, headers=HTTP_HEADERS, params=payload_auth)
            session_id = response_auth.json()['data']['session_id']
            # Login
            payload_login = {
                'session_id': session_id,
                'account': os.getenv('CR_ACCOUNT'),
                'password': os.getenv('CR_PASSWORD'),
            }
            if self._MATURITY_WALL_QUERY_STRING in args.url:
                if payload_login['account'] and payload_login['password']:
                    response_login = requests.post(url=self._LOGIN_URL, headers=HTTP_HEADERS, params=payload_login)
                    # Second authentication
                    payload_auth['auth'] = response_login.json()['data']['auth']
                    response_auth = requests.get(url=self._AUTHENTICATE_URL, headers=HTTP_HEADERS, params=payload_auth)
                    session_id = response_auth.json()['data']['session_id']
                else:
                    log.error('CR_ACCOUNT and CR_PASSWORD environment variables must be set for uncensored series.')

            # Initiate HTTP request to get series
            scraper = cloudscraper.create_scraper(browser={
                'browser': 'firefox',
                'platform': 'darwin',
                'mobile': False,
            })
            response2 = scraper.get(args.url)
            series_id = re.search(r'<div class="show-actions" group_id="(.*)"><\/div>', response2.text).group(1)  # https://github.com/simplymemes/crunchyroll-dl/blob/master/index.js#L586
            # Initiate API request to get collection
            payload3 = {
                'fields': 'collection.collection_id,collection.name,collection.season,collection.media_count',
                'series_id': series_id,
                'session_id': session_id,
                'sort': 'asc',
            }
            response3 = requests.get(url=self._COLLECTION_API_URL, headers=HTTP_HEADERS, params=payload3)
            collections_data = response3.json()
            if not collections_data['error'] and len(collections_data['data']):
                collection = None
                if len(collections_data['data']) > 1:
                    if hasattr(args, 'cr_collection') and args.cr_collection is not None:
                        for c in collections_data['data']:
                            if int(c['collection_id']) == args.cr_collection:
                                collection = c
                                break
                    if collection is None:
                        error_message = 'The season specified was not found, or multiple seasons were detected but none was specified. Available seasons:\n\n'
                        for c in collections_data['data']:
                            error_message += '\tID: %s\tName: %s\tSeason: %s\n' % (c['collection_id'], c['name'], c['season'])
                        error_message += '\nUse --cr-collection flag to specify a valid collection ID. Visit %s for more information.' % response3.url
                        log.error(error_message)
                        return output_source, output_episodes
                else:
                    collection = collections_data['data'][0]
                # Initiate API request to get media
                payload4 = {
                    'collection_id': collection['collection_id'],
                    'fields': 'media.media_id,media.episode_number,media.free_available',
                    'limit': 5000,
                    'offset': 0,
                    'session_id': session_id,
                    'sort': 'asc',
                }
                response4 = requests.get(url=self._MEDIA_API_URL, headers=HTTP_HEADERS, params=payload4)
                media_data = response4.json()
                if not media_data['error'] and len(media_data['data']):
                    # Reset counters
                    count = 0
                    free_count = 0
                    first_episode = None
                    for episode in media_data['data']:
                        if episode['episode_number'] and episode['episode_number'] != '':
                            if not first_episode:
                                first_episode = episode
                            # Gather episode information
                            episode_id = get_episode_id(count, args.episodes)
                            # Build episode record
                            output_episodes.append(Episode(
                                subject_id=args.subject,
                                episode_id=episode_id,
                                service_id=SITE_SERVICE_ID[self._CRAWLER_ID],
                                episode_url_id=episode['media_id'],
                                remark='EP%s-Crunchyroll' % episode['episode_number'],
                            ))
                            # Update counters
                            count += 1
                            if episode['free_available']:
                                free_count += 1
                    # Check consistency of the number of episodes
                    if count != len(args.episodes):
                        log.warning('Episodes mismatch')
                    # Gather subject information
                    paid = get_paid_status(count, free_count)
                    response5 = scraper.get(self._MEDIA_URL % first_episode['media_id'])
                    vilos_config_media = json.loads(re.search(r'vilos\.config\.media\s*=\s*(\{.*\})', response5.content.decode()).group(1))
                    locales = []
                    for stream in vilos_config_media['streams']:
                        if stream['format'] == 'multitrack_adaptive_hls_v2' and stream['hardsub_lang']:
                            locales.append(self.process_locale_string(stream['hardsub_lang']))
                    # Build source record
                    output_source = Source(
                        subject_id=args.subject,
                        service_id=SITE_SERVICE_ID[self._CRAWLER_ID],
                        paid=paid,
                        subject_url_id=series_id,
                        subtitle_locales=locales,
                        remark='%s-Crunchyroll' % collection['name'],
                    )
        except (KeyError, ValueError):
            print(traceback.format_exc())
        return output_source, output_episodes

    @staticmethod
    def process_locale_string(locale_string: str) -> str:
        """Process locale string.

        :param str locale_string: a locale string grabbed from Crunchyroll website
        :return: a locale string in the format of 'xx_XX' with country code processed
        :rtype: str
        """
        substitution_map = {
            'arME': 'arSA',
            'esLA': 'esMX',
        }
        if locale_string in substitution_map:
            locale_string = substitution_map[locale_string]
        return '%s_%s' % (locale_string[:2], locale_string[2:])
