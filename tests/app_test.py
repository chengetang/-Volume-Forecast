# %%
import time
import math
import pandas as pd
import requests
import json
import os
import datetime
import base64
import subprocess
import sys
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By

# 关闭 requests 库关于 InsecureRequestWarning 的警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

print("库导入成功")

# =======================================================
# ==                   导入配置文件                      ==
# =======================================================

# 统一的脚本目录/配置文件路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE_NAME = "config_data_test.py"
CONFIG_FILE_PATH = os.path.join(SCRIPT_DIR, CONFIG_FILE_NAME)   

"""重新加载配置"""
print("\n" + "="*50)
print("           系统初始化")
print("="*50)

try:
    modules_to_clear = ['config_data_test']
    for module in modules_to_clear:
        if module in sys.modules:
            del sys.modules[module]
            print(f"🗑️  已清除模块: {module}")
    
    if SCRIPT_DIR not in sys.path:
        sys.path.insert(0, SCRIPT_DIR)
    
    global stations, API_CONFIG, QUERY_CONFIG, HEADERS_CONFIG
    global TOKEN_CONFIG, FEISHU_CONFIG, OUTPUT_CONFIG, SYSTEM_CONFIG
    
    from config_data_test import (
        stations, API_CONFIG, QUERY_CONFIG, HEADERS_CONFIG,
        TOKEN_CONFIG, FEISHU_CONFIG, OUTPUT_CONFIG, SYSTEM_CONFIG
    )
    print("✅ 配置文件加载成功")
    print(f"📊 加载的站点数量: {len(stations)}")
    for station in stations[:3]:
        print(f"   - {station['name']} (ID: {station['id']})")
except ImportError as e:
    print(f"❌ 配置文件加载失败: {e}")

# =======================================================
# ==              账号密码本地存储 & 获取                 ==
# =======================================================

def get_auth_info():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(script_dir, 'config_local_test.json')

    # 如果本地文件存在，直接读取
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                auth_data = json.load(f)
            print("✅ 从本地文件加载认证信息成功")
            return auth_data
        except Exception as e:
            print(f"❌ 读取本地文件失败: {e}")
    
    # 要求用户输入（第一次运行会走到这里）
    print("\n" + "="*50)
    print("首次使用，请输入登录信息")
    print("="*50)
    
    username = input("用户名: ").strip()
    password = input("密码: ").strip()
    
    if not username or not password:
        print("❌ 用户名和密码不能为空")
        return None
    
    # 保存到本地文件
    try:
        auth_data = {'username': username, 'password': password}
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(auth_data, f, ensure_ascii=False, indent=2)
        print("✅ 认证信息已保存到本地文件")
        return auth_data
    except Exception as e:
        print(f"❌ 保存失败: {e}")
        return {'username': username, 'password': password}

# 获取认证信息
auth_info = get_auth_info()
if not auth_info:
    print("❌ 无法获取认证信息，程序退出")
    exit(1)

USERNAME = auth_info['username']
PASSWORD = auth_info['password']
print(f"✅ 使用用户: {USERNAME}")

# =======================================================
# ==                 浏览器初始化                       ==
# =======================================================

driver = webdriver.Chrome()
print("浏览器启动成功")
# 替换为你要登录的网址
login_url = 'https://cps.cirroparcel.nl/login' # 登录页
driver.get(login_url)

# 等待页面加载
time.sleep(3) 

# --- 使用 XPath 定位元素并填写 ---
try:
    username_field = driver.find_element(By.XPATH, '//input[@placeholder="手机号" or @placeholder="Phone number" or @placeholder="telefoonnummer"]')
    username_field.send_keys(USERNAME)  # 使用从认证函数获取的用户名

    password_field = driver.find_element(By.XPATH, '//input[@placeholder="密码" or @placeholder="Password" or @placeholder="wachtwoord"]')
    password_field.send_keys(PASSWORD)  # 使用从认证函数获取的密码
except Exception as e:
    print(f"自动填写用户名/密码失败: {e}")
    print("请手动填写所有登录信息。")

# --- 点击复选框 ---
print("📝 点击未选中的复选框...")
try:
    checkboxes = driver.find_elements(By.XPATH, '//input[@type="checkbox"]')
    
    for checkbox in checkboxes:
        if not checkbox.is_selected():
            checkbox.click()
    
    print("✅ 复选框已点击")
    
except Exception as e:
    print(f"❌ 处理复选框失败: {e}")

# --- 手动验证码输入 ---
print("\n" + "="*50)
print("请手动输入验证码，并在浏览器中完成登录操作。")
print("="*50)
input("确认登录成功后，请按 Enter 键继续...")

print("登录完成，准备提取 Cookies 并请求 API...")

# =======================================================
# ==                 时间计算                          ==
# =======================================================

# --- 1. 获取基础日期 ---
today_date = datetime.date.today()
six_days_ago_date = today_date - datetime.timedelta(days=6)
yesterday_date = today_date - datetime.timedelta(days=1) 

# --- 2. 计算并存储到四个变量中 ---
today_begin_time = today_date.strftime('%Y-%m-%d') + " 00:00:00"
today_end_time = today_date.strftime('%Y-%m-%d') + " 23:59:59"
past_period_begin_time = six_days_ago_date.strftime('%Y-%m-%d') + " 00:00:00"
past_period_end_time = yesterday_date.strftime('%Y-%m-%d') + " 23:59:59"

# --- 3. 打印所有四个变量以供检查 ---
print("="*20 + " 当天时间范围 " + "="*20)
print(f"变量 'today_begin_time':     {today_begin_time}")
print(f"变量 'today_end_time':       {today_end_time}")
print("\n" + "="*20 + " 过去六天到昨天的时间范围 " + "="*20)
print(f"变量 'past_period_begin_time': {past_period_begin_time}")
print(f"变量 'past_period_end_time':   {past_period_end_time}")

# =======================================================
# ==                 获取 Token                        ==
# =======================================================

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

# =======================================================
# ==              第一段：查询【当天】数据                 ==
# =======================================================

if 'auth_token' in locals() and auth_token:
    print("\n\n========== 开始执行【今日】数据查询 ==========")
    s = requests.Session()

    # 使用配置中的 API URL和请求头
    api_url = f"{API_CONFIG['base_url']}{API_CONFIG['endpoints']['total_count']}"
    headers = HEADERS_CONFIG['common_headers'].copy()
    headers['Authorization'] = auth_token
    
    results_today = []

    # 遍历站点列表，获取站点名称和ID
    for station in stations:
        dest_name = station['name']
        dest_id = station['id']

        print(f"--- 正在查询 [今日] 数据: {dest_name} (ID: {dest_id}) ---")
        
        payload = {
            "pageNum": 1,
            "pageSize": QUERY_CONFIG['page_size'],
            "packageNoList": [],
            "destinId": dest_id,
            "departedList": QUERY_CONFIG['departed_list_today'],
            "checkInBeginTime": today_begin_time,
            "checkInEndTime": today_end_time
        }
        
        try:
            response = requests.post(api_url, headers=headers, json=payload, timeout=API_CONFIG['timeout'])
            
            if response.status_code == 200:
                total_count = response.json().get('data', {}).get('totalCount', 0)
                print(f"查询成功: {dest_name} 的 totalCount 是 {total_count}")

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

        time.sleep(SYSTEM_CONFIG['sleep_between_requests'])
    
    df_today = pd.DataFrame(results_today)
    print("\n【今日】数据查询完成！")
    print(df_today)
    
else:
    print("错误：未能找到 auth_token。请确保已成功登录并获取 Token。")

# =======================================================
# ==             第二段：查询【前六日】数据                ==
# =======================================================

if 'auth_token' in locals() and auth_token:
    print("\n\n========== 开始执行【前六日】数据查询 ==========")
    s = requests.Session()
    api_url = f"{API_CONFIG['base_url']}{API_CONFIG['endpoints']['total_count']}"
    
    headers = HEADERS_CONFIG['common_headers'].copy()
    headers['Authorization'] = auth_token
    
    results_past_6_days = []

    for station in stations:
        dest_name = station['name']
        dest_id = station['id']
        print(f"--- 正在查询 [前六日] 数据: {dest_name} (ID: {dest_id}) ---")
        
        payload = {
            "pageNum": 1,
            "pageSize": QUERY_CONFIG['page_size'],
            "packageNoList": [],
            "destinId": dest_id,
            "departedList": QUERY_CONFIG['departed_list_past'],
            "checkInBeginTime": past_period_begin_time,
            "checkInEndTime": past_period_end_time
        }
        
        try:
            response = requests.post(api_url, headers=headers, json=payload, timeout=API_CONFIG['timeout'])
        
            
            if response.status_code == 200:
                total_count = response.json().get('data', {}).get('totalCount', 0)
                print(f"查询成功: {dest_name} 的 totalCount 是 {total_count}")

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

    df_past_6_days = pd.DataFrame(results_past_6_days)
    print("\n【前六日】数据查询完成！")
    print(df_past_6_days)

else:
    print("错误：未能找到 auth_token。请确保已成功登录并获取 Token。")

# =======================================================
# ==         查询到件--待签入 status=1            ==
# =======================================================

if 'auth_token' in locals() and auth_token:
    print("\n\n==================== 开始执行【到件--待签入】数据查询 ====================")
    s = requests.Session()
    api_url = f"{API_CONFIG['base_url']}{API_CONFIG['endpoints']['status_details']}"
    
    # 使用特殊请求头
    headers = HEADERS_CONFIG['special_headers'].copy()
    headers['Authorization'] = auth_token
    
    results_wait_collect = []
    today_str = datetime.date.today().strftime('%Y-%m-%d')

    for station in stations:
        dest_name = station['name']
        dest_id = station['id']
        print(f"--- 正在查询 [到件--待签入] 数据: {dest_name} (ID: {dest_id}) ---")
        
        payload = {
            "custNos": [],
            "status": 1,
            "centerIds": QUERY_CONFIG['center_ids'],
            "timeArr": [], 
            "nextIds": [],
            "targetSiteId": dest_id,
            "startTime": today_str,
            "endTime": today_str,
            "pageNum": 1,
            "pageSize": QUERY_CONFIG['status_page_size']
        }
        
        try:
            response = requests.post(api_url, headers=headers, json=payload, timeout=API_CONFIG['timeout'])
            
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

        time.sleep(SYSTEM_CONFIG['sleep_between_requests'])

    df_wait_collect = pd.DataFrame(results_wait_collect)
    print("\n【到件待签入】数据查询完成！")
    print(df_wait_collect)

else:
    print("错误：未能找到 auth_token。请确保已成功登录并获取 Token。")

# =======================================================
# ==             获取签入--待集包 status=2              ==
# =======================================================

if 'auth_token' in locals() and auth_token:
    print("\n\n==================== 开始执行【签入待集包】数据查询 ====================")
    s = requests.Session()
    api_url = f"{API_CONFIG['base_url']}{API_CONFIG['endpoints']['status_details']}"
    
    headers = HEADERS_CONFIG['special_headers'].copy()
    headers['Authorization'] = auth_token
    
    results_status_2 = []
    today_str = datetime.date.today().strftime('%Y-%m-%d')

    for station in stations:
        dest_name = station['name']
        dest_id = station['id']
        print(f"--- 正在查询 签入待集包数据: {dest_name} (ID: {dest_id}) ---")
        
        payload = {
            "custNos": [],
            "status": 2,
            "centerIds": QUERY_CONFIG['center_ids'],
            "timeArr": [],
            "nextIds": [],
            "targetSiteId": dest_id,
            "startTime": today_str,
            "endTime": today_str,
            "pageNum": 1,
            "pageSize": QUERY_CONFIG['status_page_size']
        }
        
        try:
            response = requests.post(api_url, headers=headers, json=payload, timeout=API_CONFIG['timeout'])
            
            if response.status_code == 200:
                response_json = response.json()
                data_dict = response_json.get('data')
                records = data_dict.get('records') if data_dict else None
                wait_count = 0
                
                if records: 
                    wait_count = records[0].get('waitCollectAndGroupCnt', 0)
                
                print(f"查询成功: {dest_name} 的 waitCollectAndGroupCnt 是 {wait_count}")
                results_status_2.append({
                    'destinId': dest_id,
                    '目的地名称': dest_name,
                    '签入待集包': wait_count
                })
            else:
                print(f"查询失败: {dest_name}，服务器状态码: {response.status_code}")
                results_status_2.append({'destinId': dest_id, '目的地名称': dest_name, '签入待集包': '查询失败'})
        except requests.exceptions.RequestException as e:
            print(f"请求异常: {dest_name}, 错误: {e}")
            results_status_2.append({'destinId': dest_id, '目的地名称': dest_name, '签入待集包': '请求异常'})

        time.sleep(SYSTEM_CONFIG['sleep_between_requests'])

    df_status_2 = pd.DataFrame(results_status_2)
    print("\n【签入待集包】数据查询完成！")
    print(df_status_2)

else:
    print("错误：未能找到 auth_token。请确保已成功登录并获取 Token。")

# =======================================================
# ==                   数据合并                         ==
# =======================================================

df_merge = pd.merge(df_today, df_past_6_days, on=['destinId', '目的地名称'], how='outer')

# 再合并 df_wait_collect
df_merge = pd.merge(df_merge, df_wait_collect, on=['destinId', '目的地名称'], how='outer')
df_merge = pd.merge(df_merge, df_status_2, on=['destinId', '目的地名称'], how='outer')
df_merge['当前货量'] = (df_merge['今日已生产'] + df_merge['前六日库存']+ df_merge['签入待集包'])
df_merge['货量预估'] = (df_merge['当前货量'] + df_merge['到件待签入'])
# 打印最终结果
print(df_merge)


# =======================================================
# ==                 发送飞书消息                       ==
# =======================================================

if 'df_merge' in locals():
    print(f"\n\n==================== 开始为 {len(stations)} 个目的地发送飞书卡片 ====================")
    
    for station in stations:
        dest_name = station['name']
        
        # 收集所有webhook地址
        webhook_urls = []
        if 'webhook' in station and station['webhook']:
            webhook_urls.append(station['webhook'])
        if 'webhook_2' in station and station['webhook_2']:
            webhook_urls.append(station['webhook_2'])

        pickup_time = station['pickup_time']
        platform = station['platform']
        
        # 从合并数据中查找对应的数据
        station_data = df_merge[df_merge['目的地名称'] == dest_name]
        
        if station_data.empty:
            print(f"警告：未在数据中找到 '{dest_name}' 的信息，已跳过。")
            continue
            
        # 提取数据
        row = station_data.iloc[0]
        today_count = row['当前货量']
        total_count = row['货量预估']
            
        print(f"准备发送卡片消息到 {dest_name}...")
        
        # 构建 payload，使用配置中的消息设置
        payload = {
            "msg_type": FEISHU_CONFIG['msg_type'],
            "card": {
                "header": {
                    "template": FEISHU_CONFIG['header_template'],
                    "title": {
                        "tag": "plain_text",
                        "content": f"Volume Forecast {dest_name}"
                    }
                },
                "elements": [
                    {
                        "tag": "div",
                        "fields": [
                            {"is_short": True, "text": {"tag": "lark_md", "content": f"**Already Sorted**\n<font color='blue'>{today_count}</font>"}},
                            {"is_short": True, "text": {"tag": "lark_md", "content": f"**Estimated Total Number**\n<font color='green'>{total_count}</font>"}},
                            {"is_short": False, "text": {"tag": "lark_md", "content": ""}},
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
                        "elements": [{"tag": "plain_text", "content": f"updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"}]
                    }
                ]
            }
        }
        
        headers = {'Content-Type': 'application/json'}
        
        # 发送请求
        success_count = 0
        for i, webhook_url in enumerate(webhook_urls, 1):
            try:
                response = requests.post(webhook_url, headers=headers, data=json.dumps(payload), 
                                       timeout=FEISHU_CONFIG['request_timeout'])
                if response.status_code == 200 and response.json().get("StatusCode") == 0:
                    success_count += 1
                    print(f"-> {dest_name} 第{i}个webhook发送成功！")
                else:
                    print(f"-> {dest_name} 第{i}个webhook发送失败！响应: {response.text}")
            except requests.exceptions.RequestException as e:
                print(f"-> {dest_name} 第{i}个webhook发送异常: {e}")

            time.sleep(FEISHU_CONFIG['sleep_between_requests'])

    print("\n==================== 所有卡片消息发送任务已完成 ====================")

else:
    print("错误：未能找到数据，请确保所有准备工作已完成。")

# =======================================================
# ==                   保存结果                         ==
# =======================================================

if 'df_merge' in locals() and not df_merge.empty:
    try:
        # 使用配置中的输出设置
        output_filename = OUTPUT_CONFIG['excel_filename']
        
        # 获取脚本所在目录的绝对路径
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 构建完整的文件路径
        full_output_path = os.path.join(script_dir, output_filename)
        
        # 保存文件
        df_merge.to_excel(full_output_path, index=False, sheet_name=OUTPUT_CONFIG['sheet_name'])
        print(f"\n✅ 最终的合并数据表已成功保存到文件: {full_output_path}")
        
    except Exception as e:
        print(f"\n❌ 保存文件时出错: {e}")

else:
    print("\n错误：未能找到最终的 DataFrame (df_merge)，无法保存到文件。")
