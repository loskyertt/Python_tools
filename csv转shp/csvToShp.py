import geopandas as gpd
import pandas as pd
from pyproj import Transformer
from shapely.geometry import Point


def convert_to_wgs84(lons, lats) -> tuple:
    """把 CGCS2000(EPSG:4490) 坐标系统转换为 WGS84("EPSG:4326)

    Args:
        lons (ndarray): 经度
        lats (ndarray): 纬度

    Returns:
        tuple: 转换后的经度、纬度坐标
    """
    transformer = Transformer.from_crs(
        "EPSG:4490", "EPSG:4326", always_xy=True)
    return transformer.transform(lons, lats)


def convert_to_coordinate(lons, lats) -> tuple:
    """需要转换其它坐标系统，在这里实现

    Args:
        lons (ndarray): 经度
        lats (ndarray): 纬度

    Returns:
        tuple: 转换后的经度、纬度坐标
    """
    pass


def convert_csv_to_shp(input_csv: str, output_shp: str, size: int | None = None, random: int = False) -> None:
    """csv 转 shp ，坐标系默认是 WGS84

    Args:
        input_csv (str): 传入的 csv 文件路径
        output_shp (str): 输出的 shp 文件路径
        size (int | None, optional): 顺序读取 csv 的行数 | 随机读取 csv 文件的行数（取决于 random 参数）. Defaults to None.
        random (int | None, optional): 是否随机读取 csv 文件. Defaults to False.
    """
    if random:
        df = pd.read_csv(input_csv).sample(
            n=size, random_state=42)     # 随机数种子根据自己需求修改
    else:
        df = pd.read_csv(
            input_csv, nrows=size) if size else pd.read_csv(input_csv)

    # 批量转换坐标系
    lons, lats = df['lon'].values, df['lat'].values     # 这里需要注意对应的经纬度字段
    wgs84_lons, wgs84_lats = convert_to_wgs84(lons, lats)   # 需要其它坐标系的话，在这里修改

    # 创建几何列
    df['geometry'] = [Point(lon, lat)
                      for lon, lat in zip(wgs84_lons, wgs84_lats)]

    # 列名处理，移除特殊字符并截断至10字符
    df.columns = [col.replace(
        '/', '_').replace('(', '_').replace(')', '_')[:10] for col in df.columns]

    # 创建 GeoDataFrame
    gdf = gpd.GeoDataFrame(df, geometry='geometry', crs="EPSG:4326")

    try:
        # 尝试直接用 UTF-8 保存
        gdf.to_file(output_shp, encoding='utf-8')
    except Exception as e:
        print(f"UTF-8 保存失败，尝试使用 GBK 编码保存: {str(e)}")
        try:
            # 如果 UTF-8 失败，尝试用 GBK
            gdf.to_file(output_shp, encoding='gbk')
        except Exception as e:
            print(f"GBK 保存也失败，尝试使用 CP936 编码: {str(e)}")
            # 最后尝试使用 CP936
            gdf.to_file(output_shp, encoding='cp936')


if __name__ == "__main__":
    print("开始数据转换......")
    input_file = r'OD提取\data\input\D_20161109.csv'
    output_file = r"csv转shp\data\output\D_20161109.shp"
    convert_csv_to_shp(input_file, output_file)
    print("转换完成！")
