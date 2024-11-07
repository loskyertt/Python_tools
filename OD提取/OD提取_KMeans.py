import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


class DataPreprocessor:
    """用于数据预处理的工厂类"""

    def __init__(self, data: pd.DataFrame):
        """初始化参数

        Args:
            data (pd.DataFrame): DataFrame 类型
        """
        self.data = data[['lon', 'lat']]
        self.scaler = StandardScaler()

    def preprocess(self):
        """预处理数据的经纬度

        Returns:
            ndarray: 返回处理后的数组
        """
        data_scaled = self.scaler.fit_transform(self.data)
        return data_scaled

    def inverse_transform(self, data):
        return self.scaler.inverse_transform(data)


class KMeansCluster:
    """用于KMeans聚类分析的工厂类"""

    def __init__(self, data, n_clusters=10):
        self.data = data
        self.n_clusters = n_clusters
        self.model = KMeans(n_clusters=n_clusters, random_state=0)

    def perform_clustering(self):
        labels = self.model.fit_predict(self.data)
        centers = self.model.cluster_centers_
        return labels, centers


class ClusterMatcher:
    """用于匹配 O 点和 D 点簇的工厂类"""

    def __init__(self, o_points_df, d_points_df, o_labels, d_labels, o_centers, d_centers):
        self.o_points_df = o_points_df
        self.d_points_df = d_points_df
        self.o_labels = o_labels
        self.d_labels = d_labels
        self.o_centers = o_centers
        self.d_centers = d_centers

    def get_cluster_info(self, df, labels, centers):
        clusters = []
        for label in np.unique(labels):
            cluster_points = df[labels == label]
            center = centers[label]
            size = len(cluster_points)
            clusters.append(
                {'cluster_id': label, 'center': center, 'size': size})
        return clusters

    def match_clusters(self):
        o_clusters = self.get_cluster_info(
            self.o_points_df, self.o_labels, self.o_centers)
        d_clusters = self.get_cluster_info(
            self.d_points_df, self.d_labels, self.d_centers)

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
                    o_cluster_id, o_center[1], o_center[0],  # 注意这里交换了经纬度顺序
                    # 注意这里交换了经纬度顺序
                    d_cluster_id, d_center[1], d_center[0], match_count
                ])
        return results


if __name__ == "__main__":

    print("开始读取文件......")

    # 读取OD点数据
    o_points_df = pd.read_csv(r'OD提取\data\input\O_20161109.csv')
    d_points_df = pd.read_csv(r'OD提取\data\input\D_20161109.csv')

    print("开始数据处理......")

    # 数据预处理
    o_preprocessor = DataPreprocessor(o_points_df)
    d_preprocessor = DataPreprocessor(d_points_df)

    o_data_scaled = o_preprocessor.preprocess()
    d_data_scaled = d_preprocessor.preprocess()

    # KMeans聚类
    n_clusters = 10
    o_kmeans = KMeansCluster(o_data_scaled, n_clusters)
    d_kmeans = KMeansCluster(d_data_scaled, n_clusters)

    o_labels, o_centers = o_kmeans.perform_clustering()
    d_labels, d_centers = d_kmeans.perform_clustering()

    # 逆转换聚类中心到原始经纬度
    o_centers = o_preprocessor.inverse_transform(o_centers)
    d_centers = d_preprocessor.inverse_transform(d_centers)

    # 匹配簇
    matcher = ClusterMatcher(o_points_df, d_points_df,
                             o_labels, d_labels, o_centers, d_centers)
    results = matcher.match_clusters()

    # 输出结果到CSV文件
    results_df = pd.DataFrame(results, columns=[
        'O_cluster', 'O_lat', 'O_lon',
        'D_cluster', 'D_lat', 'D_lon', 'match_cnt'
    ])
    results_df.to_csv(
        r'OD提取\data\output\OD_cluster_matches_kmeans.csv', index=False)

    print("OD点簇匹配结果已保存到 OD_cluster_matches_kmeans.csv 文件中。")
