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
        subject_id = 69944  # 跟班×服务
        subject_url_id = 'ze9dc9ec6cf5211e2b16f'
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % subject_url_id,
            subject=subject_id,
            episodes=verify_episode_ids_format('290366-290372,290374-290378,294896')[1],
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'paid': 0,
            'subject_url_id': subject_url_id,
            'episodes_count': 13,
            'test_episodes': [
                {'index': 0, 'episode_id': 290366, 'episode_number': '1'},
                {'index': 6, 'episode_id': 290372, 'episode_number': '7'},
                {'index': 7, 'episode_id': 290374, 'episode_number': '8'},
                {'index': 11, 'episode_id': 290378, 'episode_number': '12'},
                {'index': 12, 'episode_id': 294896, 'episode_number': '13'},
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
