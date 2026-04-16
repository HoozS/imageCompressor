# 过期图片压缩工具

## 功能说明

- 扫描指定文件夹及其子文件夹中的所有图片文件
- 检测修改日期在指定天数之前的图片
- 对符合条件的图片进行压缩以节省空间
- 自动处理不同格式的图片（JPG、PNG、BMP等）
- 保留原始文件的备份（.bak后缀）
- 详细日志记录在 imageCompressor.log 文件中

## 支持的图片格式

- JPG
- JPEG
- PNG
- BMP
- TIFF
- WebP

## 使用说明

### 环境配置

可以使用虚拟环境

```shell
python -m venv env      # 创建虚拟环境，名为env
env\Scripts\activate    # 激活虚拟环境
```

安装依赖

```shell
pip -r requirements.txt
```

### 命令行使用

```shell
python imageCompressor.py <文件夹路径> [天数] [质量]
```

示例:

```shell
python imageCompressor.py "C:\\Photos"          # 使用默认设置
python imageCompressor.py "C:\\Photos" 14 75    # 14天前，质量75%
```

### 交互式使用

直接运行脚本，然后按照提示输入

- 目录路径 (默认当前目录)
- 过期天数 (默认7天)
- 压缩质量 (默认65%)

示例：

```shell
python imageCompressor.py

图片压缩工具
=============
请输入指定目录（默认当前目录）:
请输入过期天数（默认7天）:
请输入压缩质量10-100（默认65%）:
```

## Exif检查工具

可交换图像文件格式（英语：Exchangeable image file format，官方简称Exif），是专门为数码相机的照片设定的，可以记录数码照片的属性信息和拍摄数据。

用于检查图片中是否携带该数据，一般来说会照片都会携带该数据，对于“过期”图片而言该数据并不重要，在压缩过程中会首先去除该数据。`exifCheck.py`脚本旨在检查是否存在Exif数据。

## 额外建议

pip标准源通常会有下载慢的问题，可以在下载时添加`-i {下载源}`的方式临时换源，也可以`pip config set global.index-url {下载源}`的方式设定永久换源

```shell
# 临时换源
pip install -r requirements.txt -i https://pypi.mirrors.ustc.edu.cn/simple/
```

```shell
# 永久换源
pip config set global.index-url https://pypi.mirrors.ustc.edu.cn/simple/
pip install -r requirements.txt
```

```text
常见源：
清华源：https://pypi.tuna.tsinghua.edu.cn/simple
阿里源：https://mirrors.aliyun.com/pypi/simple/
豆瓣源：http://pypi.douban.com/simple/
中科大源：https://pypi.mirrors.ustc.edu.cn/simple/
```
