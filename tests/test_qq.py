import argparse
import pytest

from src import verify_episode_ids_format
from src.crawlers.qq import QQVideoCrawler


class TestQQVideoCrawler:
    """Tencent Video crawler test suite."""
    _SITE_URL_PATTERN = 'https://v.qq.com/detail/0/%s.html'
    _crawler = QQVideoCrawler()

    @staticmethod
    @pytest.fixture
    def test_qq_generic(generic_test_helper):
        """Tencent Video test helper."""
        def _test_qq_generic(source, episodes: list, test_config: dict):
            test_config['service_id'] = 'v.qq.com'
            test_config['paid'] = -1
            test_config['subtitle_locales'] = ['zh_CN']
            test_config['remark'] = '%s-腾讯视频' % test_config['subject_name']
            del test_config['subject_name']
            test_config['episode_url_id_pattern'] = r'^(?:[a-z0-9]+)$'
            for test_episode_item in test_config['test_episodes']:
                test_episode_item['remark'] = 'EP%s-腾讯视频' % test_episode_item['episode_number']
                del test_episode_item['episode_number']
            generic_test_helper.test_source(source, test_config)
            generic_test_helper.test_episodes(episodes, test_config)
        return _test_qq_generic

    def test_qq_wo_exclusion(self, test_qq_generic, caplog):
        """Tencent Video with continuous Bangumi episode IDs."""
        subject_id = 277551  # 地缚少年花子君
        subject_url_id = 'mzc00200uewor2j'
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % subject_url_id,
            subject=subject_id,
            episodes=verify_episode_ids_format('925459-925470')[1],
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'subject_url_id': subject_url_id,
            'subject_name': '地缚少年花子君',
            'episodes_count': 12,
            'test_episodes': [
                {'index': 0, 'episode_id': 925459, 'episode_number': '1'},
                {'index': 11, 'episode_id': 925470, 'episode_number': '12'},
            ],
        }
        test_qq_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text

    def test_qq_w_exclusion(self, test_qq_generic, caplog):
        """Tencent Video with discontinuous Bangumi episode IDs."""
        subject_id = 120925  # Charlotte
        subject_url_id = 'keh8jx4nea7e5w0'
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % subject_url_id,
            subject=subject_id,
            episodes=verify_episode_ids_format('541642-541653,545598')[1],
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'subject_url_id': subject_url_id,
            'subject_name': 'Charlotte',
            'episodes_count': 13,
            'test_episodes': [
                {'index': 0, 'episode_id': 541642, 'episode_number': '1'},
                {'index': 11, 'episode_id': 541653, 'episode_number': '12'},
                {'index': 12, 'episode_id': 545598, 'episode_number': '13'},
            ],
        }
        test_qq_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text
