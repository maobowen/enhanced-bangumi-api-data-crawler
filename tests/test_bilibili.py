import argparse
import pytest

from src import verify_episode_ids_format
from src.crawlers.bilibili import BilibiliCrawler


class TestBilibiliCrawler:
    """Bilibili crawler test suite."""
    _SITE_URL_PATTERN = 'https://www.bilibili.com/bangumi/media/md%d/'
    _crawler = BilibiliCrawler()

    @staticmethod
    @pytest.fixture
    def test_bilibili_generic(generic_test_helper):
        """Bilibili test helper."""
        def _test_bilibili_generic(source, episodes: list, test_config: dict):
            test_config['service_id'] = 'bilibili.com_%s' % test_config['service_id_suffix']
            test_config['subject_url_id'] = str(test_config['subject_url_id'])
            test_config['subtitle_locales'] = ['zh_%s' % test_config['service_id_suffix'].upper()]
            del test_config['service_id_suffix']
            test_config['remark'] = '%s-B站%s' % (test_config['subject_name'], test_config['remark_suffix'])
            del test_config['subject_name']
            test_config['episode_url_id_pattern'] = r'^(?:BV[0-9A-Za-z]{10})(?:/index_\d+\.html)?$'
            for test_episode_item in test_config['test_episodes']:
                test_episode_item['remark'] = 'EP%s-B站%s' % (test_episode_item['episode_number'], test_config['remark_suffix'])
                del test_episode_item['episode_number']
            del test_config['remark_suffix']
            generic_test_helper.test_source(source, test_config)
            generic_test_helper.test_episodes(episodes, test_config)
        return _test_bilibili_generic

    def test_bilibili_cn_all_free_wo_exclusion(self, test_bilibili_generic, caplog):
        """Bilibili (available in mainland China) with all episodes free and continuous Bangumi episode IDs."""
        subject_id = 41488  # 樱花庄的宠物女孩
        subject_url_id = 687
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % subject_url_id,
            subject=subject_id,
            episodes=verify_episode_ids_format('193987-194010')[1],
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'service_id_suffix': 'cn',
            'paid': 0,
            'subject_url_id': subject_url_id,
            'subject_name': '樱花庄的宠物女孩',
            'remark_suffix': '大陆',
            'episodes_count': 24,
            'test_episodes': [
                {'index': 0, 'episode_id': 193987, 'episode_number': '1'},
                {'index': 23, 'episode_id': 194010, 'episode_number': '24'},
            ],
        }
        test_bilibili_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text

    def test_bilibili_cn_all_free_w_exclusion(self, test_bilibili_generic, caplog):
        """Bilibili (available in mainland China) with all episodes free and discontinuous Bangumi episode IDs."""
        subject_id = 51  # CLANNAD 第1期
        subject_url_id = 1177
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % subject_url_id,
            subject=subject_id,
            episodes=verify_episode_ids_format('92-103,533-542,37338')[1],
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'service_id_suffix': 'cn',
            'paid': 0,
            'subject_url_id': subject_url_id,
            'subject_name': 'CLANNAD',
            'remark_suffix': '大陆',
            'episodes_count': 23,
            'test_episodes': [
                {'index': 0, 'episode_id': 92, 'episode_number': '1'},
                {'index': 11, 'episode_id': 103, 'episode_number': '12'},
                {'index': 12, 'episode_id': 533, 'episode_number': '13'},
                {'index': 21, 'episode_id': 542, 'episode_number': '22'},
                {'index': 22, 'episode_id': 37338, 'episode_number': '番外篇'},
            ],
        }
        test_bilibili_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text

    def test_bilibili_cn_first_free_wo_exclusion(self, test_bilibili_generic, caplog):
        """Bilibili (available in mainland China) with only the first episode free and continuous Bangumi episode IDs."""
        subject_id = 248175  # 辉夜大小姐想让我告白 第1期
        subject_url_id = 5267730
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % subject_url_id,
            subject=subject_id,
            episodes=verify_episode_ids_format('850264-850275')[1],
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'service_id_suffix': 'cn',
            'paid': 1,
            'subject_url_id': subject_url_id,
            'subject_name': '辉夜大小姐想让我告白～天才们的恋爱头脑战～',
            'remark_suffix': '大陆',
            'episodes_count': 12,
            'test_episodes': [
                {'index': 0, 'episode_id': 850264, 'episode_number': '1'},
                {'index': 11, 'episode_id': 850275, 'episode_number': '12'},
            ],
        }
        test_bilibili_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text

    def test_bilibili_cn_first_free_w_exclusion(self, test_bilibili_generic, caplog):
        """Bilibili (available in mainland China) with only the first episode free and discontinuous Bangumi episode IDs."""
        subject_id = 207573  # 月色真美
        subject_url_id = 5989
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % subject_url_id,
            subject=subject_id,
            episodes=verify_episode_ids_format('705416-705421,719948,705422-705427')[1],
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'service_id_suffix': 'cn',
            'paid': 1,
            'subject_url_id': subject_url_id,
            'subject_name': '月色真美',
            'remark_suffix': '大陆',
            'episodes_count': 13,
            'test_episodes': [
                {'index': 0, 'episode_id': 705416, 'episode_number': '1'},
                {'index': 5, 'episode_id': 705421, 'episode_number': '6'},
                {'index': 6, 'episode_id': 719948, 'episode_number': '6.5'},
                {'index': 7, 'episode_id': 705422, 'episode_number': '7'},
                {'index': 12, 'episode_id': 705427, 'episode_number': '12'},
            ],
        }
        test_bilibili_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text

    def test_bilibili_cn_all_paid_wo_exclusion(self, test_bilibili_generic, caplog):
        """Bilibili (available in mainland China) with all episodes paid and continuous Bangumi episode IDs."""
        subject_id = 271687  # 虚构推理
        subject_url_id = 28224145
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % subject_url_id,
            subject=subject_id,
            episodes=verify_episode_ids_format('925555-925566')[1],
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'service_id_suffix': 'cn',
            'paid': 2,
            'subject_url_id': subject_url_id,
            'subject_name': '虚构推理',
            'remark_suffix': '大陆',
            'episodes_count': 12,
            'test_episodes': [
                {'index': 0, 'episode_id': 925555, 'episode_number': '1'},
                {'index': 11, 'episode_id': 925566, 'episode_number': '12'},
            ],
        }
        test_bilibili_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text

    def test_bilibili_cn_all_paid_w_exclusion(self, test_bilibili_generic, caplog):
        """Bilibili (available in mainland China) with all episodes paid and discontinuous Bangumi episode IDs."""
        subject_id = 263771  # 美妙射击部
        subject_url_id = 28222731
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % subject_url_id,
            subject=subject_id,
            episodes=verify_episode_ids_format('908267-908273,919810,908274-908278')[1],
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'service_id_suffix': 'cn',
            'paid': 2,
            'subject_url_id': subject_url_id,
            'subject_name': '美妙射击部',
            'remark_suffix': '大陆',
            'episodes_count': 13,
            'test_episodes': [
                {'index': 0, 'episode_id': 908267, 'episode_number': '1'},
                {'index': 6, 'episode_id': 908273, 'episode_number': '7'},
                {'index': 7, 'episode_id': 919810, 'episode_number': '7.5'},
                {'index': 8, 'episode_id': 908274, 'episode_number': '8'},
                {'index': 12, 'episode_id': 908278, 'episode_number': '12'},
            ],
        }
        test_bilibili_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text

    def test_bilibili_hk_all_free(self, test_bilibili_generic, caplog):
        """Bilibili (only available in Hong Kong) with all episodes free."""
        subject_id = 266455  # 水果篮子 第1期
        subject_url_id = 26341584
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % subject_url_id,
            subject=subject_id,
            episodes=verify_episode_ids_format('873545-873553,874066-874068,880603-880615')[1],
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'service_id_suffix': 'hk',
            'paid': 0,
            'subject_url_id': subject_url_id,
            'subject_name': '生肖奇缘 (2019)（僅限港澳地區）',
            'remark_suffix': '香港',
            'episodes_count': 25,
            'test_episodes': [
                {'index': 0, 'episode_id': 873545, 'episode_number': '1'},
                {'index': 8, 'episode_id': 873553, 'episode_number': '9'},
                {'index': 9, 'episode_id': 874066, 'episode_number': '10'},
                {'index': 11, 'episode_id': 874068, 'episode_number': '12'},
                {'index': 12, 'episode_id': 880603, 'episode_number': '13'},
                {'index': 24, 'episode_id': 880615, 'episode_number': '25'},
            ],
        }
        test_bilibili_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text

    def test_bilibili_tw_all_free(self, test_bilibili_generic, caplog):
        """Bilibili (only available in Taiwan) with all episodes free."""
        subject_id = 279457  # 刀剑神域 第3期第2部
        subject_url_id = 28222854
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % subject_url_id,
            subject=subject_id,
            episodes=verify_episode_ids_format('906496,905519-905530')[1],
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'service_id_suffix': 'hk',
            'paid': 0,
            'subject_url_id': subject_url_id,
            'subject_name': '刀劍神域 Alicization War of Underworld（僅限台灣地區）',
            'remark_suffix': '台湾',
            'episodes_count': 13,
            'test_episodes': [
                {'index': 0, 'episode_id': 906496, 'episode_number': '0'},
                {'index': 1, 'episode_id': 905519, 'episode_number': '1'},
                {'index': 12, 'episode_id': 905530, 'episode_number': '12'},
            ],
        }
        test_bilibili_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text

    def test_bilibili_hktw_all_free(self, test_bilibili_generic, caplog):
        """Bilibili (only available outside mainland China) with all episodes free."""
        subject_id = 76325  # 约会大作战 第2期
        subject_url_id = 4187
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % subject_url_id,
            subject=subject_id,
            episodes=verify_episode_ids_format('373616-373625')[1],
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'service_id_suffix': 'hk',
            'paid': 0,
            'subject_url_id': subject_url_id,
            'subject_name': '約會大作戰 第二季 （僅限港澳台地區）',
            'remark_suffix': '港台',
            'episodes_count': 10,
            'test_episodes': [
                {'index': 0, 'episode_id': 373616, 'episode_number': '1'},
                {'index': 9, 'episode_id': 373625, 'episode_number': '10'},
            ],
        }
        test_bilibili_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text

    def test_bilibili_hktw_first_free(self, test_bilibili_generic, caplog):
        """Bilibili (only available outside mainland China) with only the first episode free."""
        subject_id = 285776  # ID:INVADED
        subject_url_id = 28226764
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % subject_url_id,
            subject=subject_id,
            episodes=verify_episode_ids_format('925327-925338,927005')[1],
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'service_id_suffix': 'hk',
            'paid': 1,
            'subject_url_id': subject_url_id,
            'subject_name': 'ID:INVADED（僅限港澳台地區）',
            'remark_suffix': '港台',
            'episodes_count': 13,
            'test_episodes': [
                {'index': 0, 'episode_id': 925327, 'episode_number': '1'},
                {'index': 11, 'episode_id': 925338, 'episode_number': '12'},
                {'index': 12, 'episode_id': 927005, 'episode_number': '13'},
            ],
        }
        test_bilibili_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text
