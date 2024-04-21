import re
import os
import pandas as pd
import numpy as np
from fastdtw import fastdtw
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

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

def read_left_file_id_csv_to_dataframe(left_file_id,  notReservedColumn, folder_path='轨迹数据集2'):
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
        df.drop(columns=notReservedColumn,inplace=True)
        dfs[left_file_id+'-'+extract_first_and_last_numbers(csv_file)[1]] = df
    return dfs

def plot(df1, df2):
    """_summary绘制重叠区域的两条轨迹
    """
    # 绘制散点图
    plt.scatter(df2['x'], df2['y'], color='blue', label='id2',s=1,alpha=0.5)
    plt.scatter(df1['x'], df1['y'], color='red', label='id1',s=1,alpha=0.5)
    # 添加图例
    plt.legend()
    # 添加标签和标题
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Scatter Plot of id1 and id2')

def plot_array(trajectories: list):
    """绘制多条轨迹

    Args:
        trajectories (list): 二位轨迹数组的列表
    """
    for coordinates in trajectories:
        x_values, y_values = zip(*coordinates)
        # 使用matplotlib绘制散点图
        plt.scatter(x_values, y_values,s=1)
        # 可选：添加标题和轴标签
    plt.title('Scatter Plot of Coordinates')
    plt.xlabel('X Axis')
    plt.ylabel('Y Axis')

def smooth_function(df,col_name,smooth_part):
    """对重合区域的轨迹使用三次样条插值平滑
    Args:
        df (_type_): _description_
        col_name (_type_): _description_
        smooth_part (_type_): _description_
    Returns:
        df : _description_
    """
    #根据标志列和比例进行置空
    flag_1_indices = df.index[df['flag'] == 1]
    num_rows_to_blank = int(smooth_part * len(flag_1_indices))
    for index in flag_1_indices[:num_rows_to_blank].union(flag_1_indices[-num_rows_to_blank:]):
        df.loc[index, col_name] = None
    for col in col_name:
        x=np.array(df[col])
        time=np.array(df['time'])
        # 找到缺失数据的索引
        missing_indices = np.isnan(df[col])
        # 创建插值函数，使用非缺失部分的数据进行插值
        f = interp1d(time[~missing_indices], x[~missing_indices], kind='cubic')
        # 将缺失部分的值替换回原始数组中
        x[missing_indices] = f(time[missing_indices])
        df[col]=x
    return df