import numpy as np

def haversine_distance(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
    """计算两点间的haversine距离

    Args:
        lon1 (float): longitude 1
        lat1 (float): latitude 1
        lon2 (float): longitude 2
        lat2 (float): latitude 2

    Returns:
        float: 两点间的距离
    """
    R = 6371  # 地球半径（千米）

    # 转换为弧度
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2
    c = 2 * np.arcsin(np.sqrt(a))
    km = R * c

    return km


if __name__ == "__main__":

    x1 = 37.779388
    y1 = -122.423246
    x2 = 32.719464
    y2 = -117.220406

    print(haversine_distance(y1, x1, y2, x2)) # 734.4119414181606