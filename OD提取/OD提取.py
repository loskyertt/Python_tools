import pandas as pd

# 读取数据文件
data_path = 'D:\\Desktop\\2024_GIS\\original_data\\track\\20140830_train.txt'

# 手动指定列名
column_names = ['vehicle_id', 'latitude', 'longitude', 'status', 'timestamp']
df = pd.read_csv(data_path, names=column_names)

# 确保数据按照车辆ID和时间排序
df.sort_values(by=['vehicle_id', 'timestamp'], inplace=True)

# 初始化存储OD点的列表
o_points = []
d_points = []

# 迭代每个车辆的轨迹数据
for vehicle_id, group in df.groupby('vehicle_id'):
    # 初始化载客状态
    current_status = 0

    for i in range(len(group)):
        row = group.iloc[i]
        status = row['status']

        if current_status == 0 and status == 1:
            # 当前状态从0变为1，记录为O点
            o_points.append([row['vehicle_id'], row['longitude'], row['latitude'], row['timestamp']])
        elif current_status == 1 and status == 0:
            # 当前状态从1变为0，记录为D点
            d_points.append([row['vehicle_id'], row['longitude'], row['latitude'], row['timestamp']])

        # 更新当前状态
        current_status = status

# 转换为DataFrame
o_points_df = pd.DataFrame(o_points, columns=['vehicle_id', 'longitude', 'latitude', 'timestamp'])
d_points_df = pd.DataFrame(d_points, columns=['vehicle_id', 'longitude', 'latitude', 'timestamp'])

# 将O点和D点数据分别保存到CSV文件
o_points_df.to_csv('D:\\Desktop\\2024_GIS\\output_data\\output_data_OD提取\\start_data.csv', index=False)
d_points_df.to_csv('D:\\Desktop\\2024_GIS\\output_data\\output_data_OD提取\\end_data.csv', index=False)

print("OD点数据提取完成。")
