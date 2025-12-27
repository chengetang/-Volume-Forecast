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
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/bd1776d2-bf7f-4bbe-8bd3-e44eca8c3a4f"
    },
  
    {
        "id": 761,
        "name": "C4T",
        "pickup_time": "19:30",
        "platform": "Platform 85",
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/a5d67e93-0000-40a5-bfc8-dafdd5aeac32"
    },

    {
        "id": 768, 
        "name": "WER", 
        "pickup_time": "20:30", 
        "platform": "Platform 83",
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/a8e2666b-d0dd-419b-b706-a65742a2bd69",
        "webhook_2": "https://open.feishu.cn/open-apis/bot/v2/hook/120e1bf5-7050-4e57-93c3-b7f640c42992"
    },

    {
        "id": 878,
        "name": "ANA",
        "pickup_time": "21:00",
        "platform": "Platform A05",
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/37c5a6ee-5a8c-4de5-8964-798649fc364a"
    },
  
    {
        "id": 879,
        "name": "MEK",
        "pickup_time": "19:00",
        "platform": "Platform 34",
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/1be920d5-3e51-4495-a6ee-46e0cafd8c94"
    },

    {
         "id": 899,
         "name": "JHD",
         "pickup_time": "20:00",
         "platform": "Platform 34",
         "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/78499cfe-42ce-414a-815c-5feeaaf675cb"
    },
    
    {
        "id": 0, 
        # "id": 948,
        "name": "INB",
        "pickup_time": "19:00",
        "platform": "Platform 84",
        # "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/188141ec-d65a-464d-be96-4b6d00343c49" # 测试
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/9eb00e37-5c08-4b3e-a8d9-d41adc21ae25"
    },

    {
        "id": 1002,
        "name": "RIN",
        "pickup_time": "20:00",
        "platform": "Platform 85",
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/8af7ddf9-6af5-43bc-84f7-566baebea047"
    },
    {
        "id": 1092,
        "name": "ACT",
        "pickup_time": "21:00",
        "platform": "Platform 86",
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/8794cb6b-5734-420e-8684-c0eb9749f598"
    },
    {
        "id": 1124,
        "name": "RSR",
        "pickup_time": "19:45",
        "platform": "Platform 33",
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/0097d1c3-36c9-4880-afbc-af6d5abe9275"
    },
    {
        "id": 1158,
        "name": "SAM",
        "pickup_time": "21:00",
        "platform": "Platform ***",
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/09b83a29-433f-49f3-8635-e3a0a18a3077"
    },
    {
        "id": 1193,
        "name": "OMT",
        "pickup_time": "19:00",
        "platform": "Platform 85",
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/058b48dc-6979-4d3c-ab4f-f089a1fa1c60"
    },
    {
        "id": 1229,
        "name": "RSL",
        "pickup_time": "19:45",
        "platform": "Platform 87",
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/28f3b5e2-a316-4a84-b994-2e091093cc03"
    },
    {
        "id": 1266,
        "name": "DET",
        "pickup_time": "19:00",
        "platform": "Platform 87",
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/c0da2b16-b8e8-4316-8292-08f13ea25715"
    },
    {
        "id": 1326,
        "name": "AAT",
        "pickup_time": "21:00",
        "platform": "Platform ***",
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/a760722a-e32c-49cb-b4b4-bbfac737518f"
    },
    {
        "id": 1327,
        "name": "SAS",
        "pickup_time": "21:00",
        "platform": "Platform ***",
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/b8c2177e-a17f-42d2-b175-ac24ed71340d"
    },
    {
        "id": 1329,
        "name": "GAL",
        "pickup_time": "19:00",
        "platform": "Platform 32",
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/866f6dd5-a8aa-4454-bf99-207b11d382f9"
    },
    {
        "id": 1330,
        "name": "CEK",
        "pickup_time": "19:45",
        "platform": "Platform 30",
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/c42978a2-826b-4974-9162-cac3e2ed572b"
    },
    {
        "id": 1332,
        "name": "RKM",
        "pickup_time": "19:00",
        "platform": "Platform 82",
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/25eaa0c5-90ac-4028-82bd-9803c63631f3"
    },
    {
        "id": 1334,
        "name": "AAA",
        "pickup_time": "21:00",
        "platform": "Platform A02",
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/160b24c1-1cb3-4e5f-814b-d8d244f8f978"
    },
    {
        "id": 1339,
        "name": "TSI",
        "pickup_time": "19:00",
        "platform": "Platform 27",
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/a4841ae0-5e7b-46fc-a8a5-357fe5c50630"
    },
    {
        "id": 1340,
        "name": "BTY",
        "pickup_time": "21:00",
        "platform": "Platform 9",
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/35e9f4e0-d27c-4681-9087-4c2097e97c7d"
    },
    {
        "id": 1341,
        "name": "SFT",
        "pickup_time": "21:00",
        "platform": "Platform A04",
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/0d08292a-af0e-4bf6-8724-4542b626ae46"
    },
    {
        "id": 1342,
        "name": "FPS",
        "pickup_time": "19:45",
        "platform": "Platform 33",
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/16bd74ca-b880-487c-be21-65dc83b42a4f"
    },
    {
        "id": 1345,
        "name": "BEN",
        "pickup_time": "21:00",
        "platform": "Platform 29",
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/d3cde48e-7720-4fec-b65e-8eba33e0dbae"
    },
    {
        "id": 1346,
        "name": "BMB",
        "pickup_time": "20:00",
        "platform": "Platform 91",
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/51abaae6-88c7-4fc5-bddc-92c5c010344a"
    },
    {
        "id": 1350,
        "name": "YKY",
        "pickup_time": "19:45",
        "platform": "Platform 29",
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/04db8bca-2e2c-4fe9-8c59-1cbf77fa5d42"
    },
    {
        "id": 1351,
        "name": "G6T",
        "pickup_time": "20:30",
        "platform": "Platform 30",
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/fe7a2762-e23a-48e8-9194-02904871270a"
    },
    
    {
        "id": 0,
        # "id": 1354,
        "name": "B88",
        "pickup_time": "21:00",
        "platform": "Platform 5",
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/a605f6fa-1eff-419a-8e4b-0f954bad96e4"
        # "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/188141ec-d65a-464d-be96-4b6d00343c49" #测试
    },
    
    {
        "id": 1355,
        "name": "XXX",
        "pickup_time": "21:00",
        "platform": "Platform 89",
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/615b8908-2e12-4bb1-933c-0a5837ec607b"
    },
    # {
    #     "id": 1356,
    #     "name": "E1L",
    #     "pickup_time": "10:00",
    #     "platform": "Platform 34",
    #     "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/615b8908-2e12-4bb1-933c-0a5837ec607b",
    # },
    {
        "id": 1357,
        "name": "T7Q",
        "pickup_time": "20:00",
        "platform": "Platform 31",
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/c8fce7f9-d01c-46f0-9fd7-330710f9bc7d"
    },
    {
        "id": 1358,
        "name": "VT2",
        "pickup_time": "21:00",
        "platform": "Platform 27",
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/107f5940-4abc-4b7f-8838-03d0c8eef77f"
    },
    {
        "id": 1359,
        "name": "AFM",
        "pickup_time": "19:00",
        "platform": "Platform 83",
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/f9224be2-e834-41f4-8373-7e6cb561226a"
    },
    {
        "id": 1366,
        "name": "TR6",
        "pickup_time": "20:00",
        "platform": "Platform 32",
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/a95e75de-b77c-4278-a178-80211c4d33a6"
    },
    {
        "id": 1364,
        "name": "BAL",
        "pickup_time": "21:00",
        "platform": "Platform 10",
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/7db751cf-75b7-4753-a920-cb90cf6cd212"
    },
    {
        "id": 1371,
        "name": "KT1",
        "pickup_time": "21:00",
        "platform": "Platform 84",
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/5ad729cb-c477-4360-b5f7-b7e295e0079f"
    },
    {
        "id": 1368,
        "name": "DIA",
        "pickup_time": "21:00",
        "platform": "Platform 7",
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/dcb0f50d-72a0-4735-a8c2-f4b4872748bb"
    },
    {
        "id": 1370,
        "name": "BFF",
        "pickup_time": "21:00",
        "platform": "Platform 8",
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/22aa8100-c1ac-47e5-8f23-548ccea9916d"
    },
    {
        "id": 1384,
        "name": "TEE",
        "pickup_time": "21:00",
        "platform": "Platform ***",
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/55591948-7fc4-465f-9144-9a83951ebbc0"
    },
    {
        "id": 1372,
        "name": "SWC",
        "pickup_time": "21:00",
        "platform": "Platform ***",
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/857ddb47-24cd-4d49-a089-c2cc61d12e79"
    },
    {
        "id": 1383,
        "name": "LEY",
        "pickup_time": "21:00",
        "platform": "Platform ***",
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/daeb8c2a-1615-4fef-b67a-50211a1ac1c8"
    },
    {
        "id": 1385,
        "name": "VXO",
        "pickup_time": "21:00",
        "platform": "Platform ***",
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/2cfc9785-62ac-4596-872a-f08693a212a9"
    },
    {
        "id": 1380,
        "name": "LOG",
        "pickup_time": "21:00",
        "platform": "Platform ***",
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/9c721c83-fe57-4eec-b83d-2d8f49cf1ad0"
    },
    {
        "id": 1347,
        "name": "HA6",
        "pickup_time": "21:00",
        "platform": "Platform ***",
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/dc4561ce-9d55-4fbc-8c17-f147263ebb4d"
    },
    {
        "id": 1381,
        "name": "POK",
        "pickup_time": "21:00",
        "platform": "Platform ***",
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/755341c2-4b92-44c3-bccb-844fb2716eb1"
    },
    {
        "id": 1375,
        "name": "C5S",
        "pickup_time": "21:00",
        "platform": "Platform ***",
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/827b5779-5607-4f0d-aee2-67d9e92b0d33"
    },
    {
        "id": 1376,
        "name": "BMW",
        "pickup_time": "20:00",
        "platform": "Platform 90",
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/47e0010c-e016-4c61-9cc5-66919a2649de"
    },
    {
        "id": 1377,
        "name": "TOP",
        "pickup_time": "20:00",
        "platform": "Platform 30",
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/26af2598-035f-4327-95fa-32c8f428adab"
    },
    {
        "id": 1378,
        "name": "MOF",
        "pickup_time": "20:30",
        "platform": "Platform 76",
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/d7febf15-1965-4ac5-9117-87643a7c5571"
    },
    {
        "id": 1386,
        "name": "LAK",
        "pickup_time": "21:00",
        "platform": "Platform 87",
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/da3b7177-6c4e-487f-8469-1b977ed6ef3f"
    },
    # {
    #     "id": 1387,
    #     "name": "NGT",
    #     "pickup_time": "20:00",
    #     "platform": "Platform 88",
    #     "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/a5cf4557-53d1-45d4-a57e-d65673a24d54"
    # },
    # {
    #     "id": 1388,
    #     "name": "MAN",
    #     "pickup_time": "21:00",
    #     "platform": "Platform ***",
    #     "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/ede70a5a-1baf-4f24-ad1e-417551df3a62"
    # },
    {
        "id": 1389,
        "name": "PMS",
        "pickup_time": "21:00",
        "platform": "Platform A02",
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/31bdf103-7ec9-4429-a27a-c709fef64c05"
    },
    {
        "id": 1390,
        "name": "37A",
        "pickup_time": "21:00",
        "platform": "Platform ***",
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/5fc3dd02-e166-4514-bd99-1f41c5ddc588"     
    },
    {
        "id": 1391,
        "name": "JUM",
        "pickup_time": "21:00",
        "platform": "Platform ***",
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/23e6507f-1f4d-448b-8631-bad6776716c1"     
    },
    {
        "id": 1413,
        "name": "T4U",
        "pickup_time": "20:00",
        "platform": "Platform 31",
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/5ff782cd-a708-4cee-af64-5f963fea4f53"     
    },
    {
        "id": 1418,
        "name": "PRE",
        "pickup_time": "19:00",
        "platform": "Platform 25",
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/8b63688f-d402-445a-9a1d-4d2ccc6b57d0"     
    },
    {
        "id": 1420,
        "name": "AWK",
        "pickup_time": "19:00",
        "platform": "Platform 34",
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/23c1511d-e854-4aff-b9c0-ab8bae58835b"     
    },
    {
        "id": 1414,
        "name": "RAR",
        "pickup_time": "21:00",
        "platform": "Platform 15",
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/c6a47d13-72cb-4edc-96ef-4862a99f7895"     
    },
    {
        "id": 1424,
        "name": "9HI",
        "pickup_time": "21:00 - 21:30",
        "platform": "Platform ***",
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/f19f4b88-b9eb-4fdf-bef5-35133f9d85cf"     
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

