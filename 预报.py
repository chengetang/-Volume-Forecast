# %%
stations = [
    {"id": 758, "name": "PSW", "pickup_time": "20:30", "platform": "Platform 83"},
    {"id": 761, "name": "C4T", "pickup_time": "19:30", "platform": "Platform 85"},
    {"id": 768, "name": "WER", "pickup_time": "20:30", "platform": "Platform 83"},
    {"id": 878, "name": "ANA", "pickup_time": "21:00", "platform": "Platform A05"},
    {"id": 879, "name": "MEK", "pickup_time": "19:00", "platform": "Platform 34"},
    #{"id": 899, "name": "JHD", "pickup_time": "20:00", "platform": "Platform 88"},
    {"id": 948, "name": "INB", "pickup_time": "19:00", "platform": "Platform 84"},
    {"id": 1002, "name": "RIN", "pickup_time": "20:00", "platform": "Platform 85"},
    {"id": 1092, "name": "ACT", "pickup_time": "21:00", "platform": "Platform 86"},
    {"id": 1124, "name": "RSR", "pickup_time": "19:45", "platform": "Platform 33"},
    {"id": 1158, "name": "SAM", "pickup_time": "21:00", "platform": "Platform ***"},
    {"id": 1193, "name": "OMT", "pickup_time": "19:00", "platform": "Platform 85"},
    {"id": 1229, "name": "RSL", "pickup_time": "19:45", "platform": "Platform 87"},
    {"id": 1266, "name": "DET", "pickup_time": "19:00", "platform": "Platform 87"},
    {"id": 1326, "name": "AAT", "pickup_time": "21:00", "platform": "Platform ***"},
    {"id": 1327, "name": "SAS", "pickup_time": "21:00", "platform": "Platform ***"},
    {"id": 1329, "name": "GAL", "pickup_time": "19:00", "platform": "Platform 32"},
    {"id": 1330, "name": "CEK", "pickup_time": "19:45", "platform": "Platform 30"},
    {"id": 1332, "name": "RKM", "pickup_time": "19:00", "platform": "Platform 82"},
    {"id": 1334, "name": "AAA", "pickup_time": "21:00", "platform": "Platform A02"},
    {"id": 1339, "name": "TSI", "pickup_time": "20:30", "platform": "Platform 27"},
    {"id": 1340, "name": "BTY", "pickup_time": "21:00", "platform": "Platform 9"},
    {"id": 1341, "name": "SFT", "pickup_time": "21:00", "platform": "Platform A04"},
    {"id": 1342, "name": "FPS", "pickup_time": "19:45", "platform": "Platform 33"},
    {"id": 1345, "name": "BEN", "pickup_time": "21:00", "platform": "Platform 29"},
    {"id": 1346, "name": "BMB", "pickup_time": "19:45", "platform": "Platform 28"},
    {"id": 1350, "name": "YKY", "pickup_time": "19:45", "platform": "Platform 29"},
    {"id": 1351, "name": "G6T", "pickup_time": "20:30", "platform": "Platform 30"},
    {"id": 1354, "name": "B88", "pickup_time": "21:00", "platform": "Platform 5"},
    {"id": 1355, "name": "XXX", "pickup_time": "21:00", "platform": "Platform 89"},
    #{"id": 1356, "name": "E1L", "pickup_time": "10:00", "platform": "Platform 34"},
    {"id": 1357, "name": "T7Q", "pickup_time": "20:00", "platform": "Platform 31"},
    {"id": 1358, "name": "VT2", "pickup_time": "21:00", "platform": "Platform 27"},
    {"id": 1359, "name": "AFM", "pickup_time": "19:00", "platform": "Platform 83"},
    {"id": 1366, "name": "TR6", "pickup_time": "20:00", "platform": "Platform 32"},
    {"id": 1364, "name": "BAL", "pickup_time": "21:00", "platform": "Platform 10"},
    {"id": 1371, "name": "KT1", "pickup_time": "21:00", "platform": "Platform 84"},
    {"id": 1368, "name": "DIA", "pickup_time": "21:00", "platform": "Platform 7"},
    {"id": 1370, "name": "BFF", "pickup_time": "21:00", "platform": "Platform 8"},
    {"id": 1384, "name": "TEE", "pickup_time": "21:00", "platform": "Platform ***"},
    {"id": 1372, "name": "SWC", "pickup_time": "21:00", "platform": "Platform ***"},
    {"id": 1383, "name": "LEY", "pickup_time": "21:00", "platform": "Platform ***"},
    {"id": 1385, "name": "VXO", "pickup_time": "21:00", "platform": "Platform ***"},
    {"id": 1380, "name": "LOG", "pickup_time": "21:00", "platform": "Platform ***"},
    {"id": 1347, "name": "HA6", "pickup_time": "21:00", "platform": "Platform ***"},
    {"id": 1382, "name": "TNZ", "pickup_time": "21:00", "platform": "Platform ***"},
    {"id": 1381, "name": "POK", "pickup_time": "21:00", "platform": "Platform ***"},
    {"id": 1375, "name": "C5S", "pickup_time": "21:00", "platform": "Platform ***"},
    {"id": 1376, "name": "BMW", "pickup_time": "20:00", "platform": "Platform 28"},
    {"id": 1377, "name": "TOP", "pickup_time": "20:00", "platform": "Platform 30"},
    {"id": 1378, "name": "MOF", "pickup_time": "20:30", "platform": "Platform 76"},
    {"id": 1386, "name": "LAK", "pickup_time": "21:00", "platform": "Platform 87"},
    #{"id": 1387, "name": "NGT", "pickup_time": "20:00", "platform": "Platform 88"},
    {"id": 1388, "name": "MAN", "pickup_time": "21:00", "platform": "Platform ***"},
    {"id": 1389, "name": "PMS", "pickup_time": "21:00", "platform": "Platform ***"}
]


# %%
import time
import math
import pandas as pd
import requests # 导入新的库
import json     # 导入 JSON 库
from selenium import webdriver
from selenium.webdriver.common.by import By

print("库导入成功")

# 关闭 requests 库关于 InsecureRequestWarning 的警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

driver = webdriver.Chrome()
print("浏览器启动成功")
# 替换为你要登录的网址
login_url = 'https://cps.cirroparcel.nl/login' # 假设这是登录页
driver.get(login_url)

# 等待页面加载
time.sleep(3) 

# --- 使用 XPath 定位元素并填写 ---
try:
    username_field = driver.find_element(By.XPATH, '//input[@placeholder="手机号"]')
    username_field.send_keys('491629517653') # 替换为你的手机号

    password_field = driver.find_element(By.XPATH, '//input[@placeholder="密码"]')
    password_field.send_keys('801074') # 替换为你的密码
except Exception as e:
    print(f"自动填写用户名/密码失败: {e}")
    print("请手动填写所有登录信息。")


# --- 暂停脚本，等待用户手动操作 ---
print("="*50)
print("脚本已暂停，请在浏览器中完成登录操作。")
print("="*50)
input("确认登录成功后，请按 Enter 键继续...")

print("登录完成，准备提取 Cookies 并请求 API...")

# %%
import datetime

# --- 1. 获取基础日期 ---
today_date = datetime.date.today()
six_days_ago_date = today_date - datetime.timedelta(days=6)
yesterday_date = today_date - datetime.timedelta(days=1) # <--- 新增：计算昨天的日期

# --- 2. 重新计算并存储到四个变量中 ---

# 用于查询当天范围的变量 (这部分不变)
today_begin_time = today_date.strftime('%Y-%m-%d') + " 00:00:00"
today_end_time = today_date.strftime('%Y-%m-%d') + " 23:59:59"

# 用于查询过去6天范围的变量 (从6天前到昨天)
past_period_begin_time = six_days_ago_date.strftime('%Y-%m-%d') + " 00:00:00"
# !! 核心改动: 使用 yesterday_date 来生成结束时间 !!
past_period_end_time = yesterday_date.strftime('%Y-%m-%d') + " 23:59:59"


# --- 3. 打印所有四个变量以供检查 ---
print("="*20 + " 当天时间范围 " + "="*20)
print(f"变量 'today_begin_time':     {today_begin_time}")
print(f"变量 'today_end_time':       {today_end_time}")
print("\n" + "="*20 + " 过去六天到昨天的时间范围 " + "="*20)
print(f"变量 'past_period_begin_time': {past_period_begin_time}")
print(f"变量 'past_period_end_time':   {past_period_end_time}")

# %%
# --- 1. 从 Selenium 中提取 Cookies ---
#selenium_cookies = driver.get_cookies()

# --- 2. 创建一个 requests Session ---
# Session 对象可以跨请求保持 Cookies，非常方便
s = requests.Session()

# --- 3. 将 Cookies 添加到 requests Session 中 ---
#or cookie in selenium_cookies:
#    s.cookies.set(cookie['name'], cookie['value'])


# %%
# 第 4 步 (最终自动化版): 自动获取 Token 并请求 API

# --- 1. 等待并自动从 localStorage 获取 Token ---
print("正在尝试从浏览器 localStorage 自动获取 Authorization Token...")
auth_token = None
try:
    # 等待几秒钟，确保登录后脚本有时间将 Token 写入 localStorage
    time.sleep(3) 
    
    # !! 使用你找到的 Key: 'Admin-Token' !!
    token_key_in_storage = 'Admin-Token'
    
    # 执行 JavaScript 从 localStorage 中获取 item
    token_value = driver.execute_script(f"return localStorage.getItem('{token_key_in_storage}');")

    if token_value:
        # 统一加上 "Bearer " 前缀，以防万一
        if token_value.startswith('Bearer '):
            auth_token = token_value
        else:
            auth_token = f'Bearer {token_value}'
        print("成功自动获取到 Token！",auth_token)
    else:
        # 这个错误处理很重要，如果 Key 存在但值为空
        print(f"错误：在 localStorage 中找到了 Key '{token_key_in_storage}'，但其值为空。可能是登录后写入有延迟。")

except Exception as e:
    print(f"自动获取 Token 失败: {e}")
    print("请确认 Key 的名字是否拼写正确。")



# %% [markdown]
# #读取当天的装载中，待出库，已出仓，已组托

# %%
# --- 准备工作：定义你的站点字典 ---
# 我们使用 {ID: 名称} 的格式，这样可以在结果中同时保留 ID 和名称
id_to_name_mapping = {
    
    'PSW': 758, 'WER': 768, 'C4T': 761, 'BAL': 1364,
    'LOG': 1380, 'TEE': 1384, 
    'VXO': 1385, 'ANA': 878, 'MEK': 879, 
     'INB': 948,
    'RIN': 1002,  'ACT': 1092, 'RSR': 1124,
    'SAM': 1158, 'OMT': 1193, 'RSL': 1229, 'DET': 1266, 
    'AAT': 1326, 'SAS': 1327, 'GAL': 1329,
    'CEK': 1330, 'RKM': 1332, 'AAA': 1334, 
    'TSI': 1339, 'BTY': 1340,
    'SFT': 1341, 'FPS': 1342, 'BEN': 1345,
    'BMB': 1346, 'HA6': 1347, 'YKY': 1350,
    'G6T': 1351, 'B88': 1354, 'XXX': 1355, 'VT2': 1358, 
    'AFM': 1359, 'T7Q': 1357, 'KAZ': 1362,
    'BMW': 1376, 'TR6': 1366, 
    'LAK': 1386, 'TOP': 1377, 'DIA': 1368, 'MOF': 1378, 'C5S': 1375,
    'BFF': 1370, 'LEY': 1383, 'KT1': 1371, 
    'POK': 1381, 'SWC': 1372, 'MAN':1388
    #'JHD': 899, 'NGT': 1387,'E1L': 1356,
}




# %%
# =======================================================
# ==              第一段：查询【当天】数据                 ==
# =======================================================

if 'auth_token' in locals() and auth_token:
    print("\n\n==================== 开始执行【今日】数据查询 ====================")
    s = requests.Session()
    api_url = 'https://cps.cirroparcel.nl/prod-api/ops/centerPack/totalCount'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Content-Type': 'application/json;charset=UTF-8',
        'Authorization': auth_token
    }
    
    # 1. 修改变量名，用于存储今天的结果
    results_today = []

    for dest_name, dest_id in id_to_name_mapping.items(): # 假设 id_to_name_mapping 已定义
        print(f"--- 正在查询 [今日] 数据: {dest_name} (ID: {dest_id}) ---")
        
        payload = {
          "pageNum": 1,
          "pageSize": 50,
          "packageNoList": [],
          "destinId": dest_id,
          "departedList": ["2", "7", "1", "5", "6"],
          # 2. 使用“当天”的时间变量
          "checkInBeginTime": today_begin_time, # 假设 today_begin_time 已定义
          "checkInEndTime": today_end_time    # 假设 today_end_time 已定义
        }
        
        try:
            response = s.post(api_url, headers=headers, data=json.dumps(payload), verify=False, timeout=20)
            
            if response.status_code == 200:
                total_count = response.json().get('data', {}).get('totalCount', 0)
                print(f"查询成功: {dest_name} 的 totalCount 是 {total_count}")
                # 3. 将结果追加到今天的列表中
                results_today.append({
                    'destinId': dest_id,
                    '目的地名称': dest_name,
                    '今日已生产': total_count
                })
            else:
                print(f"查询失败: {dest_name}，服务器状态码: {response.status_code}")
                results_today.append({'destinId': dest_id, '目的地名称': dest_name, '今日已生产': '查询失败'})
        except requests.exceptions.Timeout:
            print(f"请求超时: {dest_name} (超过20秒未响应)")
            results_today.append({'destinId': dest_id, '目的地名称': dest_name, '今日已生产': '请求超时'})
        except requests.exceptions.RequestException as e:
            print(f"请求异常: {dest_name}, 错误: {e}")
            results_today.append({'destinId': dest_id, '目的地名称': dest_name, '今日已生产': '请求异常'})

        time.sleep(1)
    
    # 将结果转换为 DataFrame
    df_today = pd.DataFrame(results_today)
    print("\n【今日】数据查询完成！")
    print(df_today)
    
else:
    print("错误：未能找到 auth_token。请确保已成功登录并获取 Token。")

# %%
# =======================================================
# ==             第二段：查询【前六日】数据                ==
# =======================================================

if 'auth_token' in locals() and auth_token:
    print("\n\n==================== 开始执行【前六日】数据查询 ====================")
    s = requests.Session()
    api_url = 'https://cps.cirroparcel.nl/prod-api/ops/centerPack/totalCount'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Content-Type': 'application/json;charset=UTF-8',
        'Authorization': auth_token
    }
    
    # 1. 修改变量名，用于存储前六日的结果
    results_past_6_days = []
    
    # !! 在这里修改为你需要查询的“其他状态”列表 !!
    departed_list_past = ["7", "2"]  # <--- 示例：假设你要查这些状态

    for dest_name, dest_id in id_to_name_mapping.items(): # 假设 id_to_name_mapping 已定义
        print(f"--- 正在查询 [前六日] 数据: {dest_name} (ID: {dest_id}) ---")
        
        payload = {
          "pageNum": 1,
          "pageSize": 50,
          "packageNoList": [],
          "destinId": dest_id,
          "departedList": departed_list_past, # 使用为“过去”定义的状态列表
          # 2. 使用“过去六天”的时间变量
          "checkInBeginTime": past_period_begin_time, # 假设 past_six_days_begin_time 已定义
          "checkInEndTime": past_period_end_time    # 假设 past_six_days_end_time 已定义
        }
        
        try:
            response = s.post(api_url, headers=headers, data=json.dumps(payload), verify=False, timeout=20)
            

            
            if response.status_code == 200:
                total_count = response.json().get('data', {}).get('totalCount', 0)
                print(f"查询成功: {dest_name} 的 totalCount 是 {total_count}")
                # 3. 将结果追加到前六日的列表中
                results_past_6_days.append({
                    'destinId': dest_id,
                    '目的地名称': dest_name,
                    '前六日库存': total_count
                })
            else:
                print(f"查询失败: {dest_name}，服务器状态码: {response.status_code}")
                results_past_6_days.append({'destinId': dest_id, '目的地名称': dest_name, '前六日库存': '查询失败'})
        except requests.exceptions.Timeout:
            print(f"请求超时: {dest_name} (超过20秒未响应)")
            results_past_6_days.append({'destinId': dest_id, '目的地名称': dest_name, '前六日库存': '请求超时'})
        except requests.exceptions.RequestException as e:
            print(f"请求异常: {dest_name}, 错误: {e}")
            results_past_6_days.append({'destinId': dest_id, '目的地名称': dest_name, '前六日库存': '请求异常'})

        time.sleep(1)

    # 将结果转换为 DataFrame
    df_past_6_days = pd.DataFrame(results_past_6_days)
    print("\n【前六日】数据查询完成！")
    print(df_past_6_days)

else:
    print("错误：未能找到 auth_token。请确保已成功登录并获取 Token。")

# %%
# =======================================================
# ==         查询到件--待签入 status=1            ==
# =======================================================

if 'auth_token' in locals() and auth_token:
    print("\n\n==================== 开始执行【到件--待签入】数据查询 ====================")
    s = requests.Session()
    api_url = 'https://cps.cirroparcel.nl/prod-api/dbu_report/common/magic/eu/center/board/status/details'
    
    # =================================================================================
    # ==  !! 关键 1：严格按照您截图中的 Headers 进行构建 !!  ==
    # =================================================================================
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Authorization': auth_token,
        'Channel-Id': 'nl',
        'Content-Type': 'application/json', 
        'Date-Time-Format': 'HH:mm:ss dd/MM/yyyy',
        'Dnt': '1',
        'Lang': 'zh',
        'Origin': 'https://cps.cirroparcel.nl',
        'Sec-Ch-Ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Timezone': 'GMT+0100',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
        'User-Time-Zone': 'Europe/Amsterdam'
    }
    # =================================================================================
    
    results_wait_collect = []
    today_str = datetime.date.today().strftime('%Y-%m-%d')
    for dest_name, dest_id in id_to_name_mapping.items(): 
        print(f"--- 正在查询 [到件--待签入] 数据: {dest_name} (ID: {dest_id}) ---")
        
        # =================================================================================
        # ==  !! 关键 2：严格按照您截图中的 Payload 进行构建 (timeArr: None) !!  ==
        # =================================================================================
        payload = {
            "custNos": [],
            "status": 1,
            "centerIds": [753],
            "timeArr": [], 
            "nextIds": [],
            "targetSiteId": dest_id,
            "startTime": today_str,
            "endTime": today_str,
            "pageNum": 1,
            "pageSize": 10
        }
        
        try:
            response = s.post(api_url, headers=headers, data=json.dumps(payload), verify=False, timeout=20)
            
            if response.status_code == 200:
                response_json = response.json()
                data_dict = response_json.get('data')
                records = data_dict.get('records') if data_dict else None
                wait_count = 0
                
                if records: 
                    wait_count = records[0].get('waitCheckInWaybillCnt', 0)
                
                print(f"查询成功: {dest_name} 的 waitCheckInWaybillCnt 是 {wait_count}")
                results_wait_collect.append({'destinId': dest_id, '目的地名称': dest_name, '到件待签入': wait_count})
            else:
                print(f"查询失败: {dest_name}，服务器状态码: {response.status_code}")
                results_wait_collect.append({'destinId': dest_id, '目的地名称': dest_name, '到件待签入': '查询失败'})
        except requests.exceptions.RequestException as e:
            print(f"请求异常: {dest_name}, 错误: {e}")
            results_wait_collect.append({'destinId': dest_id, '目的地名称': dest_name, '到件待签入': '请求异常'})

        time.sleep(1)

    df_wait_collect = pd.DataFrame(results_wait_collect)
    print("\n【到件待签入】数据查询完成！")
    print(df_wait_collect)

else:
    print("错误：未能找到 auth_token。请确保已成功登录并获取 Token。")

# %%
#=======================================================
# ==         获取签入--待集包    status=2    ==
# =======================================================

if 'auth_token' in locals() and auth_token:
    print("\n\n==================== 开始执行【签入待集包】数据查询 ====================")
    s = requests.Session()
    api_url = 'https://cps.cirroparcel.nl/prod-api/dbu_report/common/magic/eu/center/board/status/details'
    
    # --- Headers (保持不变) ---
    headers = {
        'Accept': 'application/json, text/plain, */*', 'Authorization': auth_token, 'Channel-Id': 'nl',
        'Content-Type': 'application/json', 'Date-Time-Format': 'HH:mm:ss dd/MM/yyyy', 'Dnt': '1',
        'Lang': 'zh', 'Origin': 'https://cps.cirroparcel.nl',
        'Sec-Ch-Ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
        'Sec-Ch-Ua-Mobile': '?0', 'Sec-Ch-Ua-Platform': '"Windows"', 'Timezone': 'GMT+0100',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
        'User-Time-Zone': 'Europe/Amsterdam'
    }
    
    # --- 1. 创建一个新的列表，专门用于存储本次查询的结果 ---
    results_status_2 = []
    today_str = datetime.date.today().strftime('%Y-%m-%d')

    # --- 2. 开始遍历所有目的地 ---
    for dest_name, dest_id in id_to_name_mapping.items(): 
        print(f"--- 正在查询 签入待集包数据: {dest_name} (ID: {dest_id}) ---")
        
        # --- 3. 构建 status 为 2 的 Payload ---
        payload = {
            "custNos": [],
            "status": 2, # <-- 核心区别在这里
            "centerIds": [753],
            "timeArr": [],
            "nextIds": [],
            "targetSiteId": dest_id,
            "startTime": today_str,
            "endTime": today_str,
            "pageNum": 1,
            "pageSize": 10
        }
        
        try:
            response = s.post(api_url, headers=headers, data=json.dumps(payload), verify=False, timeout=20)
            
            if response.status_code == 200:
                response_json = response.json()
                data_dict = response_json.get('data')
                records = data_dict.get('records') if data_dict else None
                wait_count = 0
                
                if records: 
                    # --- 4. 提取我们需要的 waitCollectAndGroupCnt ---
                    wait_count = records[0].get('waitCollectAndGroupCnt', 0)
                
                print(f"查询成功: {dest_name} 的 waitCollectAndGroupCnt 是 {wait_count}")

                # --- 5. 将结果存入新列表，并使用新的列名 ---
                results_status_2.append({
                    'destinId': dest_id,
                    '目的地名称': dest_name,
                    '签入待集包': wait_count # <-- 使用新的列名
                })
            else:
                print(f"查询失败: {dest_name}，服务器状态码: {response.status_code}")
                results_status_2.append({'destinId': dest_id, '目的地名称': dest_name, '签入待集包': '查询失败'})
        except requests.exceptions.RequestException as e:
            print(f"请求异常: {dest_name}, 错误: {e}")
            results_status_2.append({'destinId': dest_id, '目的地名称': dest_name, '签入待集包': '请求异常'})

        time.sleep(1)

    # --- 6. 将结果转换为一个新的 DataFrame ---
    df_status_2 = pd.DataFrame(results_status_2)
    print("\n【签入待集包】数据查询完成！")
    print(df_status_2)

else:
    print("错误：未能找到 auth_token。请确保已成功登录并获取 Token。")

# %%

df_merge = pd.merge(df_today, df_past_6_days, on=['destinId', '目的地名称'], how='outer')

# 再合并 df_wait_collect
df_merge = pd.merge(df_merge, df_wait_collect, on=['destinId', '目的地名称'], how='outer')
df_merge = pd.merge(df_merge, df_status_2, on=['destinId', '目的地名称'], how='outer')
df_merge['当前货量'] = (df_merge['今日已生产'] + df_merge['前六日库存']+ df_merge['签入待集包'])
df_merge['货量预估'] = (df_merge['当前货量'] + df_merge['到件待签入'])
# 打印最终结果
print(df_merge)


# %%
bot_mapping = {
    "PSW": "https://open.feishu.cn/open-apis/bot/v2/hook/bd1776d2-bf7f-4bbe-8bd3-e44eca8c3a4f",
    "C4T": "https://open.feishu.cn/open-apis/bot/v2/hook/a5d67e93-0000-40a5-bfc8-dafdd5aeac32",
    "WER": "https://open.feishu.cn/open-apis/bot/v2/hook/a8e2666b-d0dd-419b-b706-a65742a2bd69",
    "ANA": "https://open.feishu.cn/open-apis/bot/v2/hook/37c5a6ee-5a8c-4de5-8964-798649fc364a",
    "MEK": "https://open.feishu.cn/open-apis/bot/v2/hook/1be920d5-3e51-4495-a6ee-46e0cafd8c94",
    #"JHD": "https://open.feishu.cn/open-apis/bot/v2/hook/78499cfe-42ce-414a-815c-5feeaaf675cb",
    "INB": "https://open.feishu.cn/open-apis/bot/v2/hook/8f132424-c7fd-4fd5-a16a-425f83b083d5",
    "RIN": "https://open.feishu.cn/open-apis/bot/v2/hook/8af7ddf9-6af5-43bc-84f7-566baebea047",
    "ACT": "https://open.feishu.cn/open-apis/bot/v2/hook/8794cb6b-5734-420e-8684-c0eb9749f598",
    "RSR": "https://open.feishu.cn/open-apis/bot/v2/hook/0097d1c3-36c9-4880-afbc-af6d5abe9275",
    "SAM": "https://open.feishu.cn/open-apis/bot/v2/hook/09b83a29-433f-49f3-8635-e3a0a18a3077",
    "OMT": "https://open.feishu.cn/open-apis/bot/v2/hook/058b48dc-6979-4d3c-ab4f-f089a1fa1c60",
    "RSL": "https://open.feishu.cn/open-apis/bot/v2/hook/28f3b5e2-a316-4a84-b994-2e091093cc03",
    "DET": "https://open.feishu.cn/open-apis/bot/v2/hook/c0da2b16-b8e8-4316-8292-08f13ea25715",
    "AAT": "https://open.feishu.cn/open-apis/bot/v2/hook/a760722a-e32c-49cb-b4b4-bbfac737518f",
    "SAS": "https://open.feishu.cn/open-apis/bot/v2/hook/b8c2177e-a17f-42d2-b175-ac24ed71340d",
    "GAL": "https://open.feishu.cn/open-apis/bot/v2/hook/866f6dd5-a8aa-4454-bf99-207b11d382f9",
    "CEK": "https://open.feishu.cn/open-apis/bot/v2/hook/c42978a2-826b-4974-9162-cac3e2ed572b",
    "RKM": "https://open.feishu.cn/open-apis/bot/v2/hook/25eaa0c5-90ac-4028-82bd-9803c63631f3",
    "AAA": "https://open.feishu.cn/open-apis/bot/v2/hook/160b24c1-1cb3-4e5f-814b-d8d244f8f978",
    "TSI": "https://open.feishu.cn/open-apis/bot/v2/hook/a4841ae0-5e7b-46fc-a8a5-357fe5c50630",
    "BTY": "https://open.feishu.cn/open-apis/bot/v2/hook/35e9f4e0-d27c-4681-9087-4c2097e97c7d",
    "SFT": "https://open.feishu.cn/open-apis/bot/v2/hook/0d08292a-af0e-4bf6-8724-4542b626ae46",
    "FPS": "https://open.feishu.cn/open-apis/bot/v2/hook/16bd74ca-b880-487c-be21-65dc83b42a4f",
    "BEN": "https://open.feishu.cn/open-apis/bot/v2/hook/d3cde48e-7720-4fec-b65e-8eba33e0dbae",
    "BMB": "https://open.feishu.cn/open-apis/bot/v2/hook/51abaae6-88c7-4fc5-bddc-92c5c010344a",
    "YKY": "https://open.feishu.cn/open-apis/bot/v2/hook/04db8bca-2e2c-4fe9-8c59-1cbf77fa5d42",
    "G6T": "https://open.feishu.cn/open-apis/bot/v2/hook/fe7a2762-e23a-48e8-9194-02904871270a",
    "B88": "https://open.feishu.cn/open-apis/bot/v2/hook/b546eda9-6e98-49ec-9414-85e49b00b0f0",
    "XXX": "https://open.feishu.cn/open-apis/bot/v2/hook/615b8908-2e12-4bb1-933c-0a5837ec607b",
    #"E1L": "https://open.feishu.cn/open-apis/bot/v2/hook/79fa57a2-9bcc-4414-bce6-68fb92c83a10",
    "T7Q": "https://open.feishu.cn/open-apis/bot/v2/hook/c8fce7f9-d01c-46f0-9fd7-330710f9bc7d",
    "VT2": "https://open.feishu.cn/open-apis/bot/v2/hook/107f5940-4abc-4b7f-8838-03d0c8eef77f",
    "AFM": "https://open.feishu.cn/open-apis/bot/v2/hook/f9224be2-e834-41f4-8373-7e6cb561226a",
    "TR6": "https://open.feishu.cn/open-apis/bot/v2/hook/a95e75de-b77c-4278-a178-80211c4d33a6",
    "BAL": "https://open.feishu.cn/open-apis/bot/v2/hook/7db751cf-75b7-4753-a920-cb90cf6cd212",
    "KT1": "https://open.feishu.cn/open-apis/bot/v2/hook/5ad729cb-c477-4360-b5f7-b7e295e0079f",
    "DIA": "https://open.feishu.cn/open-apis/bot/v2/hook/dcb0f50d-72a0-4735-a8c2-f4b4872748bb",
    "BFF": "https://open.feishu.cn/open-apis/bot/v2/hook/22aa8100-c1ac-47e5-8f23-548ccea9916d",
    "TEE": "https://open.feishu.cn/open-apis/bot/v2/hook/55591948-7fc4-465f-9144-9a83951ebbc0",
    "SWC": "https://open.feishu.cn/open-apis/bot/v2/hook/857ddb47-24cd-4d49-a089-c2cc61d12e79",
    "LEY": "https://open.feishu.cn/open-apis/bot/v2/hook/daeb8c2a-1615-4fef-b67a-50211a1ac1c8",
    "VXO": "https://open.feishu.cn/open-apis/bot/v2/hook/2cfc9785-62ac-4596-872a-f08693a212a9",
    "LOG": "https://open.feishu.cn/open-apis/bot/v2/hook/9c721c83-fe57-4eec-b83d-2d8f49cf1ad0",
    "HA6": "https://open.feishu.cn/open-apis/bot/v2/hook/dc4561ce-9d55-4fbc-8c17-f147263ebb4d",
    "TNZ": "https://open.feishu.cn/open-apis/bot/v2/hook/8a7a6f3a-bf7a-43dc-92e9-d646291de8d0",
    "POK": "https://open.feishu.cn/open-apis/bot/v2/hook/755341c2-4b92-44c3-bccb-844fb2716eb1",
    "C5S": "https://open.feishu.cn/open-apis/bot/v2/hook/827b5779-5607-4f0d-aee2-67d9e92b0d33",
    "BMW": "https://open.feishu.cn/open-apis/bot/v2/hook/47e0010c-e016-4c61-9cc5-66919a2649de",
    "TOP": "https://open.feishu.cn/open-apis/bot/v2/hook/26af2598-035f-4327-95fa-32c8f428adab",
    "MOF": "https://open.feishu.cn/open-apis/bot/v2/hook/d7febf15-1965-4ac5-9117-87643a7c5571",
    "LAK": "https://open.feishu.cn/open-apis/bot/v2/hook/da3b7177-6c4e-487f-8469-1b977ed6ef3f",
    #"NGT": "https://open.feishu.cn/open-apis/bot/v2/hook/a5cf4557-53d1-45d4-a57e-d65673a24d54",
    "MAN": "https://open.feishu.cn/open-apis/bot/v2/hook/ede70a5a-1baf-4f24-ad1e-417551df3a62",
    "PMS": "https://open.feishu.cn/open-apis/bot/v2/hook/31bdf103-7ec9-4429-a27a-c709fef64c05"
}
    


print(f"成功创建了 {len(bot_mapping)} 个目的地的机器人映射。")

# %%
# 将列表转换为以“名称”为键的字典，以便快速查找
station_details = {station['name']: station for station in stations}

if 'df_merge' in locals() and 'bot_mapping' in locals() and 'station_details' in locals():
    print("\n\n==================== 开始为每个目的地发送飞书卡片 ====================")
    
    for index, row in df_merge.iterrows():
        # --- 1. 提取数据 ---
        dest_name = row['目的地名称']
        today_count = row['当前货量']
        total_count = row['货量预估']
        
        # --- 2. 查找信息 ---
        webhook_url = bot_mapping.get(dest_name)
        details = station_details.get(dest_name)
        
        if not webhook_url:
            print(f"警告：未找到 '{dest_name}' 的 webhook 地址，已跳过。")
            continue
        
        pickup_time = details['pickup_time'] if details else 'N/A'
        platform = details['platform'] if details else 'N/A'
            
        print(f"准备发送卡片消息到 {dest_name}...")
        
        # =========================================================================
        # == !! 核心修正：这是一个常规的 Python 字典，不是 f-string !! ==
        # =========================================================================
        payload = {
            "msg_type": "interactive",
            "card": {
                "header": {
                    "template": "blue",
                    "title": {
                        "tag": "plain_text",
                        "content": f"Volume Forecast {dest_name}" # <-- f-string 只用在这里
                    }
                },
                "elements": [
                    {
                        "tag": "div",
                        "fields": [
                            {"is_short": True, "text": {"tag": "lark_md", "content": f"**Already Sorted**\n<font color='blue'>{today_count}</font>"}},
                            {"is_short": True, "text": {"tag": "lark_md", "content": f"**Estimated Total Number**\n<font color='green'>{total_count}</font>"}},
                            {"is_short": False, "text": {"tag": "lark_md", "content": ""}},
                            #{"is_short": True, "text": {"tag": "lark_md", "content": f"**预计托数**\n<font color='grey'>{math.ceil(total_count/150)}</font>"}}
                        ]
                    },
                    {"tag": "hr"},
                    {
                        "tag": "div",
                        "fields": [
                            {"is_short": True, "text": {"tag": "lark_md", "content": f"**Pick up time**\n{pickup_time}"}},
                            {"is_short": True, "text": {"tag": "lark_md", "content": f"**Dock**\n{platform}"}}
                        ]
                    },
                    {"tag": "hr"},
                    {
                        "tag": "note",
                        "elements": [{"tag": "plain_text", "content": f"更新时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"}]
                    }
                ]
            }
        }
        # =========================================================================
        
        headers = {'Content-Type': 'application/json'}
        
        # --- 4. 发送请求 ---
        try:
            response = requests.post(webhook_url, headers=headers, data=json.dumps(payload), timeout=10)
            if response.status_code == 200 and response.json().get("StatusCode") == 0:
                print(f"-> {dest_name} 卡片消息发送成功！")
            else:
                print(f"-> {dest_name} 卡片消息发送失败！响应: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"-> {dest_name} 卡片消息发送异常: {e}")

        time.sleep(1)

    print("\n==================== 所有卡片消息发送任务已完成 ====================")

else:
    print("错误：未能找到 df_merge, bot_mapping, 或 station_details。请确保所有准备工作已完成。")

# %% [markdown]
# 添加需要额外发送的群和机器人

# %%
bot_mapping = {
    
    "WER": "https://open.feishu.cn/open-apis/bot/v2/hook/120e1bf5-7050-4e57-93c3-b7f640c42992",
    
}
    


print(f"成功创建了 {len(bot_mapping)} 个目的地的机器人映射。")

# %%
# 将列表转换为以“名称”为键的字典，以便快速查找
station_details = {station['name']: station for station in stations}

if 'df_merge' in locals() and 'bot_mapping' in locals() and 'station_details' in locals():
    print("\n\n==================== 开始为每个目的地发送飞书卡片 ====================")
    
    for index, row in df_merge.iterrows():
        # --- 1. 提取数据 ---
        dest_name = row['目的地名称']
        today_count = row['当前货量']
        total_count = row['货量预估']
        
        # --- 2. 查找信息 ---
        webhook_url = bot_mapping.get(dest_name)
        details = station_details.get(dest_name)
        
        if not webhook_url:
            print(f"警告：未找到 '{dest_name}' 的 webhook 地址，已跳过。")
            continue
        
        pickup_time = details['pickup_time'] if details else 'N/A'
        platform = details['platform'] if details else 'N/A'
            
        print(f"准备发送卡片消息到 {dest_name}...")
        
        # =========================================================================
        # == !! 核心修正：这是一个常规的 Python 字典，不是 f-string !! ==
        # =========================================================================
        payload = {
            "msg_type": "interactive",
            "card": {
                "header": {
                    "template": "blue",
                    "title": {
                        "tag": "plain_text",
                        "content": f"Volume Forecast {dest_name}" # <-- f-string 只用在这里
                    }
                },
                "elements": [
                    {
                        "tag": "div",
                        "fields": [
                            {"is_short": True, "text": {"tag": "lark_md", "content": f"**Already Sorted**\n<font color='blue'>{today_count}</font>"}},
                            {"is_short": True, "text": {"tag": "lark_md", "content": f"**Estimated Total Number**\n<font color='green'>{total_count}</font>"}},
                            {"is_short": False, "text": {"tag": "lark_md", "content": ""}},
                            #{"is_short": True, "text": {"tag": "lark_md", "content": f"**预计托数**\n<font color='grey'>{math.ceil(total_count/150)}</font>"}}
                        ]
                    },
                    {"tag": "hr"},
                    {
                        "tag": "div",
                        "fields": [
                            {"is_short": True, "text": {"tag": "lark_md", "content": f"**Pick up time**\n{pickup_time}"}},
                            {"is_short": True, "text": {"tag": "lark_md", "content": f"**Dock**\n{platform}"}}
                        ]
                    },
                    {"tag": "hr"},
                    {
                        "tag": "note",
                        "elements": [{"tag": "plain_text", "content": f"更新时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"}]
                    }
                ]
            }
        }
        # =========================================================================
        
        headers = {'Content-Type': 'application/json'}
        
        # --- 4. 发送请求 ---
        try:
            response = requests.post(webhook_url, headers=headers, data=json.dumps(payload), timeout=10)
            if response.status_code == 200 and response.json().get("StatusCode") == 0:
                print(f"-> {dest_name} 卡片消息发送成功！")
            else:
                print(f"-> {dest_name} 卡片消息发送失败！响应: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"-> {dest_name} 卡片消息发送异常: {e}")

        time.sleep(1)

    print("\n==================== 所有卡片消息发送任务已完成 ====================")

else:
    print("错误：未能找到 df_merge, bot_mapping, 或 station_details。请确保所有准备工作已完成。")

# %%
# 确保 df_merge DataFrame 存在且不为空
if 'df_merge' in locals() and not df_merge.empty:
    
    # 1. 定义要保存的文件名
    output_filename = '最终合并报告.xlsx'
    
    try:
        # 2. 调用 to_excel 方法
        #    index=False 表示不将 DataFrame 的索引（0, 1, 2...）写入 Excel 文件
        #    sheet_name='数据汇总' 是给 Excel 文件中的工作表命名
        df_merge.to_excel(output_filename, index=False, sheet_name='数据汇总')
        
        # 3. 打印确认信息
        print(f"\n✅ 最终的合并数据表已成功保存到文件: {output_filename}")
        
    except Exception as e:
        # 捕获可能发生的写入错误（例如，文件被占用或权限问题）
        print(f"\n❌ 保存文件时出错: {e}")

else:
    print("\n错误：未能找到最终的 DataFrame (df_merge)，无法保存到文件。")


