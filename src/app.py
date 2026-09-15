# %%
import time
import pandas as pd
import requests
import json
import os
import datetime
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By

# 关闭 requests 库关于 InsecureRequestWarning 的警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

print("库导入成功")

# =========================================================
# ==   第一部分：准备工作（登录 / 获取 Token / 日期计算）        ==
# =========================================================

# --- 导入配置文件 ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE_NAME = "config_data.py"
CONFIG_FILE_PATH = os.path.join(SCRIPT_DIR, CONFIG_FILE_NAME)

print("\n" + "="*50)
print("           系统初始化")
print("="*50)

try:
    modules_to_clear = ['config_data']
    for module in modules_to_clear:
        if module in sys.modules:
            del sys.modules[module]
            print(f"🗑️  已清除模块: {module}")

    if SCRIPT_DIR not in sys.path:
        sys.path.insert(0, SCRIPT_DIR)

    global stations, stations_special_request, API_CONFIG, QUERY_CONFIG, HEADERS_CONFIG
    global TOKEN_CONFIG, FEISHU_CONFIG, FEISHU_CONFIG_POSTCODE, SYSTEM_CONFIG, ROUTE_MAPPING_CONFIG

    from config_data import (
        stations, stations_special_request, API_CONFIG, QUERY_CONFIG, HEADERS_CONFIG,
        TOKEN_CONFIG, FEISHU_CONFIG, FEISHU_CONFIG_POSTCODE, SYSTEM_CONFIG, ROUTE_MAPPING_CONFIG
    )
    print("✅ 配置文件加载成功")
    print(f"📊 普通站点数量: {len(stations)}")
    print(f"📊 邮编明细站点数量: {len(stations_special_request)}")
    for station in stations_special_request:
        print(f"   - {station['name']} (ID: {station['id']})")
except ImportError as e:
    print(f"❌ 配置文件加载失败: {e}")


def get_auth_info():
    """从本地文件读取账号密码，没有则要求用户输入并保存"""
    config_file = os.path.join(SCRIPT_DIR, 'config_local.json')

    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                auth_data = json.load(f)
            print("✅ 从本地文件加载认证信息成功")
            return auth_data
        except Exception as e:
            print(f"❌ 读取本地文件失败: {e}")

    print("\n" + "="*50)
    print("首次使用，请输入登录信息")
    print("="*50)

    username = input("用户名: ").strip()
    password = input("密码: ").strip()

    if not username or not password:
        print("❌ 用户名和密码不能为空")
        return None

    try:
        auth_data = {'username': username, 'password': password}
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(auth_data, f, ensure_ascii=False, indent=2)
        print("✅ 认证信息已保存到本地文件")
        return auth_data
    except Exception as e:
        print(f"❌ 保存失败: {e}")
        return {'username': username, 'password': password}


# --- 登录并获取 Token ---
auth_info = get_auth_info()
if not auth_info:
    print("❌ 无法获取认证信息，程序退出")
    exit(1)

USERNAME = auth_info['username']
PASSWORD = auth_info['password']
print(f"✅ 使用用户: {USERNAME}")

driver = webdriver.Chrome()
print("浏览器启动成功")
login_url = 'https://cps.cirroparcel.nl/login'
driver.get(login_url)

time.sleep(3)

try:
    username_field = driver.find_element(By.XPATH, '//input[@placeholder="手机号" or @placeholder="Phone number" or @placeholder="telefoonnummer"]')
    username_field.send_keys(USERNAME)

    password_field = driver.find_element(By.XPATH, '//input[@placeholder="密码" or @placeholder="Password" or @placeholder="wachtwoord"]')
    password_field.send_keys(PASSWORD)
except Exception as e:
    print(f"自动填写用户名/密码失败: {e}")
    print("请手动填写所有登录信息。")

print("📝 点击未选中的复选框...")
try:
    checkboxes = driver.find_elements(By.XPATH, '//input[@type="checkbox"]')
    for checkbox in checkboxes:
        if not checkbox.is_selected():
            checkbox.click()
    print("✅ 复选框已点击")
except Exception as e:
    print(f"❌ 处理复选框失败: {e}")

print("\n" + "="*50)
print("请手动输入验证码，并在浏览器中完成登录操作。")
print("="*50)
input("确认登录成功后，请按 Enter 键继续...")

print("登录完成，准备提取 Cookies 并请求 API...")

# --- 日期计算 ---
today_date = datetime.date.today()
six_days_ago_date = today_date - datetime.timedelta(days=6)
yesterday_date = today_date - datetime.timedelta(days=1)

today_begin_time = today_date.strftime('%Y-%m-%d') + " 00:00:00"
today_end_time = today_date.strftime('%Y-%m-%d') + " 23:59:59"
past_period_begin_time = six_days_ago_date.strftime('%Y-%m-%d') + " 00:00:00"
past_period_end_time = yesterday_date.strftime('%Y-%m-%d') + " 23:59:59"
today_str = today_date.strftime('%Y-%m-%d')

# stations_special_request 专用：只查"今日"窗口（从昨天 00:00 到今天 23:59），
# 覆盖次日凌晨运行时仍是 sortFlag='N' 的昨日包裹；不再需要单独查前六日
today_begin_time_special = yesterday_date.strftime('%Y-%m-%d') + " 00:00:00"

print(f"今日范围: {today_begin_time} ~ {today_end_time}")
print(f"前六日范围: {past_period_begin_time} ~ {past_period_end_time}")
print(f"今日范围（邮编明细站点）: {today_begin_time_special} ~ {today_end_time}")

# --- 获取 Token ---
print("正在尝试从浏览器 localStorage 自动获取 Authorization Token...")
auth_token = None
try:
    time.sleep(3)
    token_key_in_storage = 'Admin-Token'
    token_value = driver.execute_script(f"return localStorage.getItem('{token_key_in_storage}');")

    if token_value:
        auth_token = token_value if token_value.startswith('Bearer ') else f'Bearer {token_value}'
        print("✅ 成功自动获取到 Token！")
    else:
        print(f"错误：在 localStorage 中找到了 Key '{token_key_in_storage}'，但其值为空。可能是登录后写入有延迟。")
except Exception as e:
    print(f"自动获取 Token 失败: {e}")
    print("请确认 Key 的名字是否拼写正确。")


def send_feishu_card(station, payload, feishu_config):
    """把 payload 发送到该站点配置的所有 webhook，逐个记录成功/失败"""
    dest_name = station['name']

    webhook_urls = []
    if station.get('webhook'):
        webhook_urls.append(station['webhook'])
    if station.get('webhook_2'):
        webhook_urls.append(station['webhook_2'])

    if not webhook_urls:
        print(f"警告：{dest_name} 未配置 webhook，已跳过发送。")
        return

    headers = {'Content-Type': 'application/json'}
    for i, webhook_url in enumerate(webhook_urls, 1):
        try:
            response = requests.post(webhook_url, headers=headers, data=json.dumps(payload),
                                      timeout=feishu_config['request_timeout'])
            if response.status_code == 200 and response.json().get("StatusCode") == 0:
                print(f"-> {dest_name} 第{i}个webhook发送成功！")
            else:
                print(f"-> {dest_name} 第{i}个webhook发送失败！响应: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"-> {dest_name} 第{i}个webhook发送异常: {e}")

        time.sleep(feishu_config['sleep_between_requests'])


# =========================================================
# ==   第二部分：普通站点 —— 聚合查询 + 原有卡片格式             ==
# =========================================================

def fetch_total_count(station, departed_list, begin_time, end_time, headers, api_url):
    """今日/前六日共用：按站点查询 totalCount 聚合数量"""
    dest_id = station['id']
    payload = {
        "pageNum": 1,
        "pageSize": QUERY_CONFIG['page_size'],
        "packageNoList": [],
        "destinId": dest_id,
        "departedList": departed_list,
        "checkInBeginTime": begin_time,
        "checkInEndTime": end_time
    }

    try:
        response = requests.post(api_url, headers=headers, data=json.dumps(payload), verify=False, timeout=API_CONFIG['timeout'])
        if response.status_code == 200:
            return response.json().get('data', {}).get('totalCount', 0)
        return '查询失败'
    except requests.exceptions.Timeout:
        return '请求超时'
    except requests.exceptions.RequestException:
        return '请求异常'


def fetch_status_aggregate(station, status_code, count_field, headers, api_url):
    """到件待签入(status=1)/签入待集包(status=2)共用：按站点查询聚合数量"""
    dest_id = station['id']
    payload = {
        "custNos": [],
        "status": status_code,
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
            data_dict = response.json().get('data')
            records = data_dict.get('records') if data_dict else None
            return records[0].get(count_field, 0) if records else 0
        return '查询失败'
    except requests.exceptions.RequestException:
        return '请求异常'


def run_normal_stations():
    if not ('auth_token' in globals() and auth_token):
        print("错误：未能找到 auth_token。请确保已成功登录并获取 Token。")
        return

    total_count_url = f"{API_CONFIG['base_url']}{API_CONFIG['endpoints']['total_count']}"
    common_headers = HEADERS_CONFIG['common_headers'].copy()
    common_headers['Authorization'] = auth_token

    status_url = f"{API_CONFIG['base_url']}{API_CONFIG['endpoints']['status_details']}"
    status_headers = HEADERS_CONFIG['special_headers'].copy()
    status_headers['Authorization'] = auth_token

    results_today, results_past_6_days = [], []
    results_wait_collect, results_status_2 = [], []

    for station in stations:
        dest_name, dest_id = station['name'], station['id']

        today_count = fetch_total_count(station, QUERY_CONFIG['departed_list_today'], today_begin_time, today_end_time, common_headers, total_count_url)
        results_today.append({'destinId': dest_id, '目的地名称': dest_name, '今日已生产': today_count})
        time.sleep(SYSTEM_CONFIG['sleep_between_requests'])

        past_count = fetch_total_count(station, QUERY_CONFIG['departed_list_past'], past_period_begin_time, past_period_end_time, common_headers, total_count_url)
        results_past_6_days.append({'destinId': dest_id, '目的地名称': dest_name, '前六日库存': past_count})
        time.sleep(SYSTEM_CONFIG['sleep_between_requests'])

        wait_count = fetch_status_aggregate(station, 1, 'waitCheckInWaybillCnt', status_headers, status_url)
        results_wait_collect.append({'destinId': dest_id, '目的地名称': dest_name, '到件待签入': wait_count})
        time.sleep(SYSTEM_CONFIG['sleep_between_requests'])

        group_count = fetch_status_aggregate(station, 2, 'waitCollectAndGroupCnt', status_headers, status_url)
        results_status_2.append({'destinId': dest_id, '目的地名称': dest_name, '签入待集包': group_count})
        time.sleep(SYSTEM_CONFIG['sleep_between_requests'])

        print(f"--- [普通站点] {dest_name} (ID: {dest_id}) 查询完成 ---")

    df_today = pd.DataFrame(results_today)
    df_past_6_days = pd.DataFrame(results_past_6_days)
    df_wait_collect = pd.DataFrame(results_wait_collect)
    df_status_2 = pd.DataFrame(results_status_2)

    # --- 数据合并 ---
    df_merge = pd.merge(df_today, df_past_6_days, on=['destinId', '目的地名称'], how='outer')
    df_merge = pd.merge(df_merge, df_wait_collect, on=['destinId', '目的地名称'], how='outer')
    df_merge = pd.merge(df_merge, df_status_2, on=['destinId', '目的地名称'], how='outer')
    df_merge['当前货量'] = df_merge['今日已生产'] + df_merge['前六日库存'] + df_merge['签入待集包']
    df_merge['货量预估'] = df_merge['当前货量'] + df_merge['到件待签入']

    # --- 构建并发送飞书卡片（原有格式） ---
    print(f"\n==================== 开始为 {len(stations)} 个目的地发送飞书卡片 ====================")
    for station in stations:
        dest_name = station['name']
        station_data = df_merge[df_merge['目的地名称'] == dest_name]

        if station_data.empty:
            print(f"警告：未在数据中找到 '{dest_name}' 的信息，已跳过。")
            continue

        row = station_data.iloc[0]
        today_count = row['当前货量']
        total_count = row['货量预估']
        pickup_time = station['pickup_time']
        platform = station['platform']

        payload = {
            "msg_type": FEISHU_CONFIG['msg_type'],
            "card": {
                "header": {
                    "template": FEISHU_CONFIG['header_template'],
                    "title": {"tag": "plain_text", "content": f"Volume Forecast {dest_name}"}
                },
                "elements": [
                    {
                        "tag": "div",
                        "fields": [
                            {"is_short": True, "text": {"tag": "lark_md", "content": f"**Already Sorted**\n<font color='blue'>{today_count}</font>"}},
                            {"is_short": True, "text": {"tag": "lark_md", "content": f"**Packages in Warehouse Now**\n<font color='green'>{total_count}</font>"}},
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

        send_feishu_card(station, payload, FEISHU_CONFIG)

    print("==================== 普通站点卡片消息发送任务已完成 ====================")


# =========================================================
# ==   第三部分：邮编明细站点 —— 两步法明细查询 + 按邮编聚合卡片   ==
# =========================================================

def route_box_sort_key(label):
    """按路线号标签里的第一个数字排序（如 '28+29+32' 排在 28 的位置），
    未匹配到路线号的标签（未知 / has no scope yet）统一排到最后。"""
    first_token = label.split('+')[0]
    try:
        return (0, int(first_token))
    except ValueError:
        return (1, label)


def load_route_mapping(relative_path):
    """读取邮编 -> 路线号映射表（第一列=路线号 Scope，第二列=邮编 Postcode，带表头）。
    同一个邮编可能对应多条路线（如相邻路线共管一个邮编），此时合并为 'A+B' 的形式展示。"""
    project_root = os.path.dirname(SCRIPT_DIR)
    mapping_path = os.path.join(project_root, relative_path)
    if not os.path.exists(mapping_path):
        print(f"⚠️ 未找到路线号映射表: {mapping_path}，相关站点将回退展示邮编")
        return {}

    df_mapping = pd.read_excel(mapping_path)
    postcode_to_routes = {}
    for _, row in df_mapping.iterrows():
        # 单元格里的路线号本身可能已经是 "29+32" 这种组合路线，先拆成单个路线号再收集，
        # 避免同一邮编出现在多行时把整段标签直接拼接，导致像 "55+60" + "60" 拼出重复的 "55+60+60"
        route_tokens = [t.strip() for t in str(row.iloc[0]).split('+') if t.strip()]
        try:
            postcode = int(row.iloc[1])
        except (ValueError, TypeError):
            continue
        postcode_to_routes.setdefault(postcode, set()).update(route_tokens)

    return {pc: '+'.join(sorted(routes, key=int)) for pc, routes in postcode_to_routes.items()}


ROUTE_MAPPING = load_route_mapping(ROUTE_MAPPING_CONFIG['file'])

detail_records = []
tracked_special_ids = {str(station['id']) for station in stations_special_request}


def collect_detail_records(records, record_type):
    for record in records:
        if str(record.get('targetSiteId')) not in tracked_special_ids:
            continue
        detail_records.append({
            'waybillNo': record.get('waybillNo'),
            'targetCenterName': record.get('targetCenterName'),
            'targetSiteId': record.get('targetSiteId'),
            'targetSiteName': record.get('targetSiteName'),
            'postCode': record.get('postCode'),
            'type': record_type
        })


def fetch_packed_detail(departed_list, begin_time, end_time, period_label):
    """已集包：selectPageList 找出 sortFlag=='N' 的包裹，再逐个查 detail 取 waybillNo/toCode"""
    if not ('auth_token' in globals() and auth_token):
        return

    list_api_url = f"{API_CONFIG['base_url']}{API_CONFIG['endpoints']['select_page_list']}"
    detail_api_url = f"{API_CONFIG['base_url']}{API_CONFIG['endpoints']['pack_detail']}"
    headers = HEADERS_CONFIG['special_headers'].copy()
    headers['Authorization'] = auth_token

    for station in stations_special_request:
        dest_name, dest_id = station['name'], station['id']

        station_records = []
        page_num = 1
        while True:
            payload = {
                "pageNum": page_num,
                "pageSize": QUERY_CONFIG['page_size'],
                "packageNoList": [],
                "destinId": dest_id,
                "departedList": departed_list,
                "checkInBeginTime": begin_time,
                "checkInEndTime": end_time
            }
            try:
                response = requests.post(list_api_url, headers=headers, json=payload, timeout=API_CONFIG['timeout'])
                if response.status_code != 200:
                    break

                data_dict = response.json().get('data') or {}
                # selectPageList 返回的是 'list' 字段；分页依据服务端返回的 'pages'/'current'
                records = data_dict.get('list') or []
                total_pages = data_dict.get('pages', 1)
                current_page = data_dict.get('current', page_num)

                for record in records:
                    station_records.append({
                        'packageNo': record.get('packageNo'),
                        'destinCenterName': record.get('destinCenterName'),
                        'destinId': record.get('destinId'),
                        'destinName': record.get('destinName'),
                        'sortFlag': record.get('sortFlag'),
                    })

                if current_page >= total_pages:
                    break
                page_num += 1
            except requests.exceptions.RequestException:
                break

            time.sleep(SYSTEM_CONFIG['sleep_between_requests'])

        df_select_page_list = pd.DataFrame(station_records)
        if df_select_page_list.empty:
            print(f"--- [已集包-{period_label}] {dest_name} 无数据 ---")
            continue

        pending_packages = df_select_page_list[df_select_page_list['sortFlag'] == 'N']
        collected_before = len(detail_records)

        for _, pkg in pending_packages.iterrows():
            detail_page_num = 1
            all_detail_items = []

            while True:
                detail_payload = {
                    "pageNum": detail_page_num,
                    "pageSize": QUERY_CONFIG['detail_page_size'],
                    "packageNo": pkg['packageNo']
                }
                try:
                    detail_response = requests.post(detail_api_url, headers=headers, json=detail_payload, timeout=API_CONFIG['timeout'])
                    if detail_response.status_code != 200:
                        break

                    detail_data = detail_response.json().get('data') or {}
                    # 一个 packageNo 可能包含多个 waybillNo（跨多页），各自 toCode 也可能不同
                    all_detail_items.extend(detail_data.get('list') or [])

                    total_pages = detail_data.get('pages', 1)
                    current_page = detail_data.get('current', detail_page_num)
                    if current_page >= total_pages:
                        break
                    detail_page_num += 1
                except requests.exceptions.RequestException:
                    break

                time.sleep(SYSTEM_CONFIG['sleep_between_requests'])

            collect_detail_records([{
                'waybillNo': item.get('waybillNo'),
                'targetCenterName': pkg['destinCenterName'],
                'targetSiteId': pkg['destinId'],
                'targetSiteName': pkg['destinName'],
                'postCode': item.get('toCode'),
            } for item in all_detail_items], '已集包')

            time.sleep(SYSTEM_CONFIG['sleep_between_requests'])

        print(f"--- [已集包-{period_label}] {dest_name}: 写入 {len(detail_records) - collected_before} 件 ---")


# stations_special_request 只需要 type=已集包，以下两个明细查询（签入待集包 status=30 /
# 到件未签入 status=121）暂时不需要，整体注释掉，保留代码以备将来需要时恢复
"""
def fetch_checked_in_awaiting_group_detail():
    ""\"签入待集包 status=30：按站点查询明细（含 postCode）""\"
    if not ('auth_token' in globals() and auth_token):
        return

    api_url = f"{API_CONFIG['base_url']}{API_CONFIG['endpoints']['status_details']}"
    headers = HEADERS_CONFIG['special_headers'].copy()
    headers['Authorization'] = auth_token

    for station in stations_special_request:
        dest_name, dest_id = station['name'], station['id']
        page_num = 1
        station_total = 0

        while True:
            payload = {
                "custNos": [],
                "status": QUERY_CONFIG['status_checked_in_awaiting_group'],
                "centerIds": QUERY_CONFIG['center_ids'],
                "timeArr": [],
                "nextIds": [],
                "targetSiteId": dest_id,
                "startTime": today_str,
                "endTime": today_str,
                "pageNum": page_num,
                "pageSize": QUERY_CONFIG['status_page_size']
            }
            try:
                response = requests.post(api_url, headers=headers, json=payload, timeout=API_CONFIG['timeout'])
                if response.status_code != 200:
                    break

                data_dict = response.json().get('data') or {}
                records = data_dict.get('records') or []
                total = data_dict.get('total', 0)
                station_total = total

                collect_detail_records(records, '签入待集包')

                if page_num * QUERY_CONFIG['status_page_size'] >= total:
                    break
                page_num += 1
            except requests.exceptions.RequestException:
                break

            time.sleep(SYSTEM_CONFIG['sleep_between_requests'])

        print(f"--- [签入待集包] {dest_name} (ID: {dest_id}): {station_total} 件 ---")


def fetch_arrival_not_checked_in_detail():
    ""\"到件未签入 status=121：整日全量查询（不按到车单号），本地按站点过滤""\"
    if not ('auth_token' in globals() and auth_token):
        return

    api_url = f"{API_CONFIG['base_url']}{API_CONFIG['endpoints']['status_details']}"
    headers = HEADERS_CONFIG['special_headers'].copy()
    headers['Authorization'] = auth_token

    today_begin_dt = f"{today_str} 00:00:00"
    today_end_dt = f"{today_str} 23:59:59"
    page_size = QUERY_CONFIG['detail_page_size']
    max_pages = 50  # 安全上限：避免 arrivalNo 留空导致的异常分页
    page_num = 1

    while page_num <= max_pages:
        payload = {
            "status": QUERY_CONFIG['status_arrival_not_checked_in'],
            "centerIds": QUERY_CONFIG['center_ids'],
            "startTime": today_str,
            "endTime": today_str,
            "timeArr": [today_begin_dt, today_end_dt],
            "arrivalNo": "",
            "startDateTime": today_begin_dt,
            "endDateTime": today_end_dt,
            "pageNum": page_num,
            "pageSize": page_size
        }
        try:
            response = requests.post(api_url, headers=headers, json=payload, timeout=API_CONFIG['timeout'])
            if response.status_code != 200:
                break

            data_dict = response.json().get('data') or {}
            records = data_dict.get('records') or []
            total = data_dict.get('total', 0)
            collect_detail_records(records, '到件未签入')

            if page_num * page_size >= total:
                break
            page_num += 1
        except requests.exceptions.RequestException:
            break

        time.sleep(SYSTEM_CONFIG['sleep_between_requests'])
    else:
        print(f"⚠️ 已达到分页安全上限 {max_pages} 页，可能仍有数据未取完")

    arrival_counts = {}
    for r in detail_records:
        if r['type'] == '到件未签入':
            arrival_counts[r['targetSiteName']] = arrival_counts.get(r['targetSiteName'], 0) + 1
    for site_name, cnt in arrival_counts.items():
        print(f"--- [到件未签入] {site_name}: {cnt} 件 ---")
"""


def run_special_stations():
    fetch_packed_detail(QUERY_CONFIG['departed_list_today'], today_begin_time_special, today_end_time, '今日')
    # fetch_checked_in_awaiting_group_detail()  # 暂不需要：stations_special_request 只需要 type=已集包
    # fetch_arrival_not_checked_in_detail()     # 暂不需要：stations_special_request 只需要 type=已集包

    # 直接用内存中的 DataFrame 聚合，不落 Excel
    df_detail = pd.DataFrame(
        detail_records,
        columns=['waybillNo', 'targetCenterName', 'targetSiteId', 'targetSiteName', 'postCode', 'type']
    )
    df_detail['targetSiteId'] = pd.to_numeric(df_detail['targetSiteId'], errors='coerce').astype('Int64')
    df_detail['postCode'] = pd.to_numeric(df_detail['postCode'], errors='coerce').astype('Int64')

    # 同一个 waybillNo 可能出现在多个 packageNo 下，按 waybillNo 去重防止重复计数；
    # waybillNo 缺失的行无法判断是否重复，保留不去重
    has_waybill = df_detail['waybillNo'].notna()
    df_detail = pd.concat([
        df_detail[~has_waybill],
        df_detail[has_waybill].drop_duplicates(subset=['waybillNo'])
    ], ignore_index=True)

    print(f"\n==================== 开始为 {len(stations_special_request)} 个邮编明细站点发送飞书卡片 ====================")
    for station in stations_special_request:
        dest_name = station['name']
        dest_id = station['id']
        pickup_time = station['pickup_time']
        platform = station['platform']

        df_packed = df_detail[(df_detail['type'] == '已集包') & (df_detail['targetSiteId'] == dest_id)]
        if df_packed.empty:
            print(f"警告：{dest_name} 没有已集包数据，已跳过。")
            continue

        missing_postcode_count = df_packed['postCode'].isna().sum()
        if missing_postcode_count:
            print(f"⚠️ {dest_name}: {missing_postcode_count} 件已集包包裹缺少有效 postCode，将单独计入 '未知'")

        # 按 destinId 聚合出总数，再按 (destinId, postCode) 聚合出邮编明细
        total_count = len(df_packed)
        postcode_counts = df_packed.groupby('postCode', dropna=False).size().sort_index()

        if dest_name in ROUTE_MAPPING_CONFIG['applies_to']:
            # 该站点有路线号映射表：把邮编换成路线号展示；同一路线号合并计数
            labeled_counts = {}
            for postcode, count in postcode_counts.items():
                if pd.isna(postcode):
                    label = '未知'
                else:
                    label = ROUTE_MAPPING.get(int(postcode), f'Postcode {int(postcode)} has no scope yet')
                labeled_counts[label] = labeled_counts.get(label, 0) + count
            sorted_labels = sorted(labeled_counts.items(), key=lambda kv: route_box_sort_key(kv[0]))
            postcode_counts = pd.Series(dict(sorted_labels))
            section_label = 'By Route Box'
        else:
            postcode_counts.index = postcode_counts.index.map(lambda pc: '未知' if pd.isna(pc) else pc)
            section_label = 'By Postcode'

        payload = {
            "msg_type": FEISHU_CONFIG_POSTCODE['msg_type'],
            "card": {
                "header": {
                    "template": FEISHU_CONFIG_POSTCODE['header_template'],
                    "title": {"tag": "plain_text", "content": f"Volume Forecast {dest_name}"}
                },
                "elements": [
                    {"tag": "div", "text": {"tag": "lark_md", "content": f"**Already Sorted**\n<font color='blue'>{total_count}</font>"}},
                    {"tag": "hr"},
                    {"tag": "div", "text": {"tag": "lark_md", "content": f"**{section_label}**"}},
                    {
                        "tag": "div",
                        "fields": [
                            {"is_short": True, "text": {"tag": "lark_md", "content": f"**{postcode}**\n<font color='blue'>{count}</font>"}}
                            for postcode, count in postcode_counts.items()
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

        send_feishu_card(station, payload, FEISHU_CONFIG_POSTCODE)

    print("==================== 邮编明细站点卡片消息发送任务已完成 ====================")


# =========================================================
# ==   执行入口                                            ==
# =========================================================

run_normal_stations()
run_special_stations()
