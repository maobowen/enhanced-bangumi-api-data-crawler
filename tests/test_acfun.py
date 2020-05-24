import argparse
import pytest

from src import verify_episode_ids_format
from src.crawlers.acfun import AcFunCrawler


class TestAcFunCrawler:
    """AcFun crawler test suite."""
    _SITE_URL_PATTERN = 'https://www.acfun.cn/bangumi/aa%d'
    _crawler = AcFunCrawler()

    @staticmethod
    @pytest.fixture
    def test_acfun_generic(generic_test_helper):
        """AcFun test helper."""
        def _test_acfun_generic(source, episodes: list, test_config: dict):
            test_config['service_id'] = 'acfun.cn'
            test_config['paid'] = 0
            test_config['subject_url_id'] = str(test_config['subject_url_id'])
            test_config['subtitle_locales'] = ['zh_CN']
            test_config['remark'] = '<名称>-A站'
            test_config['episode_url_id_pattern'] = r'^(?:\d+)_(?:\d+)$'
            for test_episode_item in test_config['test_episodes']:
                test_episode_item['remark'] = 'EP%s-A站' % test_episode_item['episode_number']
                del test_episode_item['episode_number']
            generic_test_helper.test_source(source, test_config)
            generic_test_helper.test_episodes(episodes, test_config)
        return _test_acfun_generic

    def test_acfun_wo_exclusion(self, test_acfun_generic, caplog):
        """AcFun with continuous Bangumi episode IDs."""
        subject_id = 252655  # 佐贺偶像是传奇
        subject_url_id = 5022161
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % subject_url_id,
            subject=subject_id,
            episodes=verify_episode_ids_format('832417-832428')[1],
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'subject_url_id': subject_url_id,
            'episodes_count': 12,
            'test_episodes': [
                {'index': 0, 'episode_id': 832417, 'episode_number': '1'},
                {'index': 11, 'episode_id': 832428, 'episode_number': '12'},
            ],
        }
        test_acfun_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text

    def test_acfun_w_exclusion(self, test_acfun_generic, caplog):
        """AcFun with discontinuous Bangumi episode IDs."""
        subject_id = 266147  # 达尔文游戏
        subject_url_id = 6000896
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % subject_url_id,
            subject=subject_id,
            episodes=verify_episode_ids_format('925267-925270,929983,925271-925277')[1],
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'subject_url_id': subject_url_id,
            'episodes_count': 12,
            'test_episodes': [
                {'index': 0, 'episode_id': 925267, 'episode_number': '1'},
                {'index': 3, 'episode_id': 925270, 'episode_number': '4'},
                {'index': 4, 'episode_id': 929983, 'episode_number': '4.5'},
                {'index': 5, 'episode_id': 925271, 'episode_number': '5'},
                {'index': 11, 'episode_id': 925277, 'episode_number': '11'},
            ],
        }
        test_acfun_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text
