#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
统一的HTTP客户端，用于设置User-Agent和其他通用配置
"""

import requests
from instock.core.singleton_proxy import proxys
import time
import random

# 默认User-Agent，模拟现代浏览器
DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"

# 东方财富网需要的Cookie设置
EASTMONEY_COOKIE = "qgqp_b_id=d9603ee43a43c3fcda7a643af5b10581; st_nvi=DNgOUwl4-dConj5suyRHO6e76; st_si=07932919336390; st_pvi=06135546313648; st_sp=2025-11-21%2011%3A13%3A13; st_inirUrl=; st_sn=1; st_psi=20251121111313207-113200301321-0650867276; st_asi=delete; nid=06545c30579aca550a182fb44b85a021; nid_create_time=1763694793578; gvi=ShBFoUUT-JVAZhI_NaWfF99ec; gvi_create_time=1763694793578; fullscreengg=1; fullscreengg2=1"

# 默认请求头
DEFAULT_HEADERS = {
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": DEFAULT_USER_AGENT,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9"
}

def get_session():
    """
    创建一个带有默认配置的requests Session
    :return: requests.Session对象
    """
    session = requests.Session()
    session.headers.update(DEFAULT_HEADERS)
    return session

def get(url, **kwargs):
    """
    发送GET请求，自动添加默认User-Agent和代理
    :param url: 请求URL
    :param kwargs: 其他requests参数
    :return: requests.Response对象
    """
    # 添加随机延时，避免请求过于频繁
    # time.sleep(random.uniform(1, 3))
    
    # 添加默认headers（如果未提供）
    if 'headers' not in kwargs:
        kwargs['headers'] = DEFAULT_HEADERS.copy()
    else:
        # 如果提供了headers，确保包含User-Agent
        headers = DEFAULT_HEADERS.copy()
        headers.update(kwargs['headers'])
        kwargs['headers'] = headers
    
    # 添加代理（如果可用）
    if 'proxies' not in kwargs:
        proxies = proxys().get_proxies()
        if proxies:
            kwargs['proxies'] = proxies

    # 特殊处理东方财富网API，添加必要的Cookie
    if "eastmoney.com" in url:
        if 'headers' not in kwargs:
            kwargs['headers'] = {}
        # 添加东方财富网所需的Cookie
        kwargs['headers']['Cookie'] = EASTMONEY_COOKIE
    
    return requests.get(url, **kwargs)

def post(url, **kwargs):
    """
    发送POST请求，自动添加默认User-Agent和代理
    :param url: 请求URL
    :param kwargs: 其他requests参数
    :return: requests.Response对象
    """
    # 添加随机延时，避免请求过于频繁
    # time.sleep(random.uniform(1, 3))
    
    # 添加默认headers（如果未提供）
    if 'headers' not in kwargs:
        kwargs['headers'] = DEFAULT_HEADERS.copy()
    else:
        # 如果提供了headers，确保包含User-Agent
        headers = DEFAULT_HEADERS.copy()
        headers.update(kwargs['headers'])
        kwargs['headers'] = headers
    
    # 添加代理（如果可用）
    if 'proxies' not in kwargs:
        proxies = proxys().get_proxies()
        if proxies:
            kwargs['proxies'] = proxies
    
    # 特殊处理东方财富网API，添加必要的Cookie
    if "eastmoney.com" in url:
        if 'headers' not in kwargs:
            kwargs['headers'] = {}
        # 添加东方财富网所需的Cookie
        kwargs['headers']['Cookie'] = EASTMONEY_COOKIE
    
    return requests.post(url, **kwargs)