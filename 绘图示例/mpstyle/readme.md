# 1.主题使用方法

## 1.1 常规主题使用

```python
plt.style.use("../themes/rose-pine-matplotlib/themes/rose-pine.mplstyle")   # 导入主题路径
plt.rcParams['font.sans-serif'] = ['SimHei']
# plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
```
中文字体和符号设置（Windows 下需要设置字体，Linux 下需要添加字体文件）。注意需要放在主题设置后面，以覆盖主题的默认字体。

# 2.主题说明（来源）

1. [h4pZ/rose-pine-matplotlib](https://github.com/h4pZ/rose-pine-matplotlib)