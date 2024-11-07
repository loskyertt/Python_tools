import pandas as pd


def split_file(filename: str, split_ratio: float) -> None:
    """按比例二分文件

    Args:
        filename (str): 文件名
        split_ratio (float): 分割比例，范围(0, 1)
    """
    df = pd.read_csv(filename)
    split_index = int(len(df) * split_ratio)

    # 分割数据
    df_part1 = df[:split_index]
    df_part2 = df[split_index:]

    # 保存到两个新的CSV文件
    df_part1.to_csv(
        r'文件处理\data\input\part2_1.csv', index=False)
    df_part2.to_csv(
        r'文件处理\data\input\part2_2.csv', index=False)

    print("分割成功！")


def merge_file(filename_list: list[str]) -> None:
    """合并文件

    Args:
        filename_list (list[str]): 文件名列表
    """

    dataframes = []

    for filename in filename_list:
        df = pd.read_csv(filename)
        dataframes.append(df)

    # 按行合并所有 DataFrame
    df_merged = pd.concat(dataframes, axis=0)

    # 保存合并后的 CSV 文件
    df_merged.to_csv(r'文件处理\data\output\merged_file.csv', index=False)

    print("合并成功！")


if __name__ == "__main__":
    # 分割文件
    filename = r"文件处理\data\input\part2.csv"
    split_file(filename=filename, split_ratio=0.5)

    # 合并文件
    # file_list = [r"文件处理\data\input\processed_二手房数据_part1_1.csv",
    #              r"文件处理\data\input\processed_二手房数据_part1_2.csv",
    #              r"文件处理\data\input\processed_二手房数据_part2_1.csv",
    #              r"文件处理\data\input\processed_二手房数据_part2_2.csv"]
    # merge_file(file_list)
