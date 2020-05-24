import argparse
import pytest

from src import verify_episode_ids_format
from src.crawlers.animad import AnimadCrawler


class TestAnimadCrawler:
    """Animad crawler test suite."""
    _SITE_URL_PATTERN = 'https://acg.gamer.com.tw/acgDetail.php?s=%d'
    _crawler = AnimadCrawler()

    @staticmethod
    @pytest.fixture
    def test_animad_generic(generic_test_helper):
        """Animad test helper."""
        def _test_animad_generic(source, episodes: list, test_config: dict):
            test_config['service_id'] = 'ani.gamer.com.tw'
            test_config['paid'] = 0
            test_config['subject_url_id'] = str(test_config['subject_url_id'])
            test_config['subtitle_locales'] = ['zh_HK']
            test_config['remark'] = '%s-动画疯' % test_config['subject_name']
            del test_config['subject_name']
            test_config['episode_url_id_pattern'] = r'^(?:\d+)$'
            for test_episode_item in test_config['test_episodes']:
                test_episode_item['remark'] = 'EP%s-动画疯' % test_episode_item['episode_number']
                del test_episode_item['episode_number']
            generic_test_helper.test_source(source, test_config)
            generic_test_helper.test_episodes(episodes, test_config)
        return _test_animad_generic

    def test_animad_wo_exclusion(self, test_animad_generic, caplog):
        """Animad with continuous Bangumi episode IDs."""
        subject_id = 285482  # 异种族风俗娘评鉴指南
        subject_url_id = 106302
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % subject_url_id,
            subject=subject_id,
            episodes=verify_episode_ids_format('925252-925263')[1],
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'subject_url_id': subject_url_id,
            'subject_name': '異種族風俗娘評鑑指南',
            'episodes_count': 12,
            'test_episodes': [
                {'index': 0, 'episode_id': 925252, 'episode_number': '1'},
                {'index': 11, 'episode_id': 925263, 'episode_number': '12'},
            ],
        }
        test_animad_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text

    def test_animad_w_exclusion(self, test_animad_generic, caplog):
        """Animad with discontinuous Bangumi episode IDs."""
        subject_id = 27364  # 冰菓
        subject_url_id = 53316
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % subject_url_id,
            subject=subject_id,
            episodes=verify_episode_ids_format('152243-152253,183486,152254-152263,195723')[1],
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'subject_url_id': subject_url_id,
            'subject_name': '冰菓',
            'episodes_count': 23,
            'test_episodes': [
                {'index': 0, 'episode_id': 152243, 'episode_number': '1'},
                {'index': 10, 'episode_id': 152253, 'episode_number': '11'},
                {'index': 11, 'episode_id': 183486, 'episode_number': '11.5'},
                {'index': 12, 'episode_id': 152254, 'episode_number': '12'},
                {'index': 21, 'episode_id': 152263, 'episode_number': '21'},
                {'index': 22, 'episode_id': 195723, 'episode_number': '22'},
            ],
        }
        test_animad_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text
