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
import webbrowser
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

    global stations, stations_special_request, API_CONFIG, QUERY_CONFIG, HEADERS_CONFIG
    global TOKEN_CONFIG, FEISHU_CONFIG, FEISHU_CONFIG_POSTCODE, OUTPUT_CONFIG, SYSTEM_CONFIG

    from config_data_test import (
        stations, stations_special_request, API_CONFIG, QUERY_CONFIG, HEADERS_CONFIG,
        TOKEN_CONFIG, FEISHU_CONFIG, FEISHU_CONFIG_POSTCODE, OUTPUT_CONFIG, SYSTEM_CONFIG
    )
    print("✅ 配置文件加载成功")
    print(f"📊 加载的邮编站点数量: {len(stations_special_request)}")
    for station in stations_special_request[:3]:
        print(f"   - {station['name']} (ID: {station['id']})")
    print(f"📊 加载的普通站点数量: {len(stations)}")
    for station in stations[:3]:
        print(f"   - {station['name']} (ID: {station['id']})")
except ImportError as e:
    print(f"❌ 配置文件加载失败: {e}")

# =======================================================
# ==     明细数据汇总容器（按邮编级别，跨多个查询类型共用）    ==
# =======================================================

detail_records = []
tracked_site_ids = {str(station['id']) for station in stations_special_request}

def _collect_detail_records(records, record_type):
    for record in records:
        if str(record.get('targetSiteId')) not in tracked_site_ids:
            continue
        detail_records.append({
            'waybillNo': record.get('waybillNo'),
            'targetCenterName': record.get('targetCenterName'),
            'targetSiteId': record.get('targetSiteId'),
            'targetSiteName': record.get('targetSiteName'),
            'postCode': record.get('postCode'),
            'type': record_type
        })

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
        print("✅ 成功自动获取到 Token！")
    else:
        # 这个错误处理很重要，如果 Key 存在但值为空
        print(f"错误：在 localStorage 中找到了 Key '{token_key_in_storage}'，但其值为空。可能是登录后写入有延迟。")

except Exception as e:
    print(f"自动获取 Token 失败: {e}")
    print("请确认 Key 的名字是否拼写正确。")

# =======================================================
# ==   两步法获取邮编级明细：selectPageList + detail        ==
# ==   替换原来的 totalCount 聚合查询（今日 / 前六日）        ==
# =======================================================

def _fetch_packed_detail(departed_list, begin_time, end_time, period_label):
    if not ('auth_token' in globals() and auth_token):
        return

    list_api_url = f"{API_CONFIG['base_url']}{API_CONFIG['endpoints']['select_page_list']}"
    detail_api_url = f"{API_CONFIG['base_url']}{API_CONFIG['endpoints']['pack_detail']}"

    headers = HEADERS_CONFIG['special_headers'].copy()
    headers['Authorization'] = auth_token

    for station in stations_special_request:
        dest_name = station['name']
        dest_id = station['id']
        print(f"--- [已集包-{period_label}] 站点: {dest_name} (ID: {dest_id}) ---")

        # --- 第一步：按站点查询 selectPageList，汇总成该站点的 DataFrame（不预先过滤） ---
        station_records = []
        page_num = 1
        requested_page_size = QUERY_CONFIG['page_size']

        while True:
            payload = {
                "pageNum": page_num,
                "pageSize": requested_page_size,
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

                response_json = response.json()
                data_dict = response_json.get('data') or {}
                # 注意：selectPageList 返回的是 'list' 字段，不是 'records'；
                # 分页依据服务端返回的 'pages'/'current'，而非我们请求的 pageSize（服务端会自行限制，如固定为 20）
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
                        'sortFlagName': record.get('sortFlagName'),
                    })

                if current_page >= total_pages:
                    break
                page_num += 1
            except requests.exceptions.RequestException:
                break

            time.sleep(SYSTEM_CONFIG['sleep_between_requests'])

        df_select_page_list = pd.DataFrame(station_records)
        print(f"    selectPageList 共 {len(df_select_page_list)} 件包裹")

        if df_select_page_list.empty:
            continue

        # --- 第二步：从该站点的 DataFrame 中筛出 sortFlag == 'N'，逐个查 detail，取 waybillNo/toCode ---
        pending_packages = df_select_page_list[df_select_page_list['sortFlag'] == 'N']
        print(f"    其中 sortFlag=N（已集包待查明细）共 {len(pending_packages)} 个箱袋号，开始查询 detail...")
        collected_before = len(detail_records)

        for _, pkg in pending_packages.iterrows():
            detail_payload = {
                "pageNum": 1,
                "pageSize": 10,
                "packageNo": pkg['packageNo']
            }

            try:
                detail_response = requests.post(detail_api_url, headers=headers, json=detail_payload, timeout=API_CONFIG['timeout'])

                if detail_response.status_code != 200:
                    continue

                detail_json = detail_response.json()
                detail_data = detail_json.get('data') or {}
                # 一个 packageNo 可能包含多个 waybillNo，各自的 toCode 也可能不同；
                # 响应字段是 'list'，不是 'records'（与 selectPageList 一样）
                detail_list = detail_data.get('list') or []

                _collect_detail_records([{
                    'waybillNo': item.get('waybillNo'),
                    'targetCenterName': pkg['destinCenterName'],
                    'targetSiteId': pkg['destinId'],
                    'targetSiteName': pkg['destinName'],
                    'postCode': item.get('toCode'),
                } for item in detail_list], '已集包')

            except requests.exceptions.RequestException:
                pass

            time.sleep(SYSTEM_CONFIG['sleep_between_requests'])

        print(f"    已集包 detail 查询完成，成功写入 {len(detail_records) - collected_before} 件")


_fetch_packed_detail(QUERY_CONFIG['departed_list_today'], today_begin_time, today_end_time, '今日')
_fetch_packed_detail(QUERY_CONFIG['departed_list_past'], past_period_begin_time, past_period_end_time, '前六日')

# =======================================================
# ==     明细查询（含邮编），汇总进同一个 DataFrame    ==
# =======================================================

# --- 签入待集包 status=30（按站点查询）---
if 'auth_token' in locals() and auth_token:
    api_url = f"{API_CONFIG['base_url']}{API_CONFIG['endpoints']['status_details']}"

    headers = HEADERS_CONFIG['special_headers'].copy()
    headers['Authorization'] = auth_token

    today_str = datetime.date.today().strftime('%Y-%m-%d')

    for station in stations_special_request:
        dest_name = station['name']
        dest_id = station['id']

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

                if response.status_code == 200:
                    response_json = response.json()
                    data_dict = response_json.get('data') or {}
                    records = data_dict.get('records') or []
                    total = data_dict.get('total', 0)
                    station_total = total

                    _collect_detail_records(records, '签入待集包')

                    if page_num * QUERY_CONFIG['status_page_size'] >= total:
                        break
                    page_num += 1
                else:
                    break
            except requests.exceptions.RequestException:
                break

            time.sleep(SYSTEM_CONFIG['sleep_between_requests'])

        print(f"--- [签入待集包] 站点: {dest_name} (ID: {dest_id}): {station_total} 件包裹 ---")

else:
    pass

# --- 到件未签入 status=121（不指定到车单号，尝试整日全量拉取，本地按站点过滤）---
if 'auth_token' in locals() and auth_token:
    api_url = f"{API_CONFIG['base_url']}{API_CONFIG['endpoints']['status_details']}"

    headers = HEADERS_CONFIG['special_headers'].copy()
    headers['Authorization'] = auth_token

    today_str = datetime.date.today().strftime('%Y-%m-%d')
    today_begin_dt = f"{today_str} 00:00:00"
    today_end_dt = f"{today_str} 23:59:59"

    page_size = QUERY_CONFIG['detail_page_size']
    max_pages = 50  # 安全上限：若 arrivalNo 实际必填导致返回异常/超量数据，避免无限翻页
    page_num = 1
    print("--- [到件未签入] 开始整日全量查询 ---")

    while page_num <= max_pages:
        payload = {
            "status": QUERY_CONFIG['status_arrival_not_checked_in'],
            "centerIds": QUERY_CONFIG['center_ids'],
            "startTime": today_str,
            "endTime": today_str,
            "timeArr": [today_begin_dt, today_end_dt],
            "arrivalNo": "",  # 留空尝试获取整日全部到件，而非单个到车单号；若接口报错说明此字段必填
            "startDateTime": today_begin_dt,
            "endDateTime": today_end_dt,
            "pageNum": page_num,
            "pageSize": page_size
        }

        try:
            response = requests.post(api_url, headers=headers, json=payload, timeout=API_CONFIG['timeout'])

            if response.status_code == 200:
                response_json = response.json()
                data_dict = response_json.get('data') or {}
                records = data_dict.get('records') or []
                total = data_dict.get('total', 0)

                _collect_detail_records(records, '到件未签入')
                # print(f"    第{page_num}页，累计 total={total}")

                if page_num * page_size >= total:
                    break
                page_num += 1
            else:
                break
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
        print(f"    到件未签入 - {site_name}: {cnt} 件包裹")

else:
    pass

# =======================================================
# ==                   写入 Excel                       ==
# =======================================================

df_detail = pd.DataFrame(
    detail_records,
    columns=['waybillNo', 'targetCenterName', 'targetSiteId', 'targetSiteName', 'postCode', 'type']
)
df_detail['targetSiteId'] = pd.to_numeric(df_detail['targetSiteId'], errors='coerce').astype('Int64')
df_detail['postCode'] = pd.to_numeric(df_detail['postCode'], errors='coerce').astype('Int64')

script_dir = os.path.dirname(os.path.abspath(__file__))
today_str = datetime.date.today().strftime('%Y-%m-%d')

for station in stations_special_request:
    station_name = station['name']
    df_station = df_detail[df_detail['targetSiteId'] == station['id']]

    if df_station.empty:
        continue

    output_filename = f"{today_str}_{station_name}.xlsx"
    full_output_path = os.path.join(script_dir, output_filename)
    try:
        df_station.to_excel(full_output_path, index=False, sheet_name=OUTPUT_CONFIG['sheet_name'])
        print(f"✅ 已写入 Excel: {full_output_path}（{len(df_station)} 行）")
    except Exception as e:
        print(f"❌ 写入 Excel 失败: {full_output_path}, 错误: {e}")
        continue

# =======================================================
# ==     构建邮编卡片消息（已集包，按 postCode 聚合）           ==
# ==     暂不实际发送，改为生成本地 HTML 预览并自动打开          ==
# =======================================================

def _build_card_html(dest_name, postcode_counts, pickup_time, platform, updated_str):
    tiles_html = "".join(
        f"""<div class="tile"><div class="pc">{postcode}</div><div class="cnt">{count}</div></div>"""
        for postcode, count in postcode_counts.items()
    )
    return f"""<!doctype html>
<html><head><meta charset="utf-8"><title>Volume Forecast {dest_name}</title>
<style>
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0; min-height: 100vh; background: #EEF1F4;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
    display: flex; justify-content: center; padding: 48px 20px;
  }}
  .card {{
    width: 100%; max-width: 360px; border-radius: 10px; overflow: hidden;
    background: #FFFFFF; box-shadow: 0 1px 2px rgba(0,0,0,0.06), 0 2px 10px rgba(0,0,0,0.05);
  }}
  .card-header {{
    background: linear-gradient(135deg, #3370FF, #245BDB);
    padding: 12px 16px; color: #fff; font-size: 15px; font-weight: 600;
  }}
  .card-body {{ padding: 16px; }}
  .section-label {{ font-size: 13px; font-weight: 700; color: #1F2329; margin: 0 0 10px; }}
  .postcode-grid {{
    display: grid; grid-template-columns: repeat(auto-fill, minmax(96px, 1fr));
    gap: 8px; margin-bottom: 4px;
  }}
  .tile {{ background: #F2F3F5; border: 1px solid #E5E6EB; border-radius: 8px; padding: 9px 10px; }}
  .tile .pc {{ font-size: 12.5px; font-weight: 700; color: #1F2329; margin-bottom: 3px; }}
  .tile .cnt {{ font-size: 15px; font-weight: 700; color: #3370FF; font-variant-numeric: tabular-nums; }}
  .divider {{ height: 1px; background: #E5E6EB; margin: 14px 0; border: none; }}
  .field-pair {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }}
  .field-pair .field .k {{ font-size: 12.5px; font-weight: 700; color: #1F2329; margin-bottom: 3px; }}
  .field-pair .field .v {{ font-size: 13.5px; color: #1F2329; }}
  .card-note {{ padding: 10px 16px 13px; font-size: 11.5px; color: #8F959E; }}
</style></head>
<body>
  <div class="card">
    <div class="card-header">Volume Forecast {dest_name}</div>
    <div class="card-body">
      <p class="section-label">Already Sorted</p>
      <div class="postcode-grid">{tiles_html}</div>
      <hr class="divider" />
      <div class="field-pair">
        <div class="field"><div class="k">Pick up time</div><div class="v">{pickup_time}</div></div>
        <div class="field"><div class="k">Dock</div><div class="v">{platform}</div></div>
      </div>
    </div>
    <hr class="divider" style="margin: 0 16px;" />
    <div class="card-note">updated: {updated_str}</div>
  </div>
</body></html>"""


for station in stations_special_request:
    dest_name = station['name']
    dest_id = station['id']
    pickup_time = station['pickup_time']
    platform = station['platform']

    df_packed = df_detail[(df_detail['type'] == '已集包') & (df_detail['targetSiteId'] == dest_id)]

    if df_packed.empty:
        continue

    missing_postcode_count = df_packed['postCode'].isna().sum()
    if missing_postcode_count:
        print(f"⚠️ {dest_name}: {missing_postcode_count} 件已集包包裹缺少有效 postCode，将单独计入 '未知'")

    postcode_counts = df_packed.groupby('postCode', dropna=False).size().sort_index()
    postcode_counts.index = postcode_counts.index.map(lambda pc: '未知' if pd.isna(pc) else pc)

    payload = {
        "msg_type": FEISHU_CONFIG_POSTCODE['msg_type'],
        "card": {
            "header": {
                "template": FEISHU_CONFIG_POSTCODE['header_template'],
                "title": {
                    "tag": "plain_text",
                    "content": f"Volume Forecast {dest_name}"
                }
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {"tag": "lark_md", "content": "**Already Sorted**"}
                },
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

    updated_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    card_html = _build_card_html(dest_name, postcode_counts, pickup_time, platform, updated_str)
    card_html_path = os.path.join(script_dir, f"{today_str}_{dest_name}_card_preview.html")
    try:
        with open(card_html_path, 'w', encoding='utf-8') as f:
            f.write(card_html)
        print(f"🖼️  已生成卡片预览: {card_html_path}（未发送）")
        webbrowser.open(f"file://{card_html_path}")
    except Exception as e:
        print(f"❌ 卡片预览生成失败: {dest_name}, 错误: {e}")
        continue

# =======================================================
# ==     普通站点：沿用 app.py 聚合查询流程（今日/前六日/待签入/待集包） ==
# =======================================================

df_today = pd.DataFrame(columns=['destinId', '目的地名称', '今日已生产'])
df_past_6_days = pd.DataFrame(columns=['destinId', '目的地名称', '前六日库存'])
df_wait_collect = pd.DataFrame(columns=['destinId', '目的地名称', '到件待签入'])
df_status_2 = pd.DataFrame(columns=['destinId', '目的地名称', '签入待集包'])

if 'auth_token' in locals() and auth_token:
    api_url = f"{API_CONFIG['base_url']}{API_CONFIG['endpoints']['total_count']}"
    headers = HEADERS_CONFIG['common_headers'].copy()
    headers['Authorization'] = auth_token

    results_today = []
    for station in stations:
        dest_name = station['name']
        dest_id = station['id']

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
            response = requests.post(api_url, headers=headers, json=payload, verify=False, timeout=API_CONFIG['timeout'])

            if response.status_code == 200:
                total_count = response.json().get('data', {}).get('totalCount', 0)
                results_today.append({'destinId': dest_id, '目的地名称': dest_name, '今日已生产': total_count})
            else:
                results_today.append({'destinId': dest_id, '目的地名称': dest_name, '今日已生产': '查询失败'})
        except requests.exceptions.RequestException:
            results_today.append({'destinId': dest_id, '目的地名称': dest_name, '今日已生产': '请求异常'})

        time.sleep(SYSTEM_CONFIG['sleep_between_requests'])

    df_today = pd.DataFrame(results_today)
    print(f"--- [今日已生产] 完成，共 {len(df_today)} 个站点 ---")

    results_past_6_days = []
    for station in stations:
        dest_name = station['name']
        dest_id = station['id']

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
            response = requests.post(api_url, headers=headers, json=payload, verify=False, timeout=API_CONFIG['timeout'])

            if response.status_code == 200:
                total_count = response.json().get('data', {}).get('totalCount', 0)
                results_past_6_days.append({'destinId': dest_id, '目的地名称': dest_name, '前六日库存': total_count})
            else:
                results_past_6_days.append({'destinId': dest_id, '目的地名称': dest_name, '前六日库存': '查询失败'})
        except requests.exceptions.RequestException:
            results_past_6_days.append({'destinId': dest_id, '目的地名称': dest_name, '前六日库存': '请求异常'})

        time.sleep(SYSTEM_CONFIG['sleep_between_requests'])

    df_past_6_days = pd.DataFrame(results_past_6_days)
    print(f"--- [前六日库存] 完成，共 {len(df_past_6_days)} 个站点 ---")

    # --- 到件待签入 status=1（聚合） ---
    status_api_url = f"{API_CONFIG['base_url']}{API_CONFIG['endpoints']['status_details']}"
    status_headers = HEADERS_CONFIG['special_headers'].copy()
    status_headers['Authorization'] = auth_token
    today_str = datetime.date.today().strftime('%Y-%m-%d')

    results_wait_collect = []
    for station in stations:
        dest_name = station['name']
        dest_id = station['id']

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
            response = requests.post(status_api_url, headers=status_headers, json=payload, timeout=API_CONFIG['timeout'])

            if response.status_code == 200:
                data_dict = response.json().get('data')
                records = data_dict.get('records') if data_dict else None
                wait_count = records[0].get('waitCheckInWaybillCnt', 0) if records else 0
                results_wait_collect.append({'destinId': dest_id, '目的地名称': dest_name, '到件待签入': wait_count})
            else:
                results_wait_collect.append({'destinId': dest_id, '目的地名称': dest_name, '到件待签入': '查询失败'})
        except requests.exceptions.RequestException:
            results_wait_collect.append({'destinId': dest_id, '目的地名称': dest_name, '到件待签入': '请求异常'})

        time.sleep(SYSTEM_CONFIG['sleep_between_requests'])

    df_wait_collect = pd.DataFrame(results_wait_collect)
    print(f"--- [到件待签入] 完成，共 {len(df_wait_collect)} 个站点 ---")

    # --- 签入待集包 status=2（聚合） ---
    results_status_2 = []
    for station in stations:
        dest_name = station['name']
        dest_id = station['id']

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
            response = requests.post(status_api_url, headers=status_headers, json=payload, timeout=API_CONFIG['timeout'])

            if response.status_code == 200:
                data_dict = response.json().get('data')
                records = data_dict.get('records') if data_dict else None
                wait_count = records[0].get('waitCollectAndGroupCnt', 0) if records else 0
                results_status_2.append({'destinId': dest_id, '目的地名称': dest_name, '签入待集包': wait_count})
            else:
                results_status_2.append({'destinId': dest_id, '目的地名称': dest_name, '签入待集包': '查询失败'})
        except requests.exceptions.RequestException:
            results_status_2.append({'destinId': dest_id, '目的地名称': dest_name, '签入待集包': '请求异常'})

        time.sleep(SYSTEM_CONFIG['sleep_between_requests'])

    df_status_2 = pd.DataFrame(results_status_2)
    print(f"--- [签入待集包] 完成，共 {len(df_status_2)} 个站点 ---")

else:
    pass

# --- 数据合并 ---
df_merge = pd.merge(df_today, df_past_6_days, on=['destinId', '目的地名称'], how='outer')
df_merge = pd.merge(df_merge, df_wait_collect, on=['destinId', '目的地名称'], how='outer')
df_merge = pd.merge(df_merge, df_status_2, on=['destinId', '目的地名称'], how='outer')
df_merge['当前货量'] = df_merge['今日已生产'] + df_merge['前六日库存'] + df_merge['签入待集包']
df_merge['货量预估'] = df_merge['当前货量'] + df_merge['到件待签入']

# =======================================================
# ==     构建普通站点卡片消息（原有格式），生成 HTML 预览并打开   ==
# ==     暂不实际发送                                     ==
# =======================================================

def _build_summary_card_html(dest_name, today_count, total_count, pickup_time, platform, updated_str):
    return f"""<!doctype html>
<html><head><meta charset="utf-8"><title>Volume Forecast {dest_name}</title>
<style>
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0; min-height: 100vh; background: #EEF1F4;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
    display: flex; justify-content: center; padding: 48px 20px;
  }}
  .card {{
    width: 100%; max-width: 360px; border-radius: 10px; overflow: hidden;
    background: #FFFFFF; box-shadow: 0 1px 2px rgba(0,0,0,0.06), 0 2px 10px rgba(0,0,0,0.05);
  }}
  .card-header {{
    background: linear-gradient(135deg, #3370FF, #245BDB);
    padding: 12px 16px; color: #fff; font-size: 15px; font-weight: 600;
  }}
  .card-body {{ padding: 16px; }}
  .field-pair {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }}
  .field-pair .field .k {{ font-size: 12.5px; font-weight: 700; color: #1F2329; margin-bottom: 3px; }}
  .field-pair .field .v {{ font-size: 15px; font-weight: 700; font-variant-numeric: tabular-nums; }}
  .field-pair .field .v.blue {{ color: #3370FF; }}
  .field-pair .field .v.green {{ color: #2BA471; }}
  .field-pair .field .v.plain {{ color: #1F2329; font-weight: 500; font-size: 13.5px; }}
  .divider {{ height: 1px; background: #E5E6EB; margin: 14px 0; border: none; }}
  .card-note {{ padding: 10px 16px 13px; font-size: 11.5px; color: #8F959E; }}
</style></head>
<body>
  <div class="card">
    <div class="card-header">Volume Forecast {dest_name}</div>
    <div class="card-body">
      <div class="field-pair">
        <div class="field"><div class="k">Already Sorted</div><div class="v blue">{today_count}</div></div>
        <div class="field"><div class="k">Estimated Total Number</div><div class="v green">{total_count}</div></div>
      </div>
      <hr class="divider" />
      <div class="field-pair">
        <div class="field"><div class="k">Pick up time</div><div class="v plain">{pickup_time}</div></div>
        <div class="field"><div class="k">Dock</div><div class="v plain">{platform}</div></div>
      </div>
    </div>
    <hr class="divider" style="margin: 0 16px;" />
    <div class="card-note">updated: {updated_str}</div>
  </div>
</body></html>"""


for station in stations:
    dest_name = station['name']
    pickup_time = station['pickup_time']
    platform = station['platform']

    station_data = df_merge[df_merge['目的地名称'] == dest_name]

    if station_data.empty:
        print(f"警告：未在数据中找到 '{dest_name}' 的信息，已跳过。")
        continue

    row = station_data.iloc[0]
    today_count = row['当前货量']
    total_count = row['货量预估']

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

    updated_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    summary_card_html = _build_summary_card_html(dest_name, today_count, total_count, pickup_time, platform, updated_str)
    summary_card_path = os.path.join(script_dir, f"{today_str}_{dest_name}_card_preview.html")
    try:
        with open(summary_card_path, 'w', encoding='utf-8') as f:
            f.write(summary_card_html)
        print(f"🖼️  已生成卡片预览: {summary_card_path}（未发送）")
        webbrowser.open(f"file://{summary_card_path}")
    except Exception as e:
        print(f"❌ 卡片预览生成失败: {dest_name}, 错误: {e}")
        continue
