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
        subject_id = 150775  # NEW GAME! (第1期)
        subject_url_id = 'zc9b2f1283cd611e6abda'
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % subject_url_id,
            subject=subject_id,
            episodes=verify_episode_ids_format('642458-642469')[1],
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'paid': 0,
            'subject_url_id': subject_url_id,
            'episodes_count': 12,
            'test_episodes': [
                {'index': 0, 'episode_id': 642458, 'episode_number': '1'},
                {'index': 11, 'episode_id': 642469, 'episode_number': '12'},
            ],
        }
        test_youku_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text

    def test_youku_all_free_w_exclusion(self, test_youku_generic, caplog):
        """Youku with all episodes free and discontinuous Bangumi episode IDs."""
        subject_id = 120925  # Charlotte
        subject_url_id = 'z074ab022197c11e5b5ce'
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % subject_url_id,
            subject=subject_id,
            episodes=verify_episode_ids_format('541642-541653,545598')[1],
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'paid': 0,
            'subject_url_id': subject_url_id,
            'episodes_count': 13,
            'test_episodes': [
                {'index': 0, 'episode_id': 541642, 'episode_number': '1'},
                {'index': 11, 'episode_id': 541653, 'episode_number': '12'},
                {'index': 12, 'episode_id': 545598, 'episode_number': '13'},
            ],
        }
        test_youku_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text

    def test_youku_first_free_wo_exclusion(self, test_youku_generic, caplog):
        """Youku with only the first episode free and continuous Bangumi episode IDs."""
        subject_id = 10440  # 我们仍未知道那天所看见的花的名字。
        subject_url_id = 'zf5336bb689d511e0a046'
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % subject_url_id,
            subject=subject_id,
            episodes=verify_episode_ids_format('84692-84702')[1],
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'paid': 1,
            'subject_url_id': subject_url_id,
            'episodes_count': 11,
            'test_episodes': [
                {'index': 0, 'episode_id': 84692, 'episode_number': '1'},
                {'index': 10, 'episode_id': 84702, 'episode_number': '11'},
            ],
        }
        test_youku_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text

    def test_youku_first_free_w_exclusion(self, test_youku_generic, caplog):
        """Youku with only the first episode free and discontinuous Bangumi episode IDs."""
        subject_id = 137722  # 只有我不存在的城市
        subject_url_id = 'z17a6b178a85111e5be16'
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % subject_url_id,
            subject=subject_id,
            episodes=verify_episode_ids_format('596604-596614,596827')[1],
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'paid': 1,
            'subject_url_id': subject_url_id,
            'episodes_count': 12,
            'test_episodes': [
                {'index': 0, 'episode_id': 596604, 'episode_number': '1'},
                {'index': 10, 'episode_id': 596614, 'episode_number': '11'},
                {'index': 11, 'episode_id': 596827, 'episode_number': '12'},
            ],
        }
        test_youku_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text
