"""
货量预报工具配置文件
团队成员共享使用
"""

# ==================== 站点基础数据配置 ====================
stations = [
    {
        "id": 758, 
        "name": "PSW", 
        "pickup_time": "20:30", 
        "platform": "Platform 83",
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/188141ec-d65a-464d-be96-4b6d00343c49",
        "webhook_2": "https://open.feishu.cn/open-apis/bot/v2/hook/188141ec-d65a-464d-be96-4b6d00343c49"
    },

    {
        "id": 768, 
        "name": "WER", 
        "pickup_time": "20:30", 
        "platform": "Platform 79",
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/188141ec-d65a-464d-be96-4b6d00343c49",
        "webhook_2": "https://open.feishu.cn/open-apis/bot/v2/hook/188141ec-d65a-464d-be96-4b6d00343c49"
    },

    {
        "id": 761,
        "name": "C4T",
        "pickup_time": "20:00",
        "platform": "Platform 80",
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/188141ec-d65a-464d-be96-4b6d00343c49",
        "webhoo_2": "https://open.feishu.cn/open-apis/bot/v2/hook/188141ec-d65a-464d-be96-4b6d00343c49"
    }
]

# ==================== API 配置 ====================
API_CONFIG = {
    'base_url': 'https://cps.cirroparcel.nl/prod-api',
    'endpoints': {
        'total_count': '/ops/centerPack/totalCount',
        'status_details': '/dbu_report/common/magic/eu/center/board/status/details'
    },
    'timeout': 20,
    'retry_times': 3
}

# ==================== 查询参数配置 ====================
QUERY_CONFIG = {
    'departed_list_today': ["2", "7", "1", "5", "6"],
    'departed_list_past': ["7", "2"],
    'center_ids': [753], # 中心ID
    'page_size': 50, # 分页大小
    'status_page_size': 10
}

# ==================== 请求头配置 ====================
HEADERS_CONFIG = {
    'common_headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Content-Type': 'application/json;charset=UTF-8'
    },
    'special_headers': {
        'Accept': 'application/json, text/plain, */*',
        'Channel-Id': 'nl',
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
}

# ==================== Token 配置 ====================
TOKEN_CONFIG = {
    'storage_key': 'Admin-Token',
    'prefix': 'Bearer '
}

# ==================== 飞书消息配置 ====================
FEISHU_CONFIG = {
    'msg_type': 'interactive',
    'header_template': 'blue',
    'request_timeout': 10,
    'sleep_between_requests': 1
}

# ==================== 文件输出配置 ====================
OUTPUT_CONFIG = {
    'excel_filename': '最终合并报告.xlsx',
    'sheet_name': '数据汇总'
}

# ==================== 系统配置 ====================
SYSTEM_CONFIG = {
    'sleep_between_requests': 1,
    'wait_for_login': 3,
    'wait_for_token': 3
}
