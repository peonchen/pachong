from requests import get
import re
import os
from contextlib import closing

#---------------------------------------
# 稀饭动漫全自动，输入动漫第一集网页链接，即可爬取全集视频
#---------------------------------------
url = 'https://dick.xfani.com/watch/427/1/1.html'
#---------------------------------------

current_part = 1
cookies = {
    '__51vcke__JmrbEK9F16hDQiud': 'f87297f7-ace4-56a2-b32d-5e219c5336e0',
    '__51vuft__JmrbEK9F16hDQiud': '1728572350119',
    'user_id': '273807',
    'user_name': 'peonchen',
    'group_id': '2',
    'group_name': '%E9%BB%98%E8%AE%A4%E4%BC%9A%E5%91%98',
    'user_check': 'de6d97a429c22fdb7db75b3d24beb0c4',
    'user_portrait': '%2Fstatic%2Fimages%2Ftouxiang.png',
    'ecPopup': '1',
    'DS_Records': '%7Blog%3A%5B%7B%22name%22%3A%22%E4%BF%8F%E7%9A%AE%E5%B0%8F%E8%8A%B1%E4%BB%99%20%E8%8F%B2%E5%B0%BC%E5%85%8B%E6%96%AF%E7%9A%84%E9%92%A5%E5%8C%99%22%2C%22url%22%3A%22%2Fsearch%2Fwd%2F%25E4%25BF%258F%25E7%259A%25AE%25E5%25B0%258F%25E8%258A%25B1%25E4%25BB%2599%2520%25E8%258F%25B2%25E5%25B0%25BC%25E5%2585%258B%25E6%2596%25AF%25E7%259A%2584%25E9%2592%25A5%25E5%258C%2599.html%22%7D%5D%7D',
    'mac_history': '%7Blog%3A%5B%7B%22name%22%3A%22%5B%E5%89%A7%E5%9C%BA%E7%89%88%5D%E5%89%A7%E5%9C%BA%E7%89%88%20%E9%97%B4%E8%B0%8D%E8%BF%87%E5%AE%B6%E5%AE%B6%20%E4%BB%A3%E5%8F%B7%EF%BC%9A%E7%99%BD%22%2C%22link%22%3A%22https%3A%2F%2Fdick.xfani.com%2Fwatch%2F2720%2F1%2F1.html%22%2C%22pic%22%3A%22https%3A%2F%2Flain.bgm.tv%2Fpic%2Fcover%2Fl%2Fec%2F82%2F411428_xwKKP.jpg%22%2C%22mid%22%3A%221080P%22%7D%5D%7D',
    '_funcdn_token': '2c726dc1d349d6afe3e16cc5eb0aa2ca866076f34ea6dd7d0e537c75bdc09f64',
    '__51uvsct__JmrbEK9F16hDQiud': '22',
    '__vtins__JmrbEK9F16hDQiud': '%7B%22sid%22%3A%20%229368311b-854b-545a-accc-2363a053f736%22%2C%20%22vd%22%3A%202%2C%20%22stt%22%3A%2054392%2C%20%22dr%22%3A%2054392%2C%20%22expires%22%3A%201730978218144%2C%20%22ct%22%3A%201730976418144%7D',
    'PHPSESSID': '2iq7bcr41rdfja4dvnc934l8dj',
}
headers1 = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cache-control': 'max-age=0',
    # 'cookie': '__51vcke__JmrbEK9F16hDQiud=f87297f7-ace4-56a2-b32d-5e219c5336e0; __51vuft__JmrbEK9F16hDQiud=1728572350119; user_id=273807; user_name=peonchen; group_id=2; group_name=%E9%BB%98%E8%AE%A4%E4%BC%9A%E5%91%98; user_check=de6d97a429c22fdb7db75b3d24beb0c4; user_portrait=%2Fstatic%2Fimages%2Ftouxiang.png; ecPopup=1; DS_Records=%7Blog%3A%5B%7B%22name%22%3A%22%E4%BF%8F%E7%9A%AE%E5%B0%8F%E8%8A%B1%E4%BB%99%20%E8%8F%B2%E5%B0%BC%E5%85%8B%E6%96%AF%E7%9A%84%E9%92%A5%E5%8C%99%22%2C%22url%22%3A%22%2Fsearch%2Fwd%2F%25E4%25BF%258F%25E7%259A%25AE%25E5%25B0%258F%25E8%258A%25B1%25E4%25BB%2599%2520%25E8%258F%25B2%25E5%25B0%25BC%25E5%2585%258B%25E6%2596%25AF%25E7%259A%2584%25E9%2592%25A5%25E5%258C%2599.html%22%7D%5D%7D; mac_history=%7Blog%3A%5B%7B%22name%22%3A%22%5B%E5%89%A7%E5%9C%BA%E7%89%88%5D%E5%89%A7%E5%9C%BA%E7%89%88%20%E9%97%B4%E8%B0%8D%E8%BF%87%E5%AE%B6%E5%AE%B6%20%E4%BB%A3%E5%8F%B7%EF%BC%9A%E7%99%BD%22%2C%22link%22%3A%22https%3A%2F%2Fdick.xfani.com%2Fwatch%2F2720%2F1%2F1.html%22%2C%22pic%22%3A%22https%3A%2F%2Flain.bgm.tv%2Fpic%2Fcover%2Fl%2Fec%2F82%2F411428_xwKKP.jpg%22%2C%22mid%22%3A%221080P%22%7D%5D%7D; _funcdn_token=2c726dc1d349d6afe3e16cc5eb0aa2ca866076f34ea6dd7d0e537c75bdc09f64; __51uvsct__JmrbEK9F16hDQiud=22; __vtins__JmrbEK9F16hDQiud=%7B%22sid%22%3A%20%229368311b-854b-545a-accc-2363a053f736%22%2C%20%22vd%22%3A%202%2C%20%22stt%22%3A%2054392%2C%20%22dr%22%3A%2054392%2C%20%22expires%22%3A%201730978218144%2C%20%22ct%22%3A%201730976418144%7D; PHPSESSID=2iq7bcr41rdfja4dvnc934l8dj',
    'priority': 'u=0, i',
    'referer': 'https://dick.xfani.com/watch/2720/1/1.html',
    'sec-ch-ua': '"Chromium";v="130", "Microsoft Edge";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0',
}
headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Range': 'bytes=0-',
    'Sec-Fetch-Dest': 'video',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}
getname=get(url,verify=False).text
name = re.findall('<a href="javascript:">(.*)</a>',getname)[0].replace(" ","")
file_path = f"E:/dm/{name}"
url_cut = re.findall('(.*?)(\d*).html', url)[0][0]
if not os.path.exists(file_path):
    os.makedirs(file_path)
    print("创建文件夹！")
else:
    print("文件夹已存在！") 

while True:
    per_url = f"{url_cut}{current_part}.html"
    print(per_url)
    # res = get(per_url,verify=False,headers=headers1,cookies=cookies) # verify=False取消ssl验证
    res = get(per_url,verify=False) # verify=False取消ssl验证
    # print(res.text)
    res2 = re.findall('"url":"(.*?)","url_next"',res.text)[0]
    next_res = re.findall('"url_next":"(.*?)","from"',res.text)[0]
    decode_url  = res2.replace('\\/', '/')
    # print(decode_url )
    print(f"\n----------------------下载第{current_part}集中------------------------")
    filename = os.path.join(file_path, f"{name}_{current_part}.mp4")
    if os.path.exists(filename):
         pre_size=os.path.getsize(filename)
    else:
        pre_size=0
    print(f"文件保存在{filename}")
    with closing(get(decode_url, headers=headers,stream=True)) as response:
        chunk_size = 1024
        content_size = int(response.headers['content-length'])
        if not pre_size or pre_size and pre_size != content_size:
            print("视频大小：",content_size/(1024**2),"Mb")
            data_count = 0
            re_download = True
            while re_download:
                with open(filename, "wb") as file:
                    for data in response.iter_content(chunk_size=chunk_size):
                        file.write(data)
                        done_block = int((data_count / content_size) * 50)
                        data_count += len(data)
                        now_jd = (data_count / content_size) * 100
                        print("\r [%s%s] %d%% " % (done_block * '█', ' ' * (50 - 1 - done_block), now_jd), end=" ")
                    file.close()
                    if now_jd == 100:
                        re_download = False
        else:
            print("该文件已下载！")
    if not next_res:
        break
    else:
        current_part+=1


