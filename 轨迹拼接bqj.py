import os
import pandas as pd
import numpy as np
from fastdtw import fastdtw
import matplotlib.pyplot as plt
from utils import smooth_function, extract_first_and_last_numbers, read_left_file_id_csv_to_dataframe,plot,plot_array
import warnings
warnings.filterwarnings("ignore")

# ------------------------------------ 常量 ------------------------------------ #
notReservedColumn=['traveled_d', 'avg_speed']

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
    df_left_dict = read_left_file_id_csv_to_dataframe(left_file_id,notReservedColumn)
    
    # 读取right轨迹文件
    df_right_dict = read_left_file_id_csv_to_dataframe(right_file_id,notReservedColumn)

    # 遍历left轨迹文件

    output_df=pd.DataFrame()
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
                track1=group
                # ---------------------------------- 得到重叠区域 ---------------------------------- #
                #left_region的x值小于right_region
                leftPoint=track2["x"].min()
                rightPoint=track1["x"].max()
                # # 取出重叠区域(第1种方法)
                # # 计算与给定值最接近的一行的索引
                # leftNearestIndex = (group['x'] - leftPoint).abs().idxmin()
                # leftOverlapArea= group.loc[leftNearestIndex:]
                # rightNearestIndex = (track2['x'] - rightPoint).abs().idxmin()
                # rightOverlapArea = track2.loc[:rightNearestIndex]
                # plot(leftOverlapArea,rightOverlapArea)

                # 取出重叠区域后使用dtw匹配(第2种方法)
                leftNearestIndex = (track1['x'] - leftPoint).abs().idxmin()
                leftOverlapArea= track1.loc[leftNearestIndex:]
                leftRemain = track1.loc[:leftNearestIndex]
                rightNearestIndex = (track2['x'] - rightPoint).abs().idxmin()
                rightOverlapArea = track2.loc[:rightNearestIndex]
                rightRemain = track2.loc[rightNearestIndex:]

                trajectory_left = np.array(leftOverlapArea[['x', 'y']].values.tolist()) 
                trajectory_right = np.array(rightOverlapArea[['x', 'y']].values.tolist())

                distance, path = fastdtw(trajectory_left, trajectory_right)
                # print("DTW距离:", distance)
                # print("最佳匹配路径:", path)
                #填充较短的序列
                trajectory_shorter = leftOverlapArea if len(trajectory_left)<=len(trajectory_right) else rightOverlapArea
                trajectory_longer = leftOverlapArea if len(trajectory_left)>len(trajectory_right) else rightOverlapArea
                shorter_path_list = [element[0] for element in path] if len(trajectory_left)<=len(trajectory_right) else [element[1] for element in path]
                trajectory_shorter_filled=trajectory_shorter.iloc[shorter_path_list].reset_index()
                longer_path_list = [element[0] for element in path] if len(trajectory_left)>len(trajectory_right) else [element[1] for element in path]
                trajectory_longer_filled=trajectory_longer.iloc[longer_path_list].reset_index()
                
                trajectory_merged=pd.DataFrame()
                #计算均值
                for col in trajectory_longer_filled.columns:
                    col_type = type(trajectory_longer_filled[col].iloc[0])
                    if col_type == str:
                        trajectory_merged[col]=trajectory_shorter_filled[col]
                    else:
                        trajectory_merged[col]=(trajectory_shorter_filled[col]+trajectory_longer_filled[col])/2

                # -------------------------------- 对衔接段进行拟合平滑 -------------------------------- #
                #创建flag，标志数据的来源
                leftRemain['flag'] = 0
                trajectory_merged['flag'] = 1
                rightRemain['flag'] = 2

                #生成合成的完整轨迹,重构时间列
                last_time_left = leftRemain['time'].iloc[-1]
                time_increment = 0.04
                merged_df = pd.concat([trajectory_merged, rightRemain], ignore_index=True)
                new_times = np.arange(last_time_left + time_increment, last_time_left + len(merged_df) * time_increment + time_increment, time_increment)
                merged_df['time'] = new_times[:len(merged_df)]

                trajectory=pd.concat([leftRemain,merged_df], ignore_index=True)
                trajectory_smooth=smooth_function(trajectory,['x','y'],0.1)
                #绘图可视化
                plot_array([trajectory_smooth[['x','y']].values.tolist(),leftOverlapArea[['x','y']].values.tolist(),rightOverlapArea[['x','y']].values.tolist()])
                direction=group['direction'].unique(), track2['direction'].unique()
                plt.savefig(f'fig/plot{id1}_{id2}_direction{direction}.png')
                plt.close()
                output_df=pd.concat([output_df,trajectory_smooth])
    output_df.to_csv(f"output\{left_file_id}-{right_file_id}.csv")
                
                # #第三种算法：dtw寻找最佳匹配
                # trajectory_left = np.array(group[['x', 'y']].values.tolist())
                # trajectory_right = np.array(track2[['x', 'y']].values.tolist())
                # distance, path = fastdtw(trajectory_left, trajectory_right)
                # print("DTW距离:", distance)
                # print("最佳匹配路径:", path)


    print(0)
