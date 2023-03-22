import requests
import pandas as pd
import time
import os


def get_time(fmt:str='%Y-%m-%d %H-%M-%S') -> str:
    '''
    获取当前时间
    '''
    ts = time.time()
    ta = time.localtime(ts)
    t = time.strftime(fmt, ta)
    return t


def save_hot_list():
    # 请求头
    headers = {

        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5 (Ergänzendes Update)) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15',
        'Host': 'api.zhihu.com',


    }
    # 请求参数
    params = (
        ('limit', '50'),
        ('reverse_order', '0'),
    )
    # 发送请求
    response = requests.get(
        'https://zhihu.com/topstory/hot-list', headers=headers, params=params)

    items = response.json()['data']
    rows = []
    now = get_time()
    # 取日期为文件夹名称
    dir_path = now.split(' ')[0]
    # 文件夹不存在则创建
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    # 遍历全部热榜，取出几个属性
    for rank, item in enumerate(items, start=1):
        target = item.get('target')
        title = target.get('title')
        answer_count = target.get('answer_count')
        hot = int(item.get('detail_text').split(' ')[0])
        follower_count = target.get('follower_count')
        question_url = target.get('url').replace(
            'api', 'www').replace('questions', 'question')
        rows.append({
            '排名': rank,
            '标题': title,
            '回答数': answer_count,
            '关注数': follower_count,
            '热度(万)': hot,
            '问题链接': question_url
        })
    return rows
    # df = pd.DataFrame(rows)
    # now = get_time()
    # csv_path = dir_path+'/'+now+'.csv'
    # df.to_csv(csv_path, encoding='utf-8-sig', index=None)
    # print(now, '的热榜数据数据已保存到文件', csv_path)

# 保存热榜数据
# save_hot_list()

