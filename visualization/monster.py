import matplotlib.pyplot as plt
from matplotlib.patches import Arc

# 创建一个绘图窗口
fig, ax = plt.subplots()

# 绘制怪兽身体（圆形）
body = plt.Circle((0.5, 0.5), 0.3, color='green', fill=True)
ax.add_artist(body)

# 绘制怪兽的左眼
left_eye = plt.Circle((0.4, 0.6), 0.05, color='white', fill=True)
ax.add_artist(left_eye)

# 绘制怪兽的右眼
right_eye = plt.Circle((0.6, 0.6), 0.05, color='white', fill=True)
ax.add_artist(right_eye)

# 绘制怪兽的嘴巴（弧形）
mouth = Arc((0.5, 0.4), 0.2, 0.1, theta1=0, theta2=180, color='black')
ax.add_artist(mouth)

# 设置绘图区的范围
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

# 移除坐标轴
ax.set_xticks([])
ax.set_yticks([])

# 显示图像
plt.show()