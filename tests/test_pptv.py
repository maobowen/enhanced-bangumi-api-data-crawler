import argparse
import pytest

from src import verify_episode_ids_format
from src.crawlers.pptv import PPTVCrawler


class TestPPTVCrawler:
    """PPTV crawler test suite."""
    _SITE_URL_PATTERN = 'https://v.pptv.com/page/%s.html'
    _crawler = PPTVCrawler()

    @staticmethod
    @pytest.fixture
    def test_pptv_generic(generic_test_helper):
        """PPTV test helper."""
        def _test_pptv_generic(source, episodes: list, test_config: dict):
            test_config['service_id'] = 'pptv.com'
            test_config['subtitle_locales'] = ['zh_CN']
            test_config['remark'] = '%s-PP视频' % test_config['subject_name']
            del test_config['subject_name']
            test_config['episode_url_id_pattern'] = r'^(?:\w+)$'
            for test_episode_item in test_config['test_episodes']:
                test_episode_item['remark'] = 'EP%s-PP视频' % test_episode_item['episode_number']
                del test_episode_item['episode_number']
            generic_test_helper.test_source(source, test_config)
            generic_test_helper.test_episodes(episodes, test_config)
        return _test_pptv_generic

    def test_pptv_all_free_wo_exclusion(self, test_pptv_generic, caplog):
        """PPTV with all episodes free and continuous Bangumi episode IDs."""
        subject_id = 195229  # 清恋
        subject_url_id = 'fciakIorwYJ4Bfibc'
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % subject_url_id,
            subject=subject_id,
            episodes=verify_episode_ids_format('682004-682015')[1],
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'paid': 0,
            'subject_url_id': subject_url_id,
            'subject_name': '清恋',
            'episodes_count': 12,
            'test_episodes': [
                {'index': 0, 'episode_id': 682004, 'episode_number': '1'},
                {'index': 11, 'episode_id': 682015, 'episode_number': '12'},
            ],
        }
        test_pptv_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text

    def test_pptv_all_free_w_exclusion(self, test_pptv_generic, caplog):
        """PPTV with all episodes free and discontinuous Bangumi episode IDs."""
        subject_id = 126173  # ReLIFE
        subject_url_id = 'admzMZnicb60QjvY'
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % subject_url_id,
            subject=subject_id,
            episodes=verify_episode_ids_format('642058-642069,642497')[1],
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'paid': 0,
            'subject_url_id': subject_url_id,
            'subject_name': 'ReLIFE',
            'episodes_count': 13,
            'test_episodes': [
                {'index': 0, 'episode_id': 642058, 'episode_number': '1'},
                {'index': 11, 'episode_id': 642069, 'episode_number': '12'},
                {'index': 12, 'episode_id': 642497, 'episode_number': '13'},
            ],
        }
        test_pptv_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text

    def test_pptv_first_free_wo_exclusion(self, test_pptv_generic, caplog):
        """PPTV with only the first episode free and continuous Bangumi episode IDs."""
        subject_id = 144357  # 文豪野犬 第1期
        subject_url_id = 'Fjchnwdt3RtibicGQ'
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % subject_url_id,
            subject=subject_id,
            episodes=verify_episode_ids_format('617287-617298')[1],
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'paid': 1,
            'subject_url_id': subject_url_id,
            'subject_name': '文豪野犬',
            'episodes_count': 12,
            'test_episodes': [
                {'index': 0, 'episode_id': 617287, 'episode_number': '1'},
                {'index': 11, 'episode_id': 617298, 'episode_number': '12'},
            ],
        }
        test_pptv_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text
