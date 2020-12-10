# -*- coding: UTF-8 -*-

import re
import regex
import json
import requests
from loguru import logger
from datetime import datetime


def format_string(ustring):
    """
    全角转半角，多个连续控制符、空格替换成单个空格
    """
    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 12288:  # 全角空格直接转换
            inside_code = 32
        elif 65281 <= inside_code <= 65374:  # 全角字符（除空格）转化
            inside_code -= 65248

        rstring += chr(inside_code)
    return regex.sub(r'[\p{Z}\s]+', ' ', rstring.strip())


def request_tfserving(text, timeout=1):
    tfserving_url = 'http://192.168.5.248:8501/v1/models/sms_loan:predict'
    requests.adapters.DEFAULT_RETRIES = 5
    s = requests.session()
    s.keep_alive = False
    label = 0
    try:
        response = s.post(tfserving_url, json={"inputs": [text]}, timeout=timeout)
        # response = s.post(tfserving_url, json={"instances": [text]}, timeout=timeout)
        if response.status_code == requests.codes.ok:
            # response.encoding = 'utf-8'
            # res = response.text
            # print(type(res))
            # print(res)
            # json_resp = json.loads(response.content)
            json_resp = response.json()
            print(type(json_resp), json_resp)
            # pred = res.get('predictions', [[0]])
            # if pred[0][0] >= self.fraud_loan_threshold:
            #     label = 1
            # else:
            #     label = 0
            # logger.debug(f'fraud loan tfserving Pred: {res} Label: {label}')
        else:
            logger.info(response.status_code)
    except Exception as e:
        logger.error(e)
    return label


text = '[安逸花]好消息!您的x元已经为您放行,月低至x.x%,点urlstrs取'
text = '【阿里云】尊敬的yueha****@163.com：您的可用额度为1.43元，已不足您设置的预警值5.00元，查看可用额度、变更预警值'
text = '款可提高信用星级，并有助于提升信用额度。快速充值 http://edianzu.cn/s/u/l'
text = '尊敬的用户，因您信用良好，入选2月19日特批名单，額度可达500000，随借随还，详情请回Y，如有打扰请谅解，退订回T'


st = datetime.now()
request_tfserving(text)
print(f'use time: {datetime.now() - st}')


# ustr = '你哈\r\t\n   buduan 👉 錒嗄 。  ， ？ ！【书】 ‘小’ “中”'

# fmt_str = format_string(ustr)
# print(fmt_str)
