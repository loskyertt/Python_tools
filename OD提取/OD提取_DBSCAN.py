import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler


class DataPreprocessor:
    """用于数据预处理的工厂类"""

    def __init__(self, data):
        self.data = data[['lon', 'lat']]
        self.scaler = StandardScaler()

    def preprocess(self):
        data_scaled = self.scaler.fit_transform(self.data)
        return data_scaled


class DBSCANCluster:
    """用于DBSCAN聚类分析的工厂类"""

    def __init__(self, data, eps=0.2, min_samples=5):
        self.data = data
        self.eps = eps
        self.min_samples = min_samples
        self.model = DBSCAN(eps=self.eps, min_samples=self.min_samples)

    def perform_clustering(self):
        labels = self.model.fit_predict(self.data)
        return labels


class ClusterMatcher:
    """用于匹配 O 点和 D 点簇的工厂类"""

    def __init__(self, o_points_df, d_points_df, o_labels, d_labels):
        self.o_points_df = o_points_df
        self.d_points_df = d_points_df
        self.o_labels = o_labels
        self.d_labels = d_labels

    def get_cluster_info(self, df, labels):
        clusters = []
        for label in np.unique(labels):
            if label == -1:
                continue
            cluster_points = df[labels == label]
            center = cluster_points[['lon', 'lat']].mean().values
            size = len(cluster_points)
            clusters.append(
                {'cluster_id': label, 'center': center, 'size': size})
        return clusters

    def match_clusters(self, o_clusters, d_clusters):
        results = []
        for o_cluster in o_clusters:
            o_cluster_id = o_cluster['cluster_id']
            o_center = o_cluster['center']
            o_order_ids = set(
                self.o_points_df[self.o_labels == o_cluster_id]['order_id'])

            for d_cluster in d_clusters:
                d_cluster_id = d_cluster['cluster_id']
                d_center = d_cluster['center']
                d_order_ids = set(
                    self.d_points_df[self.d_labels == d_cluster_id]['order_id'])

                common_order_ids = o_order_ids.intersection(d_order_ids)
                match_count = len(common_order_ids)

                results.append([
                    o_cluster_id, o_center[0], o_center[1],
                    d_center[0], d_center[1], match_count
                ])
        return results


if __name__ == "__main__":

    # 读取OD点数据
    print("开始读取文件......")
    o_points_df = pd.read_csv(
        r'OD提取\data\input\O_20161109.csv')
    d_points_df = pd.read_csv(
        r'OD提取\data\input\D_20161109.csv')

    # 数据预处理
    print("开始数据预处理......")
    o_preprocessor = DataPreprocessor(o_points_df)
    d_preprocessor = DataPreprocessor(d_points_df)

    o_data_scaled = o_preprocessor.preprocess()
    d_data_scaled = d_preprocessor.preprocess()

    # DBSCAN聚类
    print("开始DBSCAN聚类分析......")
    o_cluster_model = DBSCANCluster(o_data_scaled)
    d_cluster_model = DBSCANCluster(d_data_scaled)

    o_labels = o_cluster_model.perform_clustering()
    d_labels = d_cluster_model.perform_clustering()

    # 提取簇信息
    matcher = ClusterMatcher(o_points_df, d_points_df, o_labels, d_labels)
    o_clusters = matcher.get_cluster_info(o_points_df, o_labels)
    d_clusters = matcher.get_cluster_info(d_points_df, d_labels)

    # 匹配簇
    print("开始OD点簇匹配......")
    results = matcher.match_clusters(o_clusters, d_clusters)

    # 输出结果到CSV文件
    results_df = pd.DataFrame(results, columns=[
        'O_cluster', 'O_lon', 'O_lat',
        'D_lon', 'D_lat', 'match_cnt'
    ])
    results_df.to_csv(
        r'OD提取\data\output\OD_cluster_matches_dbscan.csv', index=False)

    print("OD点簇匹配结果已保存到 OD_cluster_matches_dbscan.csv 文件中。")
