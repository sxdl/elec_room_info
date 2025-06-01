import re
import random
import requests
from datetime import datetime
from typing import Optional

from .record_csv import CSVRecordHandler
from .config import Config

from .log import get_logger
logger = get_logger(__name__)


# def create_query_form_data(info_json):
#     aids = ['0030000000004901', '0030000000011101', '0030000000011201']
#     aid = aids[eval(info_json['type'])]
#     area = '{"area":"","areaname":""}'
#     building = (f'{{"building":"{info_json["building"].split("&&&")[0]}","buildingid":'
#                 f'"{info_json["building"].split("&&&")[1]}"}}')
#     floor = f'{{"floor":"{info_json["floor"].split("&&&")[0]}","floorid":"{info_json["floor"].split("&&&")[1]}"}}'
#     room = f'{{"room":"{info_json["room"].split("&&&")[0]}","roomid":"{info_json["room"].split("&&&")[1]}"}}'
#     return {
#         'aid': aid,
#         'area': area,
#         'building': building,
#         'floor': floor,
#         'room': room
#     }


# def create_url(api_name):
#     v = random.randint(1, 100)  # 生成1到100的随机整数
#     return f'https://weixinchongzhi.scut.edu.cn/wechat/{api_name}.html?v={v}'


class ElecRoomQuery:
    """
    宿舍水电空调余额查询类
    """
    def __init__(self, **kwargs):
        """
        :param kwargs: 'session_id': 浏览器会话cookie, 'auth_link': 企业微信学生一卡通应用链接, 'csv_file_path': csv文件保存路径
        """
        self._config: Config = kwargs.get('config')

        self._bearer_token = self._config['query']['bearer_token']

        # self._session = self._config['query']['session_id']
        # self._auth_link = self._cfg['query']['auth_link']

        # self._session = kwargs.get('session_id', None)
        # self._auth_link = kwargs.get('auth_link', None)

        # if self._session == '' and self._auth_link == '':
        #     logger.error('ElecRoomQuery needs session_id or auth_link')
        #     raise ValueError('ElecRoomQuery needs session_id or auth_link')

        if self._bearer_token == '':
            logger.error("无 bearer token!")
            raise

        self._headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'ecardwxnew.scut.edu.cn',
            'Referer': 'https://ecardwxnew.scut.edu.cn/plat/shouyeUser',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/107.0.5304.110 Safari/537.36 Language/zh ColorScheme/Light wxwork/4.1.32 ('
                          'MicroMessenger/6.2) WindowsWechat  MailPlugin_Electron WeMail embeddisk wwmver/3.26.15.675',
            'synAccessSource': 'wechat-work',
            'sec-ch-ua': '"Chromium";v="107"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'synjones-auth': f"Bearer {self._bearer_token}"
        }
        # self._cookies = {'JSESSIONID': self._session}

        # self._WAT_FORM_DATA = create_query_form_data(self.auto_query(type=0))
        # self._ELE_FORM_DATA = create_query_form_data(self.auto_query(type=1))
        # self._AIR_FORM_DATA = create_query_form_data(self.auto_query(type=2))
        # logger.debug(f'WAT_FORM_DATA: {self._WAT_FORM_DATA}')
        # logger.debug(f'ELE_FORM_DATA: {self._ELE_FORM_DATA}')
        # logger.debug(f'AIR_FORM_DATA: {self._AIR_FORM_DATA}')

        self._CSV_FILE_PATH = self._config['record_csv']['csv_file_path']


    # def _get_session_from_auth_link(self, auth_link):
    #     """企业微信 > 校园一卡通， 分享的连接"""
    #     headers = {
    #         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
    #                   '*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    #         'Accept-Encoding': 'gzip, deflate, br',
    #         'Accept-Language': 'zh-CN,zh;q=0.9',
    #         'Connection': 'keep-alive',
    #         'Host': 'ecardwxnew.scut.edu.cn',
    #         'referer': 'https://ecardwxnew.scut.edu.cn/plat/shouyeUser',
    #         'Sec-Fetch-Dest': 'empty',
    #         'Sec-Fetch-Mode': 'cors',
    #         'Sec-Fetch-Site': 'same-origin',
    #         'Sec-Fetch-User': '?1',
    #         'Upgrade-Insecure-Requests': '1',
    #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
    #                       'Chrome/107.0.5304.110 Safari/537.36 Language/zh ColorScheme/Light wxwork/4.1.32 ('
    #                       'MicroMessenger/6.2) WindowsWechat  MailPlugin_Electron WeMail embeddisk wwmver/3.26.15.675',
    #         'sec-ch-ua': '"Chromium";v="107"',
    #         'sec-ch-ua-mobile': '?0',
    #         'sec-ch-ua-platform': '"Windows"',
    #         'synAccessSource': 'wechat-work',
    #     }
    #     try:
    #         response = requests.get(auth_link, headers=headers)
    #
    #         if response.status_code == 200:
    #             set_cookie = response.headers.get('Set-Cookie')
    #             if set_cookie:
    #                 logger.debug(f'set_cookie: {set_cookie}')
    #                 self._session = set_cookie.split(';')[0].split('=')[1]
    #             else:
    #                 logger.debug(f'set_cookie: None')
    #                 raise Exception("Set-Cookie header not found in the response")
    #         else:
    #             response.raise_for_status()  # 如果请求失败，会抛出异常
    #     except requests.RequestException as e:
    #         logger.error(f'Error: {e}')


    def refresh_session(self):
        """session失效刷新"""
        pass

    def query_elec_room_info(self, type):
        """余额查询 type: 1(电)，2(空调)，3(水)"""
        base_url = 'https://ecardwxnew.scut.edu.cn'
        url = base_url + '/charge/feeitem/getThirdDataByFeeItemId' + f'?feeitemid={type}' + '&synAccessSource=wechat-work'
        # params = {
        #     'aid': aid,
        #     'area': area,
        #     'building': building,
        #     'floor': floor,
        #     'room': room
        # }

        try:
            response = requests.get(url, headers=self._headers)
            response.raise_for_status()  # 如果请求失败，会抛出异常
            logger.debug(f'queryElecRoomInfo response: {response.json()}')
            # print('Query response:', response.json())
            return response.json()['map']['showData']['信息']
        except requests.RequestException as e:
            logger.error(f'Error querying room info: {e}')
            # print('Error querying room info:', e)

    # def auto_query(self, type: int):
    #     """
    #     房间信息查询
    #     :param type: 0(水)，1(电)，2(空调)
    #     :return: {'account','building','floor','id','refreshTime','room','schoolId','type'}
    #     """
    #     url = create_url(api_name='icinfo/autoQuery')
    #     params = {
    #         'type': type
    #     }
    #
    #     try:
    #         response = requests.post(url, data=params, cookies=self._cookies, headers=self._headers)
    #         response.raise_for_status()
    #         response_json = response.json()
    #         logger.debug(f'autoQuery response: {response_json}')
    #         if response_json == 1:
    #             # session 过期
    #             # self._cfg.set('query', 'session_id', '')
    #             self._config.query.session_id = ''
    #             self._config.save()
    #             logger.critical(f'session expired, refresh your auth link')
    #         return response_json
    #     except requests.RequestException as e:
    #         logger.error('Error autoQuery:', e)

    def _extract_float(self, text_value: str) -> Optional[float]:
        """
        从可能包含非数字字符的字符串中稳健地提取浮点数。
        例如："房间当前剩余电量14.60元" -> 14.60
              "房间当前剩余金额35.22" -> 35.22
              "14.30" -> 14.30
        如果找不到或无法转换，则返回 None。
        """
        if text_value is None:
            return None
        # 正则表达式查找一个一个数字
        match = re.search(r'(\d+\.?\d*)', str(text_value))
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                logger.error(f"Could not convert extracted string '{match.group(1)}' to float from '{text_value}'")
                return None
        else:
            logger.warning(f"Could not find numeric value in '{text_value}'")
            return None

    def query_balance(self):
        """
        查询水电空调余额。
        :return: 包含时间戳和各项余额（浮点数）的字典。
                 如果任何一项查询或解析失败，则返回 None。
                 Example: {'timestamp': '...', 'water_balance': 14.3, 'electricity_balance': 14.60, 'air_conditioner_balance': 35.22}
        """
        # type: 1(电), 2(空调), 3(水)
        raw_electricity_info = self.query_elec_room_info(1)
        raw_air_conditioner_info = self.query_elec_room_info(2)
        raw_water_info = self.query_elec_room_info(3)

        if raw_electricity_info is None or raw_air_conditioner_info is None or raw_water_info is None:
            logger.error("Failed to retrieve raw data for one or more utilities. Check previous logs for query_elec_room_info errors.")
            return None

        electricity_balance = self._extract_float(raw_electricity_info)
        air_conditioner_balance = self._extract_float(raw_air_conditioner_info)
        water_balance_str_part = ""
        if raw_water_info:
            match_water_keyword = re.search(r'剩余水费([\d\.]+)', raw_water_info)
            if match_water_keyword:
                water_balance_str_part = match_water_keyword.group(0)
            else:
                parts = raw_water_info.split(',')
                water_balance_str_part = parts[-1]

        water_balance = self._extract_float(water_balance_str_part)

        # 如果任何一个余额解析失败，则整个操作失败
        if electricity_balance is None or air_conditioner_balance is None or water_balance is None:
            logger.error(
                f"Failed to parse one or more balances. Raw: E='{raw_electricity_info}', A='{raw_air_conditioner_info}', W='{raw_water_info}'. "
                f"Parsed: E={electricity_balance}, A={air_conditioner_balance}, W={water_balance}"
            )
            return None

        record_data = {
            'timestamp': datetime.now().isoformat(),
            'electricity_balance': electricity_balance,
            'air_conditioner_balance': air_conditioner_balance,
            'water_balance': water_balance
        }
        logger.info(f"Successfully queried and parsed balances: {record_data}")
        return record_data

    def record_data(self):
        """disposed"""
        balance_data = self.query_balance()
        if balance_data and self._CSV_FILE_PATH:
            try:
                recorder = CSVRecordHandler(csv_file_path=self._CSV_FILE_PATH)
                recorder.record(balance_data)
                logger.info(f"Data recorded successfully to {self._CSV_FILE_PATH}: {balance_data}")
            except Exception as e:
                logger.error(f"Failed to record data to CSV at {self._CSV_FILE_PATH}: {e}")
        elif not balance_data:
            logger.warning("No balance data to record, query_balance might have failed or returned None.")
        elif not self._CSV_FILE_PATH:
            logger.warning("CSV_FILE_PATH is not set. Cannot record data.")


if __name__ == '__main__':
    from pathlib import Path
    from elec_room_info.utils.config import Config

    CONFIG_PATH = Path(__file__).parents[2] / 'data' / 'configs' / 'config.yaml'
    query = ElecRoomQuery(config=Config(CONFIG_PATH))
    query.record_data()
