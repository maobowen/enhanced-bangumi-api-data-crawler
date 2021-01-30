HTTP_HEADERS = {
    'Accept-Language': '*',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:76.0) Gecko/20100101 Firefox/76.0',
}
SITE_SERVICE_ID = {
    'acfun':       'acfun.cn',
    'animad':      'ani.gamer.com.tw',
    'bilibili':    'bilibili.com',
    'crunchyroll': 'crunchyroll.com',
    'funimation':  'funimation.com',
    'iqiyi':       'iqiyi.com',
    'letv':        'le.com',
    'netflix':     'netflix.com',
    'niconico':    'nicovideo.jp',
    'pptv':        'pptv.com',
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
    'funimation':  r'https?:\/\/(?:www\.)?funimation\.com\/shows\/(\d+)',
    'iqiyi':       r'https?:\/\/(?:(?:www\.)?|tw\.)iqiyi\.com\/(a_\w+)\.html',
    'letv':        r'https?:\/\/(?:www\.)?le\.com\/comic\/(\d+).html',
    'netflix':     r'https?:\/\/(?:www\.)?netflix\.com\/title\/(\d+)',
    'niconico':    r'https?:\/\/ch\.nicovideo\.jp\/ch(\d+)',
    'pptv':        r'https?:\/\/v\.pptv\.com\/page\/(\w+).html',
    'qq':          r'https?:\/\/v\.qq\.com\/detail\/(?:[0-9a-z])\/(\w{15})\.html',
    'viu':         r'https?:\/\/www\.viu\.com\/ott\/([a-z]{2})\/[a-z]{2}-[a-z]{2}\/vod\/(\d+)\/',
    'youku':       r'https?:\/\/list\.youku\.com\/show\/id_(z\w{20})\.html',
}
