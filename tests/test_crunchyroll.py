import argparse
import pytest

from src import verify_episode_ids_format
from src.crawlers.crunchyroll import CrunchyrollCrawler


class TestCrunchyrollCrawler:
    """Crunchyroll crawler test suite."""
    _SITE_URL_PATTERN = 'https://www.crunchyroll.com/%s'
    _crawler = CrunchyrollCrawler()

    @staticmethod
    @pytest.fixture
    def test_crunchyroll_generic(generic_test_helper):
        """Crunchyroll test helper."""
        def _test_crunchyroll_generic(source, episodes: list, test_config: dict):
            test_config['service_id'] = 'crunchyroll.com'
            test_config['remark'] = '%s-Crunchyroll' % test_config['subject_name']
            del test_config['subject_name']
            test_config['episode_url_id_pattern'] = r'^(\d+)$'
            for test_episode_item in test_config['test_episodes']:
                test_episode_item['remark'] = 'EP%s-Crunchyroll' % test_episode_item['episode_number']
                del test_episode_item['episode_number']
            generic_test_helper.test_source(source, test_config)
            generic_test_helper.test_episodes(episodes, test_config)
        return _test_crunchyroll_generic

    def test_crunchyroll_single_collection_all_free_wo_exclusion(self, test_crunchyroll_generic, caplog):
        """Crunchyroll with single collection, all episodes free and continuous Bangumi episode IDs."""
        subject_id = 47889  # 来自风平浪静的明天
        subject_url_id = 'nagi-no-asukara-nagi-asu-a-lull-in-the-sea'
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % subject_url_id,
            subject=subject_id,
            episodes=verify_episode_ids_format('322501-322526')[1],
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'paid': 0,
            'subject_url_id': subject_url_id,
            'subtitle_locales': ['en_US'],
            'subject_name': 'Nagi no Asukara (Nagi-Asu: A Lull in the Sea)',
            'episodes_count': 26,
            'test_episodes': [
                {'index': 0, 'episode_id': 322501, 'episode_number': '1'},
                {'index': 25, 'episode_id': 322526, 'episode_number': '26'},
            ],
        }
        test_crunchyroll_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text

    def test_crunchyroll_single_collection_all_free_w_exclusion(self, test_crunchyroll_generic, caplog):
        """Crunchyroll with single collection, all episodes free and discontinuous Bangumi episode IDs."""
        subject_id = 207573  # 月色真美
        subject_url_id = 'tsukigakirei'
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % subject_url_id,
            subject=subject_id,
            episodes=verify_episode_ids_format('705416-705421,719948,705422-705427')[1],
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'paid': 0,
            'subject_url_id': subject_url_id,
            'subtitle_locales': ['ar_SA', 'de_DE', 'en_US', 'es_ES', 'es_MX', 'fr_FR', 'it_IT', 'pt_BR'],
            'subject_name': 'Tsukigakirei',
            'episodes_count': 13,
            'test_episodes': [
                {'index': 0, 'episode_id': 705416, 'episode_number': '1'},
                {'index': 5, 'episode_id': 705421, 'episode_number': '6'},
                {'index': 6, 'episode_id': 719948, 'episode_number': '6.5'},
                {'index': 7, 'episode_id': 705422, 'episode_number': '7'},
                {'index': 12, 'episode_id': 705427, 'episode_number': '12'},
            ],
        }
        test_crunchyroll_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text

    def test_crunchyroll_single_collection_first_free_wo_exclusion(self, test_crunchyroll_generic, caplog):
        """Crunchyroll with single collection, only the first episode free and continuous Bangumi episode IDs."""
        subject_id = 1760  # 夏娃的时间
        subject_url_id = 'time-of-eve'
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % subject_url_id,
            subject=subject_id,
            episodes=verify_episode_ids_format('7536-7541')[1],
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'paid': 1,
            'subject_url_id': subject_url_id,
            'subtitle_locales': ['de_DE', 'en_US', 'es_MX', 'it_IT', 'pt_BR'],
            'subject_name': 'Time of Eve',
            'episodes_count': 6,
            'test_episodes': [
                {'index': 0, 'episode_id': 7536, 'episode_number': '1'},
                {'index': 5, 'episode_id': 7541, 'episode_number': '6'},
            ],
        }
        test_crunchyroll_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text

    def test_crunchyroll_single_collection_all_paid_wo_exclusion(self, test_crunchyroll_generic, caplog):
        """Crunchyroll with single collection, only the first episode free and discontinuous Bangumi episode IDs."""
        subject_id = 7157  # 缘之空
        subject_url_id = 'yosuga-no-sora-in-solitude-where-we-are-least-alone'
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % subject_url_id + '?skip_wall=1',
            subject=subject_id,
            episodes=verify_episode_ids_format('52323-52334')[1],
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'paid': 2,
            'subject_url_id': subject_url_id,
            'subtitle_locales': [],
            'subject_name': 'Yosuga no Sora: In Solitude Where We are Least Alone',
            'episodes_count': 12,
            'test_episodes': [
                {'index': 0, 'episode_id': 52323, 'episode_number': '1'},
                {'index': 11, 'episode_id': 52334, 'episode_number': '12'},
            ],
        }
        test_crunchyroll_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text

    def test_crunchyroll_multiple_collections_all_free_wo_exclusion(self, test_crunchyroll_generic, caplog):
        """Crunchyroll with multiple collections, all episodes free and continuous Bangumi episode IDs."""
        subject_id = 101442  # 悠哉日常大王 第2期
        subject_url_id = 'non-non-biyori'
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % subject_url_id,
            subject=subject_id,
            episodes=verify_episode_ids_format('538096-538107')[1],
            cr_collection=22331,
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'paid': 0,
            'subject_url_id': subject_url_id,
            'subtitle_locales': ['ar_SA', 'de_DE', 'en_US', 'es_ES', 'es_MX', 'fr_FR', 'it_IT', 'pt_BR'],
            'subject_name': 'Non Non Biyori Repeat',
            'episodes_count': 12,
            'test_episodes': [
                {'index': 0, 'episode_id': 538096, 'episode_number': '1'},
                {'index': 11, 'episode_id': 538107, 'episode_number': '12'},
            ],
        }
        test_crunchyroll_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text

    def test_crunchyroll_multiple_collections_all_free_w_exclusion(self, test_crunchyroll_generic, caplog):
        """Crunchyroll with multiple collections, all episodes free and discontinuous Bangumi episode IDs."""
        subject_id = 78405  # 悠哉日常大王 第1期
        subject_url_id = 'non-non-biyori'
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % subject_url_id,
            subject=subject_id,
            episodes=verify_episode_ids_format('319289-319299,320742')[1],
            cr_collection=21335,
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'paid': 0,
            'subject_url_id': subject_url_id,
            'subtitle_locales': ['ar_SA', 'de_DE', 'en_US', 'es_ES', 'es_MX', 'fr_FR', 'it_IT', 'pt_BR'],
            'subject_name': 'Non Non Biyori',
            'episodes_count': 12,
            'test_episodes': [
                {'index': 0, 'episode_id': 319289, 'episode_number': '1'},
                {'index': 10, 'episode_id': 319299, 'episode_number': '11'},
                {'index': 11, 'episode_id': 320742, 'episode_number': '12'},
            ],
        }
        test_crunchyroll_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text

    def test_crunchyroll_multiple_collections_all_paid_wo_exclusion(self, test_crunchyroll_generic, caplog):
        """Crunchyroll with multiple collections, all episodes paid and continuous Bangumi episode IDs."""
        subject_id = 119889  # 我老婆是学生会长 第1期
        subject_url_id = 'my-wife-is-the-student-council-president'
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % subject_url_id + '?skip_wall=1',
            subject=subject_id,
            episodes=verify_episode_ids_format('533935-533946')[1],
            cr_collection=22357,
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'paid': 2,
            'subject_url_id': subject_url_id,
            'subtitle_locales': [],
            'subject_name': 'My Wife is the Student Council President (Uncensored)',
            'episodes_count': 12,
            'test_episodes': [
                {'index': 0, 'episode_id': 533935, 'episode_number': '1'},
                {'index': 11, 'episode_id': 533946, 'episode_number': '12'},
            ],
        }
        test_crunchyroll_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text

    def test_crunchyroll_multiple_collections_all_paid_w_exclusion(self, test_crunchyroll_generic, caplog):
        """Crunchyroll with multiple collections, all episodes paid and discontinuous Bangumi episode IDs."""
        subject_id = 1998  # 金属对决 战斗陀螺 第3期
        subject_url_id = 'beyblade-metal-fusion'
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % subject_url_id,
            subject=subject_id,
            episodes=verify_episode_ids_format('22912-22916,137249-137255')[1],
            cr_collection=22595,
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'paid': 2,
            'subject_url_id': subject_url_id,
            'subtitle_locales': [],
            'subject_name': 'Beyblade: Metal Fusion Season 3',
            'episodes_count': 12,
            'test_episodes': [
                {'index': 0, 'episode_id': 22912, 'episode_number': '1'},
                {'index': 4, 'episode_id': 22916, 'episode_number': '5'},
                {'index': 5, 'episode_id': 137249, 'episode_number': '6'},
                {'index': 11, 'episode_id': 137255, 'episode_number': '12'},
            ],
        }
        test_crunchyroll_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text
