import argparse
import pytest

from src import verify_episode_ids_format
from src.crawlers.letv import LeTVCrawler


class TestLeTVCrawler:
    """LeTV crawler test suite."""
    _SITE_URL_PATTERN = 'https://www.le.com/comic/%d.html'
    _crawler = LeTVCrawler()

    @staticmethod
    @pytest.fixture
    def test_letv_generic(generic_test_helper):
        """LeTV test helper."""
        def _test_letv_generic(source, episodes: list, test_config: dict):
            test_config['service_id'] = 'le.com'
            test_config['subject_url_id'] = str(test_config['subject_url_id'])
            test_config['subtitle_locales'] = ['zh_CN']
            test_config['remark'] = '%s-乐视视频' % test_config['subject_name']
            del test_config['subject_name']
            test_config['episode_url_id_pattern'] = r'^(?:\d+)$'
            for test_episode_item in test_config['test_episodes']:
                test_episode_item['remark'] = 'EP%s-乐视视频' % test_episode_item['episode_number']
                del test_episode_item['episode_number']
            generic_test_helper.test_source(source, test_config)
            generic_test_helper.test_episodes(episodes, test_config)
        return _test_letv_generic

    def test_letv_all_free_wo_exclusion(self, test_letv_generic, caplog):
        """LeTV with all episodes free and continuous Bangumi episode IDs."""
        subject_id = 37785  # 来自新世界
        subject_url_id = 81938
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % subject_url_id,
            subject=subject_id,
            episodes=verify_episode_ids_format('198793-198817')[1],
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'paid': 0,
            'subject_url_id': subject_url_id,
            'subject_name': '来自新世界',
            'episodes_count': 25,
            'test_episodes': [
                {'index': 0, 'episode_id': 198793, 'episode_number': '1'},
                {'index': 24, 'episode_id': 198817, 'episode_number': '25'},
            ],
        }
        test_letv_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text

    def test_letv_all_free_w_exclusion(self, test_letv_generic, caplog):
        """LeTV with all episodes free and discontinuous Bangumi episode IDs."""
        subject_id = 120187  # 干物妹！小埋 第1期
        subject_url_id = 10010414
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % subject_url_id,
            subject=subject_id,
            episodes=verify_episode_ids_format('538144-538146,538149-538155,549886-549887')[1],
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'paid': 0,
            'subject_url_id': subject_url_id,
            'subject_name': '干物妹！小埋',
            'episodes_count': 12,
            'test_episodes': [
                {'index': 0, 'episode_id': 538144, 'episode_number': '1'},
                {'index': 2, 'episode_id': 538146, 'episode_number': '3'},
                {'index': 3, 'episode_id': 538149, 'episode_number': '4'},
                {'index': 9, 'episode_id': 538155, 'episode_number': '10'},
                {'index': 10, 'episode_id': 549886, 'episode_number': '11'},
                {'index': 11, 'episode_id': 549887, 'episode_number': '12'},
            ],
        }
        test_letv_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text

    def test_letv_first_free_wo_exclusion(self, test_letv_generic, caplog):
        """LeTV with only the first episode free and continuous Bangumi episode IDs."""
        subject_id = 146754  # 怪物猎人物语 RIDE ON
        subject_url_id = 10034731
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % subject_url_id,
            subject=subject_id,
            episodes=verify_episode_ids_format('638229-638276')[1],
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'paid': 1,
            'subject_url_id': subject_url_id,
            'subject_name': '怪物猎人物语 RIDE ON',
            'episodes_count': 48,
            'test_episodes': [
                {'index': 0, 'episode_id': 638229, 'episode_number': '1'},
                {'index': 47, 'episode_id': 638276, 'episode_number': '48'},
            ],
        }
        test_letv_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text
