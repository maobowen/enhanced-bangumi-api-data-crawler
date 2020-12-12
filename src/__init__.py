import argparse
import re

from .consts import SITE_SERVICE_ID, SITE_URL_PATTERN
from .crawlers.acfun import AcFunCrawler
from .crawlers.animad import AnimadCrawler
from .crawlers.bilibili import BilibiliCrawler
from .crawlers.crunchyroll import CrunchyrollCrawler
from .crawlers.funimation import FunimationCrawler
from .crawlers.interfaces import Crawler
from .crawlers.iqiyi import IqiyiCrawler
from .crawlers.letv import LeTVCrawler
from .crawlers.niconico import NiconicoCrawler
from .crawlers.netflix import NetflixCrawler
from .crawlers.pptv import PPTVCrawler
from .crawlers.qq import QQVideoCrawler
from .crawlers.viu import ViuCrawler
from .crawlers.youku import YoukuCrawler


def verify_episode_ids_format(ids_str: str) -> tuple:
    """Convert a list of Bangumi episode IDs in the format of page ranges to a Python list and validate each ID.

    :param str ids_str: list of Bangumi episode IDs in the format of page ranges
    :return: valid status and list of Bangumi episode IDs
    :rtype: tuple
    """
    intervals = ids_str.split(',')
    ids_list = []
    valid = True
    for interval in intervals:
        if '-' in interval:
            boundary_ids = [boundary_id.strip() for boundary_id in interval.split('-')]
            if len(boundary_ids) == 2 and boundary_ids[0].isdigit() and boundary_ids[-1].isdigit() and int(boundary_ids[0]) <= int(boundary_ids[-1]):
                for i in range(int(boundary_ids[0]), int(boundary_ids[-1]) + 1):
                    ids_list.append(i)
            else:
                valid = False
        elif interval.strip().isdigit():
            ids_list.append(int(interval.strip()))
        elif interval.strip() == '':
            ids_list.append(-1)
        else:
            valid = False
    return len(ids_list) > 0 and valid, ids_list


def get_args() -> argparse.Namespace:
    """Get and validate arguments.

    :return: validated arguments
    :rtype: argparse.Namespace
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', help='subject URL', type=str)
    parser.add_argument('-s', '--subject', help='subject ID on bangumi.tv', metavar='SUBJECT_ID', type=int)
    parser.add_argument('-e', '--episodes', help='episode IDs on bangumi.tv', metavar='EPISODE_IDS', type=str)
    parser.add_argument('--cr-collection', help='Crunchyroll collection ID', metavar='COLLECTION_ID', type=int)
    parser.add_argument('--funi-season', help='Funimation season ID', metavar='SEASON_ID', type=int)
    parser.add_argument('--nflx-season', help='Netflix season ID', metavar='SEASON_ID', type=int)
    args = parser.parse_args()
    while args.url is None:
        url = input("Subject URL: ")
        if url:
            args.url = url
    while args.subject is None:
        subject = input("Subject ID on bangumi.tv: ")
        if subject:
            args.subject = int(subject)
    if args.episodes:
        valid, episodes = verify_episode_ids_format(args.episodes)
        args.episodes = episodes if valid else None
    while args.episodes is None:
        episodes = input("Episode IDs on bangumi.tv: ")
        valid, episodes = verify_episode_ids_format(episodes)
        if valid:
            args.episodes = episodes
    return args


def add_optional_args(crawler: Crawler, args: argparse.Namespace):
    """Add and validate optional arguments.

    :param Crawler crawler: arguments
    :param argparse.Namespace args: arguments
    """
    if isinstance(crawler, CrunchyrollCrawler) and args.cr_collection is None:
        cr_collection = input("Crunchyroll collection ID (press ENTER for null): ")
        if cr_collection:
            args.cr_collection = int(cr_collection)
    elif isinstance(crawler, FunimationCrawler) and args.funi_season is None:
        funi_season = input("Funimation season ID (press ENTER for null): ")
        if funi_season:
            args.funi_season = int(funi_season)
    elif isinstance(crawler, NetflixCrawler) and args.nflx_season is None:
        nflx_season = input("Netflix season ID (press ENTER for null): ")
        if nflx_season:
            args.nflx_season = int(nflx_season)


def crawl(args: argparse.Namespace):
    """Call corresponding crawler and generate output.

    :param argparse.Namespace args: arguments
    """
    crawler = None
    crawler_classes = {
        'acfun':       AcFunCrawler,
        'animad':      AnimadCrawler,
        'bilibili':    BilibiliCrawler,
        'crunchyroll': CrunchyrollCrawler,
        'funimation':  FunimationCrawler,
        'iqiyi':       IqiyiCrawler,
        'letv':        LeTVCrawler,
        'netflix':     NetflixCrawler,
        'niconico':    NiconicoCrawler,
        'pptv':        PPTVCrawler,
        'qq':          QQVideoCrawler,
        'viu':         ViuCrawler,
        'youku':       YoukuCrawler,
    }
    for crawler_id in crawler_classes:
        if re.search(SITE_URL_PATTERN[crawler_id], args.url):
            crawler = crawler_classes[crawler_id]()
            break
    if crawler:
        add_optional_args(crawler, args)
        source, episodes = crawler.crawl(args)
        if source:
            print(source)
            print()
        for episode in episodes:
            print(episode)
    else:
        print('Unsupported URL. List of supported URLs:\n')
        for crawler_id in SITE_SERVICE_ID:
            print('\t%s - %s' % (SITE_SERVICE_ID[crawler_id], SITE_URL_PATTERN[crawler_id]))


def main():
    """Entry point of the crawler."""
    crawl(get_args())
