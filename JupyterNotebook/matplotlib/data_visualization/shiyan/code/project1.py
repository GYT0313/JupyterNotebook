import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

# 读取数据
data = pd.read_csv('./barley2.csv')
# 设置中文显示
plt.rcParams['font.sans-serif'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False

# 取出试验点名、种类名
sites = data.Site.unique()
varieties = data.Variety.unique()

def mkdir():
    """创建保存图片的目录"""
    path = os.path.abspath(os.curdir) + '\\pictures_png'
    if os.path.exists(path) == False:
        os.mkdir(path)
    # 创建雷达图目录
    path = os.path.abspath(os.curdir) + '\\pictures_png\\radar'
    if os.path.exists(path) == False:
        os.mkdir(path)


def save_picture(plt, picture_name, title=None, xlabel=None, ylabel=None):
    """保存图片函数"""
    path = "./pictures_png/"
    plt.title(title)
    if xlabel:
        plt.xlabel(xlabel)
    if ylabel:
        plt.ylabel(ylabel)
    plt.tight_layout()  # 避免图片保存不完整
    plt.savefig(path + picture_name, dpi=120)
    plt.show()


def mean_std():
    """计算各种类平均值、总体平均值、各种类标准差"""
    # 种类平均值
    varieties_mean = data.groupby('Variety')['Yield'].mean()
    # 总体均值
    all_mean = data.Yield.mean()
    # 标准差
    varieties_standard_deviation = data.groupby('Variety')['Yield'].std()

    fig,ax1 = plt.subplots()
    # 均值
    plt.plot(varieties, [all_mean for i in range(len(varieties))])

    # 种类均值
    plt.bar(varieties, varieties_mean, facecolor='yellowgreen', width=0.5)
    plt.grid(axis='y')
    plt.xticks(rotation=40)
    plt.xlabel("Variety")
    plt.ylabel("Yield")
    plt.yticks(range(0,50,5))

    # 标准差
    ax2 = ax1.twinx()
    plt.plot(varieties, varieties_standard_deviation,'.-', lw=2, color='r')
    plt.yticks(range(7,15))
    plt.legend('标准差', loc = 'best')
    plt.yticks(range(0,15))
    save_picture(plt, "整体分析.png", title="各类别产量均值、总体均值和标准差")
    

def analysis_by_site():
    """按地区分析"""
    fig, axes = plt.subplots(2,1)

    # 按地区绘制总产量
    data.groupby(['Site'])['Yield'] \
        .sum() \
        .sort_values() \
        .plot(kind='barh', figsize=(8,4), ax=axes[0])

    # 按地区、年份绘制总产量
    data.groupby(['Year', 'Site'])['Yield'] \
        .sum() \
        .sort_values() \
        .plot(kind='barh', figsize=(8,8), ax=axes[1])
    save_picture(plt, "各实验站每年总产量.png", xlabel="Yield")


def analysis_by_variety():
    """按大麦类别"""
    # 按大麦种类
    data.groupby('Variety')['Yield'] \
        .sum() \
        .sort_values() \
        .plot(kind='barh', figsize=(8,4))
    save_picture(plt, "各种类大麦总产量.png", title="各种类大麦总产量", xlabel="Yield")

def analysis_by_year():
    """按年份"""
    data.groupby( 'Year')['Yield'] \
        .sum() \
        .plot(kind='bar', figsize=(3,3))
    save_picture(plt, "各年份总产量.png", title="各年份总产量", xlabel="Year", ylabel="Yield")


def analysis_by_site_and_variety():
    """按地区和大麦种类"""
    fig, axes = plt.subplots(2,1)
    data.groupby(['Site','Variety'])['Yield'] \
        .sum() \
        .sort_values(ascending=False) \
        .head(10) \
        .sort_values() \
        .plot(kind='barh', figsize=(8,6), ax=axes[0])

    data.groupby(['Site','Variety'])['Yield'] \
        .sum() \
        .sort_values() \
        .head(10) \
        .sort_values() \
        .plot(kind='barh', figsize=(8,6), ax=axes[1])
    plt.xticks(range(0,121,20))
    save_picture(plt, "产量最高和产量最低的10个地区产量.png", xlabel="Yield")


def radar_for_site():
    """绘制各个地区关于每个大麦种类产量的雷达图"""
    # 分组求和
    data_series = data.groupby(['Site','Variety', 'Year'])['Yield'].sum()

    labels = np.array(varieties) # 标签
    labels_length = len(labels)  # 数据长度

    # 雷达图绘制
    def radar_chart(data1, data2, i):
        # 1931年
        data_radar1 = np.array(data1) # 数据
        angles1 = np.linspace(0, 2*np.pi, labels_length, endpoint=False)  # 分割圆周长
        data_radar1 = np.concatenate((data_radar1, [data_radar1[0]]))  # 闭合
        angles1 = np.concatenate((angles1, [angles1[0]]))  # 闭合
        # 1932年
        data_radar2 = np.array(data2) # 数据
        angles2 = np.linspace(0, 2*np.pi, labels_length, endpoint=False)  # 分割圆周长
        data_radar2 = np.concatenate((data_radar2, [data_radar2[0]]))  # 闭合
        angles2 = np.concatenate((angles2, [angles2[0]]))  # 闭合
        # 做极坐标系1931
        plt.polar(angles1, data_radar1, 'bo-', linewidth=1)
        # 做极坐标系1932
        plt.polar(angles2, data_radar2, 'go-', linewidth=1)
        # 填充1931
        plt.fill(angles1, data_radar1, facecolor='r', alpha=0.7)#
        # 填充1932
        plt.fill(angles2, data_radar2, facecolor='y', alpha=0.7)
        plt.thetagrids(angles1 * 180/np.pi, labels)  # 做标签
        plt.ylim(0, 71)
        plt.legend(['1931', '1932'])
        # 保存图片
        name = "radar/"+sites[i]+".png"
        save_picture(plt, name, title=sites[i])

    # 遍历绘制6个实验站
    for i in range(len(sites)):
        # 数据共120行，如前20行中1931年为偶数，1932年为奇数
        # 1931
        data1 = data_series[i*2*10 : (i*2+2)*10 : 2]
        # 1932
        data2 = data_series[i*2*10 + 1 : (i*2+2)*10 : 2]
        radar_chart(data1, data2, i)


def quarter_by_site():
    """计算各地区产量的四分位数，划分级别"""
    sort_data = data.groupby(['Site','Variety'])['Yield'].sum()

    for i in range(len(sites)):
        print('='*40)
        pd.set_option('precision', 2) # 保留2位小数
        # 获取数据
        site_data = sort_data[i*10:(i+1)*10].sort_values()
        # 四分位数
        upper_quarter = np.percentile(site_data, 75)
        lower_quarter = np.percentile(site_data, 25)
        # 打印
        print(site_data)
        print("\nquarter-75: {}, quarter-25: {}\n".format(upper_quarter, lower_quarter))
        # 极值标准化
        data_min = site_data.min()
        data_max = site_data.max()
        print("data standardization: ")
        print(((site_data-data_min) / (data_max-data_min)).sort_values())
        print('='*40)


def main():
    mkdir()
    mean_std()
    analysis_by_site()
    analysis_by_variety()
    analysis_by_year()
    analysis_by_site_and_variety()
    radar_for_site()
    quarter_by_site()


if __name__ == '__main__':
  main()