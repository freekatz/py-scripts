from Crypto.Cipher import AES
import base64
import json
import requests
import re

from music.src._163 import config

# 加密
pad = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
encrypto_token = lambda key, content: AES.new(key=key, mode=AES.MODE_CBC, IV=config.iv).encrypt(pad(content).encode())


# 接口
def music_interface(base_url):
    try:
        song_id = re.search(r'/(\d+?)/', base_url).groups()[0]
    except:
        song_id = re.search(r'id=(.*?)&', base_url).groups()[0]
    print(song_id)
    config.content["ids"] = "[{}]".format(song_id)
    str_content = json.dumps(config.content)
    tmp = base64.b64encode(encrypto_token(config.key1, str_content)).decode()
    params = base64.b64encode(encrypto_token(config.key2, tmp)).decode()
    # print(params)
    post_data = {
        'params': params,
        'encSecKey': config.encSecKey,
    }
    resp = requests.post(url=config.post_url, headers=config.headers, data=post_data)
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