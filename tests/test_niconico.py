import argparse
import pytest

from src import verify_episode_ids_format
from src.crawlers.niconico import NiconicoCrawler


class TestNiconicoCrawler:
    """Niconico crawler test suite."""
    _SITE_URL_PATTERN = 'https://ch.nicovideo.jp/channel/ch%d'
    _crawler = NiconicoCrawler()

    @staticmethod
    @pytest.fixture
    def test_niconico_generic(generic_test_helper):
        """Niconico test helper."""
        def _test_niconico_generic(source, episodes: list, test_config: dict):
            test_config['service_id'] = 'nicovideo.jp'
            test_config['subject_url_id'] = str(test_config['subject_url_id'])
            test_config['subtitle_locales'] = ['ja_JP']
            test_config['remark'] = '%s-niconico' % test_config['subject_name']
            del test_config['subject_name']
            test_config['episode_url_id_pattern'] = r'^(?:\d+)$'
            for test_episode_item in test_config['test_episodes']:
                test_episode_item['remark'] = 'EP%s-niconico' % test_episode_item['episode_number']
                del test_episode_item['episode_number']
            generic_test_helper.test_source(source, test_config)
            generic_test_helper.test_episodes(episodes, test_config)
        return _test_niconico_generic

    def test_niconico_all_free_wo_exclusion(self, test_niconico_generic, caplog):
        """Niconico with all episodes free and continuous Bangumi episode IDs."""
        subject_id = 275610  # 洗浴服务！～我和那家伙在女浴池！？～
        subject_url_id = 2640684
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % subject_url_id,
            subject=subject_id,
            episodes=verify_episode_ids_format('874181-874188')[1],
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'paid': 0,
            'subject_url_id': subject_url_id,
            'subject_name': '洗い屋さん！ 俺とアイツが女湯で！？',
            'episodes_count': 8,
            'test_episodes': [
                {'index': 0, 'episode_id': 874181, 'episode_number': '1'},
                {'index': 7, 'episode_id': 874188, 'episode_number': '8'},
            ],
        }
        test_niconico_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text

    def test_niconico_first_free_wo_exclusion(self, test_niconico_generic, caplog):
        """Niconico with only the first episode free and continuous Bangumi episode IDs."""
        subject_id = 265708  # 女高中生的虚度日常
        subject_url_id = 2641467
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % subject_url_id,
            subject=subject_id,
            episodes=verify_episode_ids_format('893730-893741')[1],
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'paid': 1,
            'subject_url_id': subject_url_id,
            'subject_name': '女子高生の無駄づかい',
            'episodes_count': 12,
            'test_episodes': [
                {'index': 0, 'episode_id': 893730, 'episode_number': '1'},
                {'index': 11, 'episode_id': 893741, 'episode_number': '12'},
            ],
        }
        test_niconico_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text

    def test_niconico_first_free_w_exclusion(self, test_niconico_generic, caplog):
        """Niconico with only the first episode free and discontinuous Bangumi episode IDs."""
        subject_id = 279457  # 刀剑神域 第3期第2部
        subject_url_id = 2642735
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % subject_url_id,
            subject=subject_id,
            episodes=verify_episode_ids_format('906496,905519-905530')[1],
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'paid': 1,
            'subject_url_id': subject_url_id,
            'subject_name': 'ソードアート・オンライン アリシゼーション War of Underworld',
            'episodes_count': 13,
            'test_episodes': [
                {'index': 0, 'episode_id': 906496, 'episode_number': '(?:.*)', 'is_remark_regex': True},
                {'index': 1, 'episode_id': 905519, 'episode_number': '01'},
                {'index': 12, 'episode_id': 905530, 'episode_number': '12'},
            ],
        }
        test_niconico_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text

    def test_niconico_all_paid_wo_exclusion(self, test_niconico_generic, caplog):
        """Niconico with all episodes paid and continuous Bangumi episode IDs."""
        subject_id = 271151  # 擅长捉弄的高木同学 第2期
        subject_url_id = 2641473
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % subject_url_id,
            subject=subject_id,
            episodes=verify_episode_ids_format('893874-893885')[1],
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'paid': 2,
            'subject_url_id': subject_url_id,
            'subject_name': 'からかい上手の高木さん２',
            'episodes_count': 12,
            'test_episodes': [
                {'index': 0, 'episode_id': 893874, 'episode_number': '1'},
                {'index': 11, 'episode_id': 893885, 'episode_number': '12'},
            ],
        }
        test_niconico_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text

    def test_niconico_all_paid_w_exclusion(self, test_niconico_generic, caplog):
        """Niconico with all episodes paid and discontinuous Bangumi episode IDs."""
        subject_id = 159795  # 恋爱暴君
        subject_url_id = 2630737
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % subject_url_id,
            subject=subject_id,
            episodes=verify_episode_ids_format('705488-705491,,705492-705494,,705495-705496,,705497-705498,,705499')[1],
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'paid': 2,
            'subject_url_id': subject_url_id,
            'subject_name': '恋愛暴君',
            'episodes_count': 16,
            'test_episodes': [
                {'index': 0, 'episode_id': 705488, 'episode_number': '1'},
                {'index': 3, 'episode_id': 705491, 'episode_number': '4'},
                {'index': 4, 'episode_id': -1, 'episode_number': '(?:.*)', 'is_remark_regex': True},
                {'index': 8, 'episode_id': -1, 'episode_number': '(?:.*)', 'is_remark_regex': True},
                {'index': 11, 'episode_id': -1, 'episode_number': '(?:.*)', 'is_remark_regex': True},
                {'index': 13, 'episode_id': 705498, 'episode_number': '11'},
                {'index': 14, 'episode_id': -1, 'episode_number': '(?:.*)', 'is_remark_regex': True},
                {'index': 15, 'episode_id': 705499, 'episode_number': '12', 'is_remark_regex': True},
            ],
        }
        test_niconico_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text
