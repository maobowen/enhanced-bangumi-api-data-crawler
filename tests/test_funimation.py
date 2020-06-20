import argparse
import pytest

from src import verify_episode_ids_format
from src.crawlers.funimation import FunimationCrawler


class TestFunimationCrawler:
    """Funimation crawler test suite."""
    _SITE_URL_PATTERN = 'https://www.funimation.com/shows/%d/'
    _crawler = FunimationCrawler()

    @staticmethod
    @pytest.fixture
    def test_funimation_generic(generic_test_helper):
        """Funimation test helper."""
        def _test_funimation_generic(source, episodes: list, test_config: dict):
            test_config['service_id'] = 'funimation.com'
            test_config['subtitle_locales'] = ['en_US']
            test_config['remark'] = '%s-Funimation' % test_config['subject_name']
            del test_config['subject_name']
            test_config['episode_url_id_pattern'] = r'^([\w|\-]+)$'
            for test_episode_item in test_config['test_episodes']:
                test_episode_item['remark'] = 'EP%s-Funimation' % test_episode_item['episode_number']
                del test_episode_item['episode_number']
            generic_test_helper.test_source(source, test_config)
            generic_test_helper.test_episodes(episodes, test_config)
        return _test_funimation_generic

    def test_funimation_single_season_all_free_wo_exclusion(self, test_funimation_generic, caplog):
        """Funimation with single season, all episodes free and continuous Bangumi episode IDs."""
        subject_id = 1851  # Angel Beats!
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % 1007443,
            subject=subject_id,
            episodes=verify_episode_ids_format('24834-24846')[1],
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'paid': 0,
            'subject_url_id': 'angel-beats',
            'subject_name': 'Angel Beats!',
            'episodes_count': 13,
            'test_episodes': [
                {'index': 0, 'episode_id': 24834, 'episode_number': '1'},
                {'index': 12, 'episode_id': 24846, 'episode_number': '13'},
            ],
        }
        test_funimation_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text

    def test_funimation_single_season_all_free_w_exclusion(self, test_funimation_generic, caplog):
        """Funimation with single season, all episodes free and discontinuous Bangumi episode IDs."""
        subject_id = 240038  # 青春猪头少年不会梦到兔女郎学姐
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % 594358,
            subject=subject_id,
            episodes=verify_episode_ids_format('831366-831377,834292')[1],
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'paid': 0,
            'subject_url_id': 'rascal-does-not-dream-of-bunny-girl-senpai',
            'subject_name': 'Rascal Does Not Dream of Bunny Girl Senpai',
            'episodes_count': 13,
            'test_episodes': [
                {'index': 0, 'episode_id': 831366, 'episode_number': '1'},
                {'index': 11, 'episode_id': 831377, 'episode_number': '12'},
                {'index': 12, 'episode_id': 834292, 'episode_number': '13'},
            ],
        }
        test_funimation_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text

    def test_funimation_single_season_all_paid_wo_exclusion(self, test_funimation_generic, caplog):
        """Funimation with single season, all episodes paid and continuous Bangumi episode IDs."""
        subject_id = 47889  # 来自风平浪静的明天
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % 1085447,
            subject=subject_id,
            episodes=verify_episode_ids_format('322501-322526')[1],
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'paid': 2,
            'subject_url_id': 'a-lull-in-the-sea',
            'subject_name': 'A Lull in the Sea',
            'episodes_count': 26,
            'test_episodes': [
                {'index': 0, 'episode_id': 322501, 'episode_number': '1'},
                {'index': 25, 'episode_id': 322526, 'episode_number': '26'},
            ],
        }
        test_funimation_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text

    def test_funimation_single_season_all_paid_w_exclusion(self, test_funimation_generic, caplog):
        """Funimation with single season, all episodes paid and discontinuous Bangumi episode IDs."""
        subject_id = 909  # 龙与虎
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % 1085444,
            subject=subject_id,
            episodes=verify_episode_ids_format('1026,1708-1730,2709')[1],
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'paid': 2,
            'subject_url_id': 'toradora',
            'subject_name': 'Toradora!',
            'episodes_count': 25,
            'test_episodes': [
                {'index': 0, 'episode_id': 1026, 'episode_number': '1'},
                {'index': 1, 'episode_id': 1708, 'episode_number': '2'},
                {'index': 23, 'episode_id': 1730, 'episode_number': '24'},
                {'index': 24, 'episode_id': 2709, 'episode_number': '25'},
            ],
        }
        test_funimation_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text

    def test_funimation_multiple_seasons_all_free_wo_exclusion(self, test_funimation_generic, caplog):
        """Funimation with multiple seasons, all episodes free and continuous Bangumi episode IDs."""
        subject_id = 23686  # 刀剑神域 第1期
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % 594522,
            subject=subject_id,
            episodes=verify_episode_ids_format('176903-176927')[1],
            funi_season=603153,
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'paid': 0,
            'subject_url_id': 'sword-art-online',
            'subject_name': 'Sword Art Online Season 1',
            'episodes_count': 25,
            'test_episodes': [
                {'index': 0, 'episode_id': 176903, 'episode_number': '1'},
                {'index': 24, 'episode_id': 176927, 'episode_number': '25'},
            ],
        }
        test_funimation_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text

    def test_funimation_multiple_seasons_all_free_w_exclusion(self, test_funimation_generic, caplog):
        """Funimation with multiple seasons, all episodes free and discontinuous Bangumi episode IDs."""
        subject_id = 92382  # 刀剑神域 第2期
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % 594522,
            subject=subject_id,
            episodes=verify_episode_ids_format('409988-410011,436747')[1],
            funi_season=603154,
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'paid': 0,
            'subject_url_id': 'sword-art-online',
            'subject_name': 'Sword Art Online Season 2',
            'episodes_count': 25,
            'test_episodes': [
                {'index': 0, 'episode_id': 409988, 'episode_number': '1'},
                {'index': 23, 'episode_id': 410011, 'episode_number': '23'},
                {'index': 24, 'episode_id': 436747, 'episode_number': '24'},
            ],
        }
        test_funimation_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text
