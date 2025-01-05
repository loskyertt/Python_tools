# 中文字体设置（针对 Linux）

对于 Windows，只需要在代码中添加下面即可：
```python
plt.rcParams['font.sans-serif'] = ['SimHei']
# plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
```

## 方式一：直接引入

```python
import matplotlib.font_manager as fm

font_path = "/home/sky/workspace/temp/py/fonts/SimHei.ttf"  # 设置字体路径
my_font = fm.FontProperties(fname=font_path)

# 手动注册字体
fm.fontManager.addfont(font_path)

# 获取字体名称
font_name = my_font.get_name()
print(f"真实字体名称: {font_name}")

# 设置 Matplotlib 识别该字体
plt.rcParams["font.sans-serif"] = [font_name]
plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题
```

## 方式二：修改配置文件

通过运行下面代码找到字体或主题路径：
```python
import matplotlib

print(matplotlib.matplotlib_fname())   # 查找字体路径
```

会输出类似这样的路径：
```
/home/sky/miniconda3/envs/test/lib/python3.12/site-packages/matplotlib/mpl-data/matplotlibrc
```
这个`matplotlibrc`是配置文件。

把字体文件（比如`SimHei`）放到该目录下：
```
/home/sky/miniconda3/envs/test/lib/python3.12/site-packages/matplotlib/mpl-data/fonts/ttf
```

修改`matplotlib`：
- 原来的：
```txt
#font.serif:      DejaVu Serif, Bitstream Vera Serif, Computer Modern Roman, New Century Schoolbook, Century Schoolbook L, Utopia, ITC Bookman, Bookman, Nimbus Roman No9 L, Times New Roman, Times, Palatino, Charter, serif
#font.sans-serif: DejaVu Sans, Bitstream Vera Sans, Computer Modern Sans Serif, Lucida Grande, Verdana, Geneva, Lucid, Arial, Helvetica, Avant Garde, sans-serif
```

- 修改后的：
```txt
#font.serif:      SimHei, DejaVu Serif, Bitstream Vera Serif, Computer Modern Roman, New Century Schoolbook, Century Schoolbook L, Utopia, ITC Bookman, Bookman, Nimbus Roman No9 L, Times New Roman, Times, Palatino, Charter, serif
#font.sans-serif: SimHei, DejaVu Sans, Bitstream Vera Sans, Computer Modern Sans Serif, Lucida Grande, Verdana, Geneva, Lucid, Arial, Helvetica, Avant Garde, sans-serif
```

然后执行`rm ~/.cache/matplotlib -rf`，删除缓存即可。