import logging
from time import sleep

import requests
from requests.exceptions import ProxyError, RequestException
from urllib3.exceptions import MaxRetryError, NameResolutionError

from 爬虫.proxy.getProxy import delete_proxy, get_free_proxy


def get_data(html_data, output_file: str) -> bool:
    """解析网页元素

    Args:
        html_data (html): 向网站请求到的 html 数据
        output_file (str): 输出文件路径

    Returns:
        bool: 用于判断是否解析成功
    """

    pass


def fetch_page(url: str, headers: dict, proxy: str, max_retries: int = 10, delay: int = 5):
    """获取页面信息

    Args:
        url (str): 网页链接
        headers (dict): 请求头
        proxy (str): 代理
        max_retries (int, optional): 最大尝试次数. Defaults to 10.
        delay (int, optional): 最大休眠延迟. Defaults to 5.

    Returns:
        html_data | None: 爬取到的网页
    """
    for attempt in range(max_retries):
        proxies = {
            "http": "http://" + proxy,
            "https": "http://" + proxy
        }
        print(f"第{attempt + 1}次的代理地址和端口：{proxy}")

        try:
            print(f"正在尝试获取页面: {url} (第 {attempt+1} 次尝试)")
            response = requests.get(
                url=url, headers=headers, proxies=proxies, timeout=5)
            response.raise_for_status()

            print(f"页面获取成功: {url}")
            return response.text, proxy, None  # 请求成功，返回页面数据

        except (RequestException, NameResolutionError, MaxRetryError, ProxyError) as e:
            logging.warning(f"第 {attempt + 1} 次尝试失败: {str(e)}")
            delete_proxy(proxy)  # 请求失败时删除代理
            proxy = get_free_proxy().get("proxy")  # 更新代理
            if attempt < max_retries - 1:
                logging.info(f"{delay} 秒后重试...")
                sleep(delay)
            else:
                logging.error(f"重试次数已达上限，无法获取页面: {url}")
                return None, proxy, str(e)  # 这里需要返回能成功使用的代理地址


if __name__ == "__main__":

    # 记录日志信息
    logging.basicConfig(
        filename='./logs/scraper.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # 在这里设置请求头
    headers = {
        "User-Agent": "",
        "Cookie":  ""
    }

    # 这里设置链接
    base_url = ""
    output_file = "./data/results.csv"

    page = 1
    consecutive_name_resolution_errors = 0  # 记录解析错误次数
    max_consecutive_name_resolution_errors = 5  # 设置最大解析次数

    consecutive_empty_pages = 0  # 记录连续空页次数
    max_empty_pages = 3  # 设置最大连续空页数

    # 获取初始代理
    proxy = get_free_proxy().get("proxy")

    # 翻页实现
    while True:

        url = base_url.format(page)
        print(f"正在爬取第 {page} 页: {url}")

        # 获取 HTML
        html_data, proxy, error = fetch_page(url, headers, proxy)

        if html_data is None:
            # 如果代理无效或者请求失败，才更换代理
            if "NameResolutionError" in error:
                consecutive_name_resolution_errors += 1
                logging.warning(
                    f"连续第 {consecutive_name_resolution_errors} 次遇到名称解析错误！")
                if consecutive_name_resolution_errors >= max_consecutive_name_resolution_errors:
                    logging.error(f"达到最大连续名称解析错误次数，爬取终止！")
                    break
            else:
                logging.error(f"无法获取第 {page} 页，错误信息: {error}，继续尝试下一页")
                proxy = get_free_proxy().get("proxy")  # 更换代理
                page += 1
                continue
        else:
            consecutive_name_resolution_errors = 0

            if not get_data(html_data, output_file):
                consecutive_empty_pages += 1
                if consecutive_empty_pages >= max_empty_pages:
                    logging.info(f"连续 {max_empty_pages} 页没有数据，爬取终止。")
                    break
            else:
                consecutive_empty_pages = 0  # 重置空页计数器
                print(f"第 {page} 页数据成功爬取并保存。")

        # 随机休眠一段时间，模拟人类行为，避免被封禁
        # sleep_time = random.uniform(2, 5)
        # print(f"等待 {sleep_time:.2f} 秒后继续...")
        # sleep(sleep_time)
        page += 1
