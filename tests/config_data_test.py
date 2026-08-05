"""
货量预报工具配置文件
团队成员共享使用
"""

# ==================== 站点基础数据配置 ====================
stations_special_request = [

    {
        "id": 1092,
        "name": "ACT",
        "pickup_time": "***",
        "platform": "***",
        # "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/188141ec-d65a-464d-be96-4b6d00343c49",
    }
]
stations = [
    {
            "id": 1504,
            "name": "E55",
            "pickup_time": "***",
            "platform": "***",
            # "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/3393630e-f025-4cfd-89a4-48850b1a39e3"
    }
]

# ==================== API 配置 ====================
API_CONFIG = {
    'base_url': 'https://cps.cirroparcel.nl/prod-api',
    'endpoints': {
        'total_count': '/ops/centerPack/totalCount',
        'status_details': '/dbu_report/common/magic/eu/center/board/status/details',
        'select_page_list': '/ops/centerPack/selectPageList',
        'pack_detail': '/ops/centerPack/detail'
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
    'status_page_size': 10,
    'status_checked_in_awaiting_group': 30, # 签入待集包（按站点查明细，含 postCode）
    'status_arrival_not_checked_in': 121, # 到件未签入（整日查询，不按到车单号，含 postCode）
    'detail_page_size': 500, # 明细查询分页大小（用于整日全量拉取，减少请求次数）
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
FEISHU_CONFIG_POSTCODE = {
    'msg_type': 'interactive',
    'header_template': 'blue',
    'request_timeout': 10,
    'sleep_between_requests': 1
}

# 普通站点沿用 app.py 原有的卡片格式（Already Sorted 总数 + Estimated Total Number）
FEISHU_CONFIG = {
    'msg_type': 'interactive',
    'header_template': 'blue',
    'request_timeout': 10,
    'sleep_between_requests': 1
}

# ==================== 文件输出配置 ====================
OUTPUT_CONFIG = {
    'sheet_name': '数据汇总'
}

# ==================== 系统配置 ====================
SYSTEM_CONFIG = {
    'sleep_between_requests': 1,
    'wait_for_login': 3,
    'wait_for_token': 3
}
