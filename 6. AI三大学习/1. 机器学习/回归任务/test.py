import sys, argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap
# 定义两种颜色，紫色和黄色，用于后面显示元胞状态
yeah = ("purple", "yellow")
# 创建一个颜色映射对象，让元胞的不同状态对应不同颜色
cmap = ListedColormap(yeah)

# 定义元胞的两种状态，ON 代表开启状态，用 255 表示
ON = 255
# OFF 代表关闭状态，用 0 表示
OFF = 0
# 把两种状态存到一个列表里
vals = [ON, OFF]
# 这个函数用来创建一个随机的 N x N 的元胞网格
# 每个元胞有 20% 的概率是 ON 状态，80% 的概率是 OFF 状态
def randomGrid(N):
    # 从 vals 列表里随机选 N*N 个元素，按照给定的概率选择
    # 然后把这些元素重新排列成一个 N x N 的二维数组
    return np.random.choice(vals, N*N, p=[0.2, 0.8]).reshape(N, N)

# 这个函数用来在网格里添加一个滑翔机图案
# 滑翔机是一种特殊的元胞组合，会在网格里移动
def addGlider(i, j, grid):
    # 定义滑翔机的图案，用一个 3 x 3 的二维数组表示
    glider = np.array([[0, 0, 255], [255, 0, 255], [0, 255, 255]])
    # 把滑翔机图案放到网格的指定位置
    grid[i:i+3, j:j+3] = glider

# 这个函数用来更新每一个时间步的元胞状态
def update(frameNum, img, grid, N):
    # 复制当前的网格状态，这样在更新时不会影响原来的网格
    newGrid = grid.copy()
    # 遍历网格里的每一个元胞
    for i in range(N):
        for j in range(N):
            # 计算当前元胞周围 8 个元胞的状态总和
            # 这里用 %N 是为了处理边界情况，让网格变成环形
            total = int((grid[i, (j-1)%N] + grid[i, (j+1)%N] +
                         grid[(i-1)%N, j] + grid[(i+1)%N, j] +
                         grid[(i-1)%N, (j-1)%N] + grid[(i-1)%N, (j+1)%N] +
                         grid[(i+1)%N, (j-1)%N] + grid[(i+1)%N, (j+1)%N]) / 255)
            # 如果当前元胞是 ON 状态
            if grid[i, j] == ON:
                # 如果周围元胞数量小于 2 或者大于 3
                if (total < 2) or (total > 3):
                    # 把这个元胞变成 OFF 状态
                    newGrid[i, j] = OFF
            # 如果当前元胞是 OFF 状态
            else:
                # 如果周围元胞数量等于 3
                if total == 3:
                    # 把这个元胞变成 ON 状态
                    newGrid[i, j] = ON
    # 更新图像的数据，显示新的网格状态
    img.set_data(newGrid)
    # 把新的网格状态赋值给原来的网格
    grid[:] = newGrid[:]
    # 返回更新后的图像
    return img,

# 主函数，程序的入口
def main():
    # 创建一个命令行参数解析器
    parser = argparse.ArgumentParser(description="Runs Conway's Game of Life simulation.")
    # 添加一些命令行参数
    parser.add_argument('--grid-size', dest='N', required=False)
    parser.add_argument('--mov-file', dest='movfile', required=False)
    parser.add_argument('--interval', dest='interval', required=False)
    parser.add_argument('--glider', action='store_true', required=False)
    parser.add_argument('--gosper', action='store_true', required=False)
    # 解析命令行参数
    args = parser.parse_args()

    # 网格的默认大小是 100 x 100
    N = 100
    # 如果用户指定了网格大小，并且大小大于 8
    if args.N and int(args.N) > 8:
        # 就用用户指定的大小
        N = int(args.N)

    # 每次更新的时间间隔，默认是 50 毫秒
    updateInterval = 50
    # 如果用户指定了时间间隔
    if args.interval:
        # 就用用户指定的时间间隔
        updateInterval = int(args.interval)

    # 创建一个空的数组来表示网格
    grid = np.array([])

    # 如果用户选择添加滑翔机图案
    if args.glider:
        # 创建一个全是 0 的 N x N 网格
        grid = np.zeros(N*N).reshape(N, N)
        # 在网格的 (1, 1) 位置添加滑翔机图案
        addGlider(1, 1, grid)
    else:
        # 否则，创建一个随机的网格
        grid = randomGrid(N)

    # 创建一个图形窗口，背景颜色是粉色
    fig, ax = plt.subplots(facecolor='pink')
    # 在图形窗口里显示网格，使用之前定义的颜色映射
    img = ax.imshow(grid, cmap=cmap, interpolation='nearest')

    # 创建一个动画对象，每隔一段时间调用 update 函数更新网格状态
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N,),
                                  frames=10, interval=updateInterval, save_count=50)

    # 如果用户指定了要保存动画文件
    if args.movfile:
        # 把动画保存为指定的文件，帧率是 30
        ani.save(args.movfile, fps=30, extra_args=['-vcodec', 'libx264'])

    # 显示图形窗口
    plt.show()

# 调用主函数，开始程序
main()