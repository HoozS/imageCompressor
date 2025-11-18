# 图片过期压缩工具

## 使用说明

1. 交互式使用:
    直接运行脚本，然后按照提示输入
    - 目录路径 (默认当前目录)
    - 过期天数 (默认7天)
    - 压缩质量 (默认65%)

2. 命令行使用:

   ```shell
    python imageCompressor.py <文件夹路径> [天数] [质量]
    ```

    示例:

    ```shell
    python imageCompressor.py "C:\\Photos"          # 使用默认设置
    python imageCompressor.py "C:\\Photos" 14 75    # 14天前，质量75%
    ```

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
