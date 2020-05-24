import argparse
import pytest

from src import verify_episode_ids_format
from src.crawlers.youku import YoukuCrawler


class TestYoukuCrawler:
    """Youku crawler test suite."""
    _SITE_URL_PATTERN = 'https://list.youku.com/show/id_%s.html'
    _crawler = YoukuCrawler()

    @staticmethod
    @pytest.fixture
    def test_youku_generic(generic_test_helper):
        """Youku test helper."""
        def _test_youku_generic(source, episodes: list, test_config: dict):
            test_config['service_id'] = 'youku.com'
            test_config['subtitle_locales'] = ['zh_CN']
            test_config['remark'] = '<名称>-优酷'
            test_config['episode_url_id_pattern'] = r'^(?:[A-Za-z0-9+/]+={,2})$'
            for test_episode_item in test_config['test_episodes']:
                test_episode_item['remark'] = 'EP%s-优酷' % test_episode_item['episode_number']
                del test_episode_item['episode_number']
            generic_test_helper.test_source(source, test_config)
            generic_test_helper.test_episodes(episodes, test_config)
        return _test_youku_generic

    def test_youku_all_free_wo_exclusion(self, test_youku_generic, caplog):
        """Youku with all episodes free and continuous Bangumi episode IDs."""
        subject_id = 1851  # Angel Beats
        subject_url_id = 'zfac023bc61ad11e0bea1'
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % subject_url_id,
            subject=subject_id,
            episodes=verify_episode_ids_format('24834-24846')[1],
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'paid': 0,
            'subject_url_id': subject_url_id,
            'episodes_count': 13,
            'test_episodes': [
                {'index': 0, 'episode_id': 24834, 'episode_number': '1'},
                {'index': 12, 'episode_id': 24846, 'episode_number': '13'},
            ],
        }
        test_youku_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text

    def test_youku_all_free_w_exclusion(self, test_youku_generic, caplog):
        """Youku with all episodes free and discontinuous Bangumi episode IDs."""
        subject_id = 140001  # Re:从零开始的异世界生活 第1期
        subject_url_id = 'z1b7c90e0e4df11e59e2a'
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % subject_url_id,
            subject=subject_id,
            episodes=verify_episode_ids_format('621357,621357-621368,626044-626055,626353')[1],
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'paid': 0,
            'subject_url_id': subject_url_id,
            'episodes_count': 26,
            'test_episodes': [
                {'index': 0, 'episode_id': 621357, 'episode_number': '1'},
                {'index': 1, 'episode_id': 621357, 'episode_number': '2'},
                {'index': 12, 'episode_id': 621368, 'episode_number': '13'},
                {'index': 13, 'episode_id': 626044, 'episode_number': '14'},
                {'index': 24, 'episode_id': 626055, 'episode_number': '25'},
                {'index': 25, 'episode_id': 626353, 'episode_number': '26'},
            ],
        }
        test_youku_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text

    def test_youku_first_free_wo_exclusion(self, test_youku_generic, caplog):
        """Youku with only the first episode free and continuous Bangumi episode IDs."""
        subject_id = 101442  # 悠哉日常大王 第2期
        subject_url_id = 'z837ad5f2198411e5b432'
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % subject_url_id,
            subject=subject_id,
            episodes=verify_episode_ids_format('538096-538107')[1],
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'paid': 1,
            'subject_url_id': subject_url_id,
            'episodes_count': 12,
            'test_episodes': [
                {'index': 0, 'episode_id': 538096, 'episode_number': '1'},
                {'index': 11, 'episode_id': 538107, 'episode_number': '12'},
            ],
        }
        test_youku_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text

    def test_youku_first_free_w_exclusion(self, test_youku_generic, caplog):
        """Youku with only the first episode free and discontinuous Bangumi episode IDs."""
        subject_id = 78405  # 悠哉日常大王 第1期
        subject_url_id = 'z838fc1c8030211e3b8b7'
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % subject_url_id,
            subject=subject_id,
            episodes=verify_episode_ids_format('319289-319299,320742')[1],
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'paid': 1,
            'subject_url_id': subject_url_id,
            'episodes_count': 12,
            'test_episodes': [
                {'index': 0, 'episode_id': 319289, 'episode_number': '1'},
                {'index': 10, 'episode_id': 319299, 'episode_number': '11'},
                {'index': 11, 'episode_id': 320742, 'episode_number': '12'},
            ],
        }
        test_youku_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text
