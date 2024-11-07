import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString
import warnings
from shapely.errors import ShapelyDeprecationWarning

# 忽略 shaply 的启用警告
warnings.filterwarnings("ignore", category=ShapelyDeprecationWarning)


def xy_to_line(filename: str) -> tuple[gpd.GeoDataFrame, gpd.GeoDataFrame, gpd.GeoDataFrame]:
    """用于 OD 提取后的转线操作

    Args:
        filename (str): [传入的文件路径]

    Returns:
        tuple[gpd.GeoDataFrame, gpd.GeoDataFrame, gpd.GeoDataFrame]: [包含三个 gpd.GeoDataFrame 的元组]
    """

    print("读取文件中......")
    df = pd.read_csv(filename)

    print("开始转换......")

    # 批量创建起点和终点的Point对象
    df['O_geometry'] = [Point(xy) for xy in zip(
        df['O_lon'], df['O_lat'])]
    df['D_geometry'] = [Point(xy) for xy in zip(
        df['D_lon'], df['D_lat'])]

    # 批量创建LineString对象
    df['Line_geometry'] = [LineString(xy) for xy in zip(
        list(zip(df['O_lon'], df['O_lat'])),
        list(zip(df['D_lon'], df['D_lat']))
    )]

    # 创建 GeoDataFrames
    gdf_origin = gpd.GeoDataFrame(df, geometry='O_geometry')
    gdf_destination = gpd.GeoDataFrame(df, geometry='D_geometry')
    gdf_line = gpd.GeoDataFrame(df, geometry='Line_geometry')

    # 设置坐标系编码 WGS84
    gdf_origin.set_crs(epsg=4326, inplace=True)
    gdf_destination.set_crs(epsg=4326, inplace=True)
    gdf_line.set_crs(epsg=4326, inplace=True)

    return gdf_origin, gdf_destination, gdf_line


if __name__ == "__main__":
    filename = r"OD提取\data\output\OD_cluster_matches_kmeans.csv"
    gdf_o, gdf_d, gdf_line = xy_to_line(filename)

    gdf_o.to_file(r"xy转线\data\output\O_points.shp", driver='ESRI Shapefile')
    gdf_d.to_file(r"xy转线\data\output\D_points.shp", driver='ESRI Shapefile')
    gdf_line.to_file(r"xy转线\data\output\lines.shp", driver='ESRI Shapefile')

    print("转换成功！")
