from Crypto.Cipher import AES
import base64
import json
import requests
import re
# 常量
headers = {
    # 'Host': 'm8c.music.126.net',
    'User-Agent':
    'NeteaseMusic/5.8.3.1548335430(135);Dalvik/2.1.0 (Linux; U; Android 9; ONEPLUS A5010 Build/PKQ1.180716.001)',
    # 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:65.0) Gecko/20100101 Firefox/65.0',
    'Referer':
    'http://music.163.com/',
    'Content-Type':
    'application/x-www-form-urlencoded',
}
post_url = 'https://music.163.com/weapi/song/enhance/player/url'
content = {"ids": "", "br": 999000, "csrf_token": ""}
key1 = b'0CoJUm6Qyw8W8jud'
key2 = b'ryPnuAVT5RtiIWNi'
encSecKey = 'a71973af53caae445b554150da52e75ba5687609d28013aacea03e9ef07169560f156ca76be9ac8df7bb204e05b864756aa3dd2274a65d5be964f118f6d075006695059e10cdcc806306e9a5f2f36f5bf0379f511cd13a600a6cc7031c814583863ea84d3373dea69f74354cd2dc3af61d58eeb43b1de06f588ef361ebc1eed6'

# 加密
pad = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
encrypt_token = lambda key, content: AES.new(key=key, mode=AES.MODE_CBC, IV=b'0102030405060708').encrypt(pad(content).encode())


# 接口
def music_interface(base_url):
    try:
        song_id = re.search(r'/(\d+?)/', base_url).groups()[0]
    except:
        song_id = re.search(r'id=(.*?)&', base_url).groups()[0]
    print(song_id)
    content["ids"] = "[{}]".format(song_id)
    str_content = json.dumps(content)
    tmp = base64.b64encode(encrypt_token(key1, str_content)).decode()
    params = base64.b64encode(encrypt_token(key2, tmp)).decode()
    # print(params)
    post_data = {
        'params': params,
        'encSecKey': encSecKey,
    }
    resp = requests.post(url=post_url, headers=headers, data=post_data)
    print(resp.text)
    js = json.loads(resp.content)
    song_url = js['data'][0]['url']
    return song_url


def download(url):
    music = requests.get(url)
    with open("test.mp3", 'wb') as f:
        for chunk in music.iter_content(chunk_size=20):
            f.write(chunk)


if __name__ == '__main__':
    # 输入你要下载歌曲的ID，假如想下载一整个音乐列表，那么请自行修改代码，理论上歌曲无论免费还是VIP专享，只要能听的都可以下载
    base_url = "分享Charlie Puth的单曲《How Long》:?http://music.163.com/song/509728806/?userid=410379629?(来自@网易云音乐)"

    song_url = music_interface(base_url)
    print(song_url)
    download(song_url)
    print("下载完成！！")