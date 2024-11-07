import requests


def get_local_proxy(port: int) -> str:
    """获取本地代理 IP

    Args:
        port (int): 代理端口号

    Returns:
        str: 完整的代理地址，如： 134.22.201.86:7890
    """

    # 代理地址，设置为本地代理的地址和端口
    proxy = {
        # 记得改成自己代理的端口号
        'http': f'http://localhost:{port}',
        'https': f'http://localhost:{port}',
    }

    # 访问外部API，获取代理IP
    try:
        response = requests.get('http://api.ipify.org', proxies=proxy)
        current_ip = response.text
        ip_addr = f"{current_ip}:{port}"
        return ip_addr
    except requests.RequestException as e:
        print(f"Error retrieving IP: {e}")


# 获取代理池的免费 IP
# -----------------------------------------------------------------------
def get_free_proxy() -> str:
    """获取代理池中的免费 IP

    Returns:
        str: 用 get("proxy") 获得完整的代理地址，如： 134.22.201.86:7890
    """
    return requests.get("http://127.0.0.1:5010/get/").json()


def delete_proxy(proxy) -> None:
    """删除当前从代理池获得的 IP

    Args:
        proxy (str): 完整的代理地址，如： 134.22.201.86:7890
    """
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))
# -----------------------------------------------------------------------


if __name__ == "__main__":

    print(get_local_proxy(7890))
    print(type(get_local_proxy(7890)))

    print(get_free_proxy().get("proxy"))
