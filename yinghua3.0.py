import requests, execjs, re
from contextlib import closing
from requests import get
import os


#---------------------------------------
# web路径
web_url = input("请输入web路径:")
# 集数
number = int(input("请输入集数:"))
# 开始
start = int(input("请输入开始集数:"))
# 文件夹名字
name = input("请输入文件夹名字:")
#---------------------------------------

# 文件路径
file_path = f"E:/dm/{name}"
# 路径截取
url_cut = second = re.findall('(.*?)(\d*).html', web_url)[0][0]
if not os.path.exists(file_path):
    os.makedirs(file_path)
    print("Folder created")
else:
    print("Folder already exists")

# 请求头
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Referer': 'https://www.295yhw.com/',
    'Sec-Fetch-Dest': 'iframe',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'cross-site',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

for ji in range(start, number + 1):
    print(f"\n----------------------下载{ji}/{number}个视频------------------------")
    url = f"{url_cut}{ji}.html"
    print(url)
    res = requests.get(url).text
    second = re.findall('"url":"(.*?)","url_next"', res)[0]
    res2 = requests.get('https://danmu.yhdmjx.com/m3u8.php?url=' + second, headers=headers).text
    bt_token = re.findall('var bt_token = "(.*?)";', res2)[0]
    encode_url = re.findall('getVideoInfo\("(.*?)"', res2)[0]
    decode = execjs.compile(open('./eeee/pachong/jm.js', 'r', encoding='utf-8').read(), cwd=r"./eeee./node_modules/crypto-js")
    canshu = f'getVideoInfo("{encode_url}","{bt_token}")'
    decode_url = decode.eval(canshu) 
    print("----------------------获取视频链接成功------------------------")
    print(f"视频链接为{decode_url}")
    print("----------------------正在下载视频------------------------")
    
    filename = os.path.join(file_path, f"{name}_{ji}.mp4")
    if os.path.exists(filename):
        print("该文件已存在")
        continue
    
    print(f"文件保存在{filename}")
    with closing(get(decode_url, stream=True)) as response:
        chunk_size = 1024
        content_size = int(response.headers['content-length'])
        data_count = 0
        with open(filename, "wb") as file:
            for data in response.iter_content(chunk_size=chunk_size):
                file.write(data)
                done_block = int((data_count / content_size) * 50)
                data_count += len(data)
                now_jd = (data_count / content_size) * 100
                print("\r [%s%s] %d%% " % (done_block * '█', ' ' * (50 - 1 - done_block), now_jd), end=" ")
            file.close()
