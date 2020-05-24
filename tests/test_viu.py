import argparse
import pytest

from src import verify_episode_ids_format
from src.crawlers.viu import ViuCrawler


class TestViuCrawler:
    """Viu crawler test suite."""
    _SITE_URL_PATTERN = 'https://www.viu.com/ott/%s/%s/vod/%d/'
    _crawler = ViuCrawler()

    @staticmethod
    @pytest.fixture
    def test_viu_generic(generic_test_helper):
        """Viu test helper."""
        def _test_viu_generic(source, episodes: list, test_config: dict):
            test_config['service_id'] = 'viu.com_%s' % test_config['service_id_suffix']
            test_config['subject_url_id'] = str(test_config['subject_url_id'])
            test_config['remark'] = '%s-Viu%s' % (test_config['subject_name'], test_config['service_id_suffix'].upper())
            del test_config['subject_name']
            test_config['episode_url_id_pattern'] = r'^(\d+)$'
            for test_episode_item in test_config['test_episodes']:
                test_episode_item['remark'] = 'EP%s-Viu%s' % (test_episode_item['episode_number'], test_config['service_id_suffix'].upper())
                del test_episode_item['episode_number']
            del test_config['service_id_suffix']
            generic_test_helper.test_source(source, test_config)
            generic_test_helper.test_episodes(episodes, test_config)
        return _test_viu_generic

    def test_viu_hk_wo_exclusion(self, test_viu_generic, caplog):
        """Viu (Hong Kong) with continuous Bangumi episode IDs."""
        subject_id = 213816  # ReLIFE 完结篇
        subject_url_id = 93680
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % ('hk', 'zh-hk', subject_url_id),
            subject=subject_id,
            episodes=verify_episode_ids_format('715691-715694')[1],
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'service_id_suffix': 'hk',
            'paid': 0,
            'subject_url_id': subject_url_id,
            'subtitle_locales': ['zh_HK'],
            'subject_name': 'ReLIFE 重返17歲',
            'episodes_count': 4,
            'test_episodes': [
                {'index': 0, 'episode_id': 715691, 'episode_number': '14'},
                {'index': 3, 'episode_id': 715694, 'episode_number': '17'},
            ],
        }
        test_viu_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text

    def test_viu_hk_w_exclusion(self, test_viu_generic, caplog):
        """Viu (Hong Kong) with discontinuous Bangumi episode IDs."""
        subject_id = 218708  # 比宇宙更远的地方
        subject_url_id = 71929
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % ('hk', 'zh-hk', subject_url_id),
            subject=subject_id,
            episodes=verify_episode_ids_format('766525-766536,769893')[1],
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'service_id_suffix': 'hk',
            'paid': 0,
            'subject_url_id': subject_url_id,
            'subtitle_locales': ['zh_HK'],
            'subject_name': '比宇宙更遠的地方',
            'episodes_count': 13,
            'test_episodes': [
                {'index': 0, 'episode_id': 766525, 'episode_number': '1'},
                {'index': 11, 'episode_id': 766536, 'episode_number': '12'},
                {'index': 12, 'episode_id': 769893, 'episode_number': '13'},
            ],
        }
        test_viu_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text
