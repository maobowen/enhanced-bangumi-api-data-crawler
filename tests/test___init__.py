import argparse
import re

from src import crawl, verify_episode_ids_format


class TestInit:
    """Test suite for functions inside src/__init__.py."""

    def test_valid_epsisode_ids_format_wo_exclusion(self):
        """Continuous Bangumi episode IDs."""
        valid, ids_list = verify_episode_ids_format('538096-538107')  # 101442 悠哉日常大王 第2期
        assert valid
        assert ids_list == list(range(538096, 538108))

    def test_valid_episodes_ids_format_w_single_exclusion_at_the_beginning(self):
        """One discontinuous Bangumi episode IDs at the beginning."""
        valid, ids_list = verify_episode_ids_format('906496,905519-905530')  # 279457 刀剑神域 第3期第2部
        assert valid
        assert ids_list == [906496] + list(range(905519, 905531))

    def test_valid_episodes_ids_format_w_single_exclusion_at_the_end(self):
        """One discontinuous Bangumi episode IDs at the end."""
        valid, ids_list = verify_episode_ids_format('319289-319299,320742')  # 78405 悠哉日常大王 第1期
        assert valid
        assert ids_list == list(range(319289, 319300)) + [320742]

    def test_valid_episodes_ids_format_w_single_exclusion_in_the_middle(self):
        """One discontinuous Bangumi episode IDs in the middle."""
        valid, ids_list = verify_episode_ids_format('705416-705421,719948,705422-705427')  # 207573 月色真美
        assert valid
        assert ids_list == list(range(705416, 705422)) + [719948] + list(range(705422, 705428))

    def test_valid_episodes_ids_format_w_multiple_exclusion(self):
        """Multiple Bangumi episode IDs intervals."""
        valid, ids_list = verify_episode_ids_format('873545-873553,874066-874068,880603-880615')  # 266455 水果篮子 第1期
        assert valid
        assert ids_list == list(range(873545, 873554)) + list(range(874066, 874069)) + list(range(880603, 880616))

    def test_crawl_acfun(self, capsys):
        """Crawl series on AcFun."""
        args = argparse.Namespace(
            url='https://www.acfun.cn/bangumi/aa5025182',  # NEW GAME! 第1期
            subject=150775,
            episodes=verify_episode_ids_format('642458-642469')[1],
        )
        crawl(args)
        captured = capsys.readouterr()
        assert '150775,acfun.cn,0,5025182,zh_CN,<名称>-A站' in captured.out
        assert re.search(r'150775,642458,acfun\.cn,(?:\d+)_(?:\d+),,EP1-A站', captured.out)

    def test_crawl_animad(self, capsys):
        """Crawl series on Animad."""
        args = argparse.Namespace(
            url='https://acg.gamer.com.tw/acgDetail.php?s=74763',  # Charlotte
            subject=120925,
            episodes=verify_episode_ids_format('541642-541653,545598,564743')[1],
        )
        crawl(args)
        captured = capsys.readouterr()
        assert '120925,ani.gamer.com.tw,0,74763,zh_HK,夏洛特-动画疯' in captured.out
        assert re.search(r'120925,541642,ani\.gamer\.com\.tw,(?:\d+),,EP1-动画疯', captured.out)

    def test_crawl_bilibili(self, capsys):
        """Crawl series on Bilibili."""
        args = argparse.Namespace(
            url='https://www.bilibili.com/bangumi/media/md2572/',  # Charlotte
            subject=120925,
            episodes=verify_episode_ids_format('541642-541653,545598')[1],
        )
        crawl(args)
        captured = capsys.readouterr()
        assert '120925,bilibili.com_cn,0,2572,zh_CN,Charlotte-B站大陆' in captured.out
        assert re.search(r'120925,541642,bilibili\.com_cn,(?:BV[0-9A-Za-z]{10}),,EP1-B站大陆', captured.out)

    def test_crawl_crunchyroll(self, capsys):
        """Crawl series on Crunchyroll."""
        args = argparse.Namespace(
            url='https://www.crunchyroll.com/charlotte',  # Charlotte
            subject=120925,
            episodes=verify_episode_ids_format('541642-541653,545598')[1],
        )
        crawl(args)
        captured = capsys.readouterr()
        assert '120925,crunchyroll.com,0,charlotte,en_US:es_MX:pt_BR,Charlotte-Crunchyroll' in captured.out
        assert re.search(r'120925,541642,crunchyroll\.com,(?:\d+),,EP1-Crunchyroll', captured.out)

    def test_crawl_iqiyi(self, capsys):
        """Crawl series on iQIYI."""
        args = argparse.Namespace(
            url='https://www.iqiyi.com/a_19rrhb5qhd.html',  # Charlotte
            subject=120925,
            episodes=verify_episode_ids_format('541642-541653,545598')[1],
        )
        crawl(args)
        captured = capsys.readouterr()
        assert '120925,iqiyi.com,0,a_19rrhb5qhd,zh_CN,Charlotte-爱奇艺' in captured.out
        assert re.search(r'120925,541642,iqiyi\.com,(?:v_[0-9a-z]{10}),,EP1-爱奇艺', captured.out)

    def test_crawl_niconico(self, capsys):
        """Crawl series on Niconico."""
        args = argparse.Namespace(
            url='http://ch.nicovideo.jp/channel/ch2610619',  # Charlotte
            subject=120925,
            episodes=verify_episode_ids_format('541642-541653,545598')[1],
        )
        crawl(args)
        captured = capsys.readouterr()
        assert '120925,nicovideo.jp,1,2610619,ja_JP,TVアニメ「Charlotte(シャーロット)」-niconico' in captured.out
        assert re.search(r'120925,541642,nicovideo\.jp,(?:\d+),,EP一-niconico', captured.out)

    def test_crawl_qq(self, capsys):
        """Crawl series on Tencent Video."""
        args = argparse.Namespace(
            url='https://v.qq.com/detail/k/keh8jx4nea7e5w0.html',  # Charlotte
            subject=120925,
            episodes=verify_episode_ids_format('541642-541653,545598')[1],
        )
        crawl(args)
        captured = capsys.readouterr()
        assert '120925,v.qq.com,-1,keh8jx4nea7e5w0,zh_CN,Charlotte-腾讯视频' in captured.out
        assert re.search(r'120925,541642,v\.qq\.com,(?:[a-z0-9]+),,EP1-腾讯视频', captured.out)

    def test_crawl_viu(self, capsys):
        """Crawl series on Viu."""
        args = argparse.Namespace(
            url='https://www.viu.com/ott/hk/zh-hk/vod/123101/',  # 辉夜大小姐想让我告白 第1期
            subject=248175,
            episodes=verify_episode_ids_format('850264-850275')[1],
        )
        crawl(args)
        captured = capsys.readouterr()
        assert '248175,viu.com_hk,0,123101,zh_HK,輝夜姬想讓人告白~天才們的戀愛頭腦戰~-ViuHK' in captured.out
        assert re.search(r'248175,850264,viu\.com_hk,(?:\d+),,EP1-ViuHK', captured.out)

    def test_crawl_youku(self, capsys):
        """Crawl series on Youku."""
        args = argparse.Namespace(
            url='https://list.youku.com/show/id_z074ab022197c11e5b5ce.html',  # Charlotte
            subject=120925,
            episodes=verify_episode_ids_format('541642-541653,545598')[1],
        )
        crawl(args)
        captured = capsys.readouterr()
        assert '120925,youku.com,0,z074ab022197c11e5b5ce,zh_CN,<名称>-优酷' in captured.out
        assert re.search(r'120925,541642,youku\.com,(?:[A-Za-z0-9+/]+={,2}),,EP1-优酷', captured.out)
