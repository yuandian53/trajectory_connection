import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import re
# ------------------------------------ 常量 ------------------------------------ #
notReservedColumn=['traveled_d', 'avg_speed']
# %% 函数
def extract_first_and_last_numbers(text):
    """
    Extract first and last numbers from a string

    Args:
        text (_type_): _description_

    Returns:
        _type_: _description_
    """

    # 提取第一个数字
    first_number_match = re.search(r'\d', text)
    first_number = first_number_match.group() if first_number_match else None

    # 提取最后一个数字
    last_number_match = re.search(r'\d', text[::-1])
    last_number = last_number_match.group() if last_number_match else None

    return first_number, last_number

def read_left_file_id_csv_to_dataframe(left_file_id, folder_path='轨迹数据集2'):
    """
    读取文件夹中所有以'left_file_id'开头的CSV文件，并返回一个DataFrame对象。
    参数：
    - folder_path: 字符串，要搜索的文件夹路径。
    - left_file_id: 字符串，文件名的前缀。
    返回值：
    - dataframe: DataFrame对象，包含所有匹配文件的内容。每个文件的内容按行连接在一起。
    """
    # 获取文件夹中所有文件
    all_files = os.listdir(folder_path)
    # 筛选出文件名以'left_file_id'开头且以'.csv'结尾的文件
    left_file_id_csv_files = [file for file in all_files if file.startswith(
        left_file_id) and file.endswith('.csv')]
    # 读取所有匹配文件的内容，并连接成一个DataFrame
    dfs = {}
    for csv_file in left_file_id_csv_files:
        file_path = os.path.join(folder_path, csv_file)
        df = pd.read_csv(file_path)
        dfs[left_file_id+'-'+extract_first_and_last_numbers(csv_file)[1]] = df
    return dfs

def plot(df1, df2):
    """_summary绘制重叠区域的两条轨迹
    """
    # 绘制散点图
    plt.scatter(df2['x'], df2['y'], color='blue', label='id2',s=1)
    plt.scatter(df1['x'], df1['y'], color='red', label='id1',s=1)
    # 添加图例
    plt.legend()
    # 添加标签和标题
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Scatter Plot of id1 and id2')
    # 显示图形
    plt.show()

# %% 数据读取
# 指定包含Excel文件的文件夹路径
folder_path = '拼接结果'

# 创建一个空字典来存储数据
excel_dict = {}

# 遍历文件夹中的所有文件
for filename in os.listdir(folder_path):
    # 检查文件是否为Excel文件（假设扩展名为.xlsx）
    if filename.endswith('.xlsx'):
        # 构造完整的文件路径
        file_path = os.path.join(folder_path, filename)
        print(file_path)
        # 读取Excel文件
        excel_data = pd.read_excel(file_path)
        # 将数据添加到字典中，以文件名（不含扩展名）作为键
        excel_dict[os.path.splitext(filename)[0]] = excel_data
# 现在excel_dict包含了所有的Excel数据，键是文件名，值是对应的DataFrame
# ------------------------------------ aa ------------------------------------ #
# ------------------------------- 遍历所有的配对区域，5对 ------------------------------- #
for key, value in excel_dict.items():
    left_file_id = None
    right_file_id = None
    left_file_id, right_file_id = extract_first_and_last_numbers(key)
    print(left_file_id, right_file_id)
    # 读取left轨迹文件
    df_left_dict = read_left_file_id_csv_to_dataframe(left_file_id)
    df_left_dict.drop(columns=notReservedColumn,inplace=True)
    # 读取right轨迹文件
    df_right_dict = read_left_file_id_csv_to_dataframe(right_file_id)
    df_right_dict.drop(columns=notReservedColumn,inplace=True)
    # 遍历left轨迹文件
    for k, v in df_left_dict.items():
        matchs = value[value['p1_file'] == k]
        grouped_temp = v.groupby("track_id")
        for id1, group in grouped_temp:
            match = matchs[matchs['p1_ID'] == id1][['p2_ID', 'p2_file']]
            if not match.empty:
                id2 = match.values[0][0]
                file2 = match.values[0][1]
                track2 = df_right_dict[file2]
                track2 = track2[track2['track_id'] == id2]
                print(id1,id2)
                print('匹配车辆的行车方向')
                print(group['direction'].unique(), track2['direction'].unique())
                #可视化出两个区域轨迹的重叠情况
                plot(group, track2)
                # ---------------------------------- 得到重叠区域 ---------------------------------- #
                #left_region的x值小于right_region
                leftPoint=track2["x"].min()
                rightPoint=group["x"].max()
                # # 取出重叠区域(第1种方法)
                # # 计算与给定值最接近的一行的索引
                # leftNearestIndex = (group['x'] - leftPoint).abs().idxmin()
                # leftOverlapArea= group.loc[leftNearestIndex:]
                # rightNearestIndex = (track2['x'] - rightPoint).abs().idxmin()
                # rightOverlapArea = track2.loc[:rightNearestIndex]
                # plot(leftOverlapArea,rightOverlapArea)

                # 取出重叠区域(第2种方法)
                # 计算与给定值最接近的一行的索引
                leftNearestIndex = (group['x'] - leftPoint).abs().idxmin()
                leftOverlapArea= group.loc[leftNearestIndex:]
                rightNearestIndex = (track2['x'] - rightPoint).abs().idxmin()
                rightOverlapArea = track2.loc[:rightNearestIndex]
                plot(leftOverlapArea,rightOverlapArea)
                




    print(0)
