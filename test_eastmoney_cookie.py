#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试访问东方财富网API，检查是否还需要额外的Cookie或Referer设置
用浏览器依次访问以下URL，看看是否正常，可能需要更新cookie
https://quote.eastmoney.com/center/gridlist.html
http://82.push2.eastmoney.com/api/qt/clist/get?pn=1&pz=50&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f12&fs=m:0%20t:6,m:0%20t:80,m:1%20t:2,m:1%20t:23,m:0%20t:81%20s:2048&fields=f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f14,f15,f16,f17,f18,f20,f21,f22,f23,f24,f25,f26,f37,f38,f39,f40,f41,f45,f46,f48,f49,f57,f61,f100,f112,f113,f114,f115,f221
"""

import sys
sys.path.append('.')

from instock.lib import http_client
import json

def test_eastmoney_api():
    """
    测试访问东方财富网API
    """
    # 使用东方财富网首页作为Referer
    url = "http://82.push2.eastmoney.com/api/qt/clist/get"
    params = {
        "pn": 1,
        "pz": 50,
        "po": "1",
        "np": "1",
        "ut": "bd1d9ddb04089700cf9c27f6f7426281",
        "fltt": "2",
        "invt": "2",
        "fid": "f12",
        "fs": "m:0 t:6,m:0 t:80,m:1 t:2,m:1 t:23,m:0 t:81 s:2048",
        "fields": "f12,f14",
        "_": "1623833739532",
    }
    
    print("正在测试访问东方财富网API...")
    print(f"URL: {url}")
    
    try:
        response = http_client.get(url, params=params)
        print(f"响应状态码: {response.status_code}")
        print(f"响应头中的Content-Type: {response.headers.get('Content-Type')}")
        
        if response.status_code == 200:
            data = response.json()
            print("成功获取到数据:")
            print(f"数据结构: {list(data.keys())}")
            if 'data' in data and 'diff' in data['data']:
                print(f"返回股票数量: {len(data['data']['diff'])}")
                if data['data']['diff']:
                    print(f"第一条股票数据示例: {data['data']['diff'][0]}")
            else:
                print("数据格式不符合预期")
                print(f"实际数据: {data}")
        else:
            print(f"请求失败，状态码: {response.status_code}")
            print(f"响应内容: {response.text[:500]}...")
            
    except Exception as e:
        print(f"发生异常: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_eastmoney_api()