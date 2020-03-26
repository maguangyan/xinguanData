import pandas as pd
import requests
import json
import datetime as dt

# 获取当前时间
now_time = dt.datetime.now().strftime('%F')   # %F为只显示年月日

url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
area = requests.get(url).json()
data = json.loads(area['data'])
update_time = data['lastUpdateTime']
all_counties = data['areaTree']
all_list = []
for country_data in all_counties:
    if country_data['name'] != '中国':
        continue
    else:
        all_provinces = country_data['children']
        for province_data in all_provinces:
            province_name = province_data['name']
            province_today = province_data['today']
            province_total = province_data['total']
            province_result = {'省份': province_name, '更新日期': update_time, '现有确诊': province_total['nowConfirm'],
                               '累计确诊': province_total['confirm'],'累计治愈': province_total['heal'],'累计死亡': province_total['dead'],
                               '今日新增确诊': province_today['confirm'],'今日治愈': province_today['confirmCuts']}
            all_list.append(province_result)#将当前省份的数据添加到数据列表里面

df = pd.DataFrame(all_list)
df.to_csv('China/' + now_time + '.csv', index=False, encoding="utf_8_sig")

