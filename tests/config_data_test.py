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
    },
    {
        "id": 1329,
        "name": "GAL",
        "pickup_time": "***",
        "platform": "Platform ***",
        # "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/866f6dd5-a8aa-4454-bf99-207b11d382f9"
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

# ==================== 邮编 -> 路线号 映射配置 ====================
# 目前只有 ACT 有路线号映射表；其余邮编明细站点（如 GAL、MEK）继续展示原始邮编
ROUTE_MAPPING_DATA = [
    ('1', 3731),
    ('2', 3732),
    ('3', 3704),
    ('4', 3703),
    ('5', 3708),
    ('6', 3709),
    ('9', 3984),
    ('10', 3985),
    ('13', 3945),
    ('14', 3962),
    ('15', 3961),
    ('16', 4101),
    ('17', 4102),
    ('18', 4103),
    ('19', 4104),
    ('20+28', 4106),
    ('23', 4107),
    ('24', 4145),
    ('25', 4122),
    ('26', 4121),
    ('30', 3989),
    ('31', 3999),
    ('35', 3994),
    ('36', 3993),
    ('40', 3992),
    ('41', 3439),
    ('42', 3438),
    ('43', 3437),
    ('44', 3431),
    ('45', 3432),
    ('46', 3435),
    ('47', 3436),
    ('48', 3402),
    ('53', 3404),
    ('56', 3433),
    ('57', 4125),
    ('58', 4124),
    ('59', 4131),
    ('63', 4126),
    ('66', 4233),
    ('67', 4235),
    ('70', 4245),
    ('73', 4143),
    ('74', 4141),
    ('75', 4147),
    ('11', 3997),
    ('21+22+27', 4105),
    ('12+29+32', 3998),
    ('33+38+39', 3991),
    ('34+37', 3995),
    ('49+52+54', 3401),
    ('50+51', 3403),
    ('55+60', 4132),
    ('61+62', 4133),
    ('64+65', 4128),
    ('68+69', 4231),
    ('7+8', 3981),
    ('71+72', 4142),
]

ROUTE_MAPPING_CONFIG = {
    'applies_to': ['ACT'],
}

# ==================== 系统配置 ====================
SYSTEM_CONFIG = {
    'sleep_between_requests': 1,
    'wait_for_login': 3,
    'wait_for_token': 3
}
