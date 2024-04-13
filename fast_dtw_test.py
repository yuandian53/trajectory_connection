from fastdtw import fastdtw
import numpy as np

# 示例用法
trajectory1 = np.array([[1, 2], [2, 3], [3, 4], [4, 5]])
trajectory2 = np.array([[2, 2], [4, 3], [2, 4], [5, 5]])

distance, path = fastdtw(trajectory1, trajectory2)
print("DTW距离:", distance)
print("最佳匹配路径:", path)
