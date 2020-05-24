HTTP_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:76.0) Gecko/20100101 Firefox/76.0',
}
SITE_SERVICE_ID = {
    'acfun':       'acfun.cn',
    'animad':      'ani.gamer.com.tw',
    'bilibili':    'bilibili.com',
    'crunchyroll': 'crunchyroll.com',
    'iqiyi':       'iqiyi.com',
    'niconico':    'nicovideo.jp',
    'qq':          'v.qq.com',
    'viu':         'viu.com',
    'youku':       'youku.com',
}
# https://github.com/bangumi-data/helper/blob/master/lib/commands/update.js#L7-L21
SITE_URL_PATTERN = {
    'acfun':       r'https?:\/\/(?:www\.)?acfun\.cn\/bangumi\/aa(\d+)',
    'animad':      r'https?:\/\/acg\.gamer\.com\.tw\/acgDetail\.php\?s=(\d+)',
    'bilibili':    r'https?:\/\/(?:www\.)?bilibili\.com\/bangumi\/media\/md(\d+)',
    'crunchyroll': r'https?:\/\/(?:www\.)?crunchyroll\.com\/([\w|\-]+)(?:\?skip_wall=1)?',
    'iqiyi':       r'https?:\/\/(?:(?:www\.)?|tw\.)iqiyi\.com\/(a_\w+)\.html',
    'niconico':    r'https?:\/\/ch\.nicovideo\.jp\/channel\/ch(\d+)',
    'qq':          r'https?:\/\/v\.qq\.com\/detail\/(?:[0-9a-z])\/(\w{15})\.html',
    'viu':         r'https?:\/\/www\.viu\.com\/ott\/([a-z]{2})\/[a-z]{2}-[a-z]{2}\/vod\/(\d+)\/',
    'youku':       r'https?:\/\/list\.youku\.com\/show\/id_(z\w{20})\.html',
}
