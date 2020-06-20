![GitHub Top Language](https://img.shields.io/github/languages/top/maobowen/enhanced-bangumi-api-data-crawler)
[![Build Status](https://travis-ci.com/maobowen/enhanced-bangumi-api-data-crawler.svg?branch=master)](https://travis-ci.com/maobowen/enhanced-bangumi-api-data-crawler)
[![Coverage Status](https://coveralls.io/repos/github/maobowen/enhanced-bangumi-api-data-crawler/badge.svg?branch=master)](https://coveralls.io/github/maobowen/enhanced-bangumi-api-data-crawler?branch=master)
![GitHub License](https://img.shields.io/github/license/maobowen/enhanced-bangumi-api-data-crawler)

# Data Crawler for Enhanced Bangumi API

This is a crawler which crawls anime data from various streaming websites and generate output in certain CSV format. The output can then be copied and pasted to [the data files](https://github.com/maobowen/enhanced-bangumi-api-data) used by [the Enhanced Bangumi API project](https://github.com/maobowen/enhanced-bangumi-api). This crawler currently supports the following streaming websites:

- [AcFun](https://www.acfun.cn)
- [哔哩哔哩](https://www.bilibili.com)
- [Crunchyroll](https://www.crunchyroll.com)
- [Funimation](https://www.funimation.com)
- [巴哈姆特動畫瘋](https://ani.gamer.com.tw)
- [爱奇艺](https://www.iqiyi.com)
- [乐视视频](https://www.le.com)
- [ニコニコ動画](https://www.nicovideo.jp)
- [PP视频](https://www.pptv.com)
- [腾讯视频](https://v.qq.com)
- [Viu](http://www.viu.com)
- [优酷](https://www.youku.com)

## Installation

Running this crawler requires Python 3. Simply run `pip install -r requirements.txt` to install all the dependencies, or `conda install --yes --file requirements.txt` if you are using a Conda environment.

## Usage

This crawler requires the following arguments. Taking Non Non Biyori Season 1 as an example, you need:

- Subject URL (required; flags `-u` or `--url`)
  - The URL of the anime series, for example, `https://www.crunchyroll.com/non-non-biyori`.
- Bangumi subject ID (required; flags `-s` or `--subject`)
  - The subject ID on [Bangumi](https://bgm.tv). For example, if the Bangumi URL is https://bgm.tv/subject/78405, then `78405` is the subject ID.
- Bangumi episode IDs (required; flags `-e` or `--episodes`)
  - A list of episode IDs on Bangumi. The sequence of IDs must match the sequence of episodes listing on the streaming website, and the IDs must be provided in the format of page ranges (see the definition [here](https://www.geeksforgeeks.org/python-convert-string-ranges-to-list/)). For example, `319289-319299,320742` means that [episode 1 on Crunchyroll](https://www.crunchyroll.com/media-645563) has [episode ID 319289 on Bangumi](https://bgm.tv/ep/319289), [episode 11](https://www.crunchyroll.com/media-645583) has [episode ID 319299](https://bgm.tv/ep/319299), and [episode 12](https://www.crunchyroll.com/media-645585) has [episode ID 320742](https://bgm.tv/ep/320742). You may also skip some episodes which are listed on the streaming website but not on Bangumi by having two consecutive commas like `705488-705491,,705492-705494`.
- Crunchyroll collection ID (optional; flag `--cr-collection`)
  - Collection ID on Crunchyroll. This argument is only required when a Crunchyroll series has multiple collections (multiple seasons or dubbed version). For example, season 1 of Non Non Biyori has collection ID 21335, so you must provide `--cr-collection 21335` in order to crawl data for that particular season. If you do not specify this argument but multiple collections exists in the series, the crawler will print all available collections and stop. You can apply this trick to find out what collection ID to use.
- Funimation season ID (optional; flag `--funi-season`)
  - Season ID on Funimation. This argument is only required when a Funimation series has multiple seasons, similar to the Crunchyroll collection ID. Also similarly, if you do not specify this argument but multiple seasons exists, the crawler will print all available seasons and stop.

With all the arguments prepared, the crawler can be run in two modes **outside** of the root directory:

- Interactive mode: Execute without arguments, that is, `python crawler`. It will let you input the arguments one by one.
- Quiet mode: Execute with arguments, for example, `python crawler -u "https://www.crunchyroll.com/non-non-biyori" -s 78405 -e "319289-319299,320742" --cr-collection 21335`.

The first line of the output is the [source record](https://github.com/maobowen/enhanced-bangumi-api-data/tree/master/sources), and the following are [episode records](https://github.com/maobowen/enhanced-bangumi-api-data/tree/master/episodes).

### Crunchyroll

Due to geo restrictions, crawling animes from Crunchyroll only works with a US IP address.

If you need to crawl anime series with explicit content on Crunchyroll, you must have an adult Crunchyroll account to bypass the maturity wall. Set the following environment variables before running the crawler:

```sh
export CR_ACCOUNT=<account>
export CR_PASSWORD=<password>
```

### Funimation

Due to the limitation that there is no good solution to bypass Incapsula bot detection, crawling animes from Funimation needs some extra manual work. On the anime series page, you need to use your browser's inspector and search for `TITLE_DATA` to get the series ID. Then you need to construct the URL which contains that ID, for example, <https://www.funimation.com/shows/594522/>. URLs like <https://www.funimation.com/shows/sword-art-online/> are not accepted at the moment.

## References

All references can be found in the source code. Special thanks to the following open-source projects:

- [Bangumi Data Helper](https://github.com/bangumi-data/helper): APIs for most Chinese streaming websites
- [CrunchyrollDownloaderPy](https://github.com/ThePBone/CrunchyrollDownloaderPy), [Crunchyroll API Wiki](https://github.com/CloudMax94/crunchyroll-api/wiki) and [CR-Unblocker Server](https://github.com/onestay/CR-Unblocker-Server): Crunchyroll APIs
- [Tencent Video Spider](https://github.com/ljm9104/tencent_video_spider): Tencent Video APIs
- [ViuTV API](https://github.com/ljm9104/tencent_video_spider): Viu APIs
- [WeVideo](https://github.com/afirez/WeVideo): LeTV APIs
- [youtube-dl](http://github.com/ytdl-org/youtube-dl): Some APIs and extracting data from websites

---

© [101对双生儿](https://bmao.tech/) 2020.
