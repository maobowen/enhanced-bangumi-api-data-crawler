import argparse
import os
import pytest

from src import verify_episode_ids_format
from src.crawlers.netflix import NetflixCrawler


@pytest.mark.skipif('TRAVIS' in os.environ and os.environ['TRAVIS'] == 'true',
                    reason='Skipping these tests on Travis CI.')
class TestNetflixCrawler:
    """Netflix crawler test suite."""
    _SITE_URL_PATTERN = 'https://www.netflix.com/title/%d'
    _crawler = NetflixCrawler()

    @staticmethod
    @pytest.fixture
    def test_netflix_generic(generic_test_helper):
        """Netflix test helper."""
        def _test_netflix_generic(source, episodes: list, test_config: dict):
            test_config['service_id'] = 'netflix.com'
            test_config['paid'] = 2
            test_config['subject_url_id'] = str(test_config['subject_url_id'])
            test_config['subtitle_locales'] = ['en_US']
            test_config['remark'] = '%s-Netflix' % test_config['subject_name']
            del test_config['subject_name']
            test_config['episode_url_id_pattern'] = r'^(?:\d+)$'
            for test_episode_item in test_config['test_episodes']:
                test_episode_item['remark'] = 'EP%s-Netflix' % test_episode_item['episode_number']
                del test_episode_item['episode_number']
            generic_test_helper.test_source(source, test_config)
            generic_test_helper.test_episodes(episodes, test_config)
        return _test_netflix_generic

    def test_netflix_single_collection_wo_exclusion(self, test_netflix_generic, caplog):
        """Netflix with single collection and continuous Bangumi episode IDs."""
        subject_id = 271151  # 擅长捉弄的高木同学 第2期
        subject_url_id = 80228274
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % subject_url_id,
            subject=subject_id,
            episodes=verify_episode_ids_format('893874-893885')[1],
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'subject_url_id': subject_url_id,
            'subject_name': 'Teasing Master Takagi-san',
            'episodes_count': 12,
            'test_episodes': [
                {'index': 0, 'episode_id': 893874, 'episode_number': '1'},
                {'index': 11, 'episode_id': 893885, 'episode_number': '12'},
            ],
        }
        test_netflix_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text

    def test_netflix_single_collection_w_exclusion(self, test_netflix_generic, caplog):
        """Netflix with single collection and discontinuous Bangumi episode IDs."""
        subject_id = 137722  # 只有我不在的城市
        subject_url_id = 80114225
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % subject_url_id,
            subject=subject_id,
            episodes=verify_episode_ids_format('596604-596614,596827')[1],
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'subject_url_id': subject_url_id,
            'subject_name': 'Erased',
            'episodes_count': 12,
            'test_episodes': [
                {'index': 0, 'episode_id': 596604, 'episode_number': '1'},
                {'index': 10, 'episode_id': 596614, 'episode_number': '11'},
                {'index': 11, 'episode_id': 596827, 'episode_number': '12'},
            ],
        }
        test_netflix_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text

    def test_netflix_multiple_collections_wo_exclusion(self, test_netflix_generic, caplog):
        """Netflix with multiple collections and continuous Bangumi episode IDs."""
        subject_id = 285813  # 大欺诈师
        subject_url_id = 81220435
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % subject_url_id,
            subject=subject_id,
            episodes=verify_episode_ids_format('894891-894904')[1],
            nflx_season=81220436,
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'subject_url_id': subject_url_id,
            'subject_name': 'Great Pretender',
            'episodes_count': 14,
            'test_episodes': [
                {'index': 0, 'episode_id': 894891, 'episode_number': '1'},
                {'index': 13, 'episode_id': 894904, 'episode_number': '14'},
            ],
        }
        test_netflix_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text

    def test_netflix_multiple_collections_w_exclusion(self, test_netflix_generic, caplog):
        """Netflix with multiple collections and discontinuous Bangumi episode IDs."""
        subject_id = 1424  # 轻音少女 第1期
        subject_url_id = 80003477
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % subject_url_id,
            subject=subject_id,
            episodes=verify_episode_ids_format('4835-4846,7535,28181')[1],
            nflx_season=80004139,
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'subject_url_id': subject_url_id,
            'subject_name': 'K-On!',
            'episodes_count': 14,
            'test_episodes': [
                {'index': 0, 'episode_id': 4835, 'episode_number': '1'},
                {'index': 11, 'episode_id': 4846, 'episode_number': '12'},
                {'index': 12, 'episode_id': 7535, 'episode_number': '13'},
                {'index': 13, 'episode_id': 28181, 'episode_number': '14'},
            ],
        }
        test_netflix_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text
