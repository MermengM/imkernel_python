from Demo.Algo.cimsh.main import make_molded
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

result = make_molded(Z_height=100)

# 提取 x, y, z 坐标
x = [point['x'] for point in result]
y = [point['y'] for point in result]
z = [point['z'] for point in result]

# 创建 3D 图形
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# 绘制 3D 散点图
scatter = ax.scatter(x, y, z, c=z, cmap='viridis')

# 添加颜色条
plt.colorbar(scatter)

# 设置坐标轴标签
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# 设置标题
plt.title('3D Blade Coordinates')

# 显示图形
plt.show()
