import argparse
import pytest

from src import verify_episode_ids_format
from src.crawlers.iqiyi import IqiyiCrawler


class TestIqiyiCrawler:
    """iQIYI crawler test suite."""
    _SITE_URL_PATTERN = 'https://%s.iqiyi.com/%s.html'
    _crawler = IqiyiCrawler()

    @staticmethod
    @pytest.fixture
    def test_iqiyi_generic(generic_test_helper):
        """iQIYI test helper."""
        def _test_iqiyi_generic(source, episodes: list, test_config: dict):
            test_config['service_id'] = '%siqiyi.com' % test_config['service_id_prefix']
            del test_config['service_id_prefix']
            test_config['subtitle_locales'] = ['zh_%s' % test_config['locale_suffix']]
            del test_config['locale_suffix']
            test_config['remark'] = '%s-%s' % (test_config['subject_name'], test_config['remark_suffix'])
            del test_config['subject_name']
            test_config['episode_url_id_pattern'] = r'^(?:v_[0-9a-z]{10})$'
            for test_episode_item in test_config['test_episodes']:
                test_episode_item['remark'] = 'EP%s-%s' % (test_episode_item['episode_number'], test_config['remark_suffix'])
                del test_episode_item['episode_number']
            del test_config['remark_suffix']
            generic_test_helper.test_source(source, test_config)
            generic_test_helper.test_episodes(episodes, test_config)
        return _test_iqiyi_generic

    def test_iqiyi_cn_all_free_wo_exclusion(self, test_iqiyi_generic, caplog):
        """iQiyi (mainland China site) with all episodes free and continuous Bangumi episode IDs."""
        subject_id = 260619  # 暗黑破坏神在身边
        subject_url_id = 'a_19rrhy0utp'
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % ('www', subject_url_id),
            subject=subject_id,
            episodes=verify_episode_ids_format('925567-925578')[1],
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'service_id_prefix': '',
            'paid': 0,
            'subject_url_id': subject_url_id,
            'locale_suffix': 'CN',
            'subject_name': '暗黑破坏神在身边',
            'remark_suffix': '爱奇艺',
            'episodes_count': 12,
            'test_episodes': [
                {'index': 0, 'episode_id': 925567, 'episode_number': '1'},
                {'index': 11, 'episode_id': 925578, 'episode_number': '12'},
            ],
        }
        test_iqiyi_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text

    def test_iqiyi_cn_all_free_w_exclusion(self, test_iqiyi_generic, caplog):
        """iQiyi (mainland China site) with all episodes free and discontinuous Bangumi episode IDs."""
        subject_id = 54433  # 我的青春恋爱物语果然有问题 第1期
        subject_url_id = 'a_19rrhb343l'
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % ('www', subject_url_id),
            subject=subject_id,
            episodes=verify_episode_ids_format('254896-254907,281982')[1],
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'service_id_prefix': '',
            'paid': 0,
            'subject_url_id': subject_url_id,
            'locale_suffix': 'CN',
            'subject_name': '我的青春恋爱物语果然有问题',
            'remark_suffix': '爱奇艺',
            'episodes_count': 13,
            'test_episodes': [
                {'index': 0, 'episode_id': 254896, 'episode_number': '1'},
                {'index': 11, 'episode_id': 254907, 'episode_number': '12'},
                {'index': 12, 'episode_id': 281982, 'episode_number': '13'},
            ],
        }
        test_iqiyi_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text

    def test_iqiyi_cn_first_free_w_exclusion(self, test_iqiyi_generic, caplog):
        """iQiyi (mainland China site) with only the first episode free and discontinuous Bangumi episode IDs."""
        subject_id = 225604  # 刀剑神域 第3期第1部
        subject_url_id = 'a_19rrh1temd'
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % ('www', subject_url_id),
            subject=subject_id,
            episodes=verify_episode_ids_format('826916-826935,833389-833392,864801')[1],
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'service_id_prefix': '',
            'paid': 1,
            'subject_url_id': subject_url_id,
            'locale_suffix': 'CN',
            'subject_name': '刀剑神域',
            'remark_suffix': '爱奇艺',
            'episodes_count': 25,
            'test_episodes': [
                {'index': 0, 'episode_id': 826916, 'episode_number': '1'},
                {'index': 19, 'episode_id': 826935, 'episode_number': '19'},
                {'index': 20, 'episode_id': 833389, 'episode_number': '20'},
                {'index': 23, 'episode_id': 833392, 'episode_number': '23'},
                {'index': 24, 'episode_id': 864801, 'episode_number': '24'},
            ],
        }
        test_iqiyi_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text

    def test_iqiyi_cn_all_paid_wo_exclusion(self, test_iqiyi_generic, caplog):
        """iQiyi (mainland China site) with all episodes paid and continuous Bangumi episode IDs."""
        subject_id = 277551  # 地缚少年花子君
        subject_url_id = 'a_19rrhwqgk5'
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % ('www', subject_url_id),
            subject=subject_id,
            episodes=verify_episode_ids_format('925459-925470')[1],
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'service_id_prefix': '',
            'paid': 2,
            'subject_url_id': subject_url_id,
            'locale_suffix': 'CN',
            'subject_name': '地缚少年花子君',
            'remark_suffix': '爱奇艺',
            'episodes_count': 12,
            'test_episodes': [
                {'index': 0, 'episode_id': 925459, 'episode_number': '1'},
                {'index': 11, 'episode_id': 925470, 'episode_number': '12'},
            ],
        }
        test_iqiyi_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text

    def test_iqiyi_cn_all_paid_w_exclusion(self, test_iqiyi_generic, caplog):
        """iQiyi (mainland China site) with all episodes paid and discontinuous Bangumi episode IDs."""
        subject_id = 240038  # 青春猪头少年不会梦到兔女郎学姐
        subject_url_id = 'a_19rrh6z4oh'
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % ('www', subject_url_id),
            subject=subject_id,
            episodes=verify_episode_ids_format('831366-831377,834292')[1],
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'service_id_prefix': '',
            'paid': 2,
            'subject_url_id': subject_url_id,
            'locale_suffix': 'CN',
            'subject_name': '青春猪头少年不会梦到兔女郎学姐',
            'remark_suffix': '爱奇艺',
            'episodes_count': 13,
            'test_episodes': [
                {'index': 0, 'episode_id': 831366, 'episode_number': '1'},
                {'index': 11, 'episode_id': 831377, 'episode_number': '12'},
                {'index': 12, 'episode_id': 834292, 'episode_number': '13'},
            ],
        }
        test_iqiyi_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text

    def test_iqiyi_tw_wo_exclusion(self, test_iqiyi_generic, caplog):
        """iQiyi (Taiwan site) with continuous Bangumi episode IDs."""
        subject_id = 277551  # 地缚少年花子君
        subject_url_id = 'a_19rrhwqgk5'
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % ('tw', subject_url_id),
            subject=subject_id,
            episodes=verify_episode_ids_format('925459-925470')[1],
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'service_id_prefix': 'tw.',
            'paid': 0,
            'subject_url_id': subject_url_id,
            'locale_suffix': 'HK',
            'subject_name': '地缚少年花子君',
            'remark_suffix': '愛奇藝',
            'episodes_count': 12,
            'test_episodes': [
                {'index': 0, 'episode_id': 925459, 'episode_number': '1'},
                {'index': 11, 'episode_id': 925470, 'episode_number': '12'},
            ],
        }
        test_iqiyi_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text

    def test_iqiyi_tw_w_exclusion(self, test_iqiyi_generic, caplog):
        """iQiyi (Taiwan site) with discontinuous Bangumi episode IDs."""
        subject_id = 219200  # 擅长捉弄的高木同学 第1期
        subject_url_id = 'a_19rrh1ss1p'
        args = argparse.Namespace(
            url=self._SITE_URL_PATTERN % ('tw', subject_url_id),
            subject=subject_id,
            episodes=verify_episode_ids_format('766037,767807-767817')[1],
        )
        source, episodes = self._crawler.crawl(args)
        test_config = {
            'subject_id': subject_id,
            'service_id_prefix': 'tw.',
            'paid': 0,
            'subject_url_id': subject_url_id,
            'locale_suffix': 'HK',
            'subject_name': '擅长捉弄的高木同学',
            'remark_suffix': '愛奇藝',
            'episodes_count': 12,
            'test_episodes': [
                {'index': 0, 'episode_id': 766037, 'episode_number': '1'},
                {'index': 1, 'episode_id': 767807, 'episode_number': '2'},
                {'index': 11, 'episode_id': 767817, 'episode_number': '12'},
            ],
        }
        test_iqiyi_generic(source, episodes, test_config)
        assert "Episodes mismatch" not in caplog.text
