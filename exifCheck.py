import os
from pathlib import Path
from PIL import Image, ExifTags
import sys


def get_exif_data(image_path):
    """获取图片的EXIF数据"""
    try:
        with Image.open(image_path) as img:
            exif_data = img._getexif()

            if not exif_data:
                return None, "没有找到EXIF数据"

            # 将数字标签转换为可读的名称
            readable_exif = {}
            for tag_id, value in exif_data.items():
                tag = ExifTags.TAGS.get(tag_id, tag_id)
                readable_exif[tag] = value

            return readable_exif, None

    except Exception as e:
        return None, f"读取EXIF数据失败: {e}"


def print_exif_summary(exif_data):
    """打印EXIF数据摘要"""
    if not exif_data:
        print("  无EXIF数据")
        return

    # 常见的EXIF标签
    common_tags = {
        "Make": "相机品牌",
        "Model": "相机型号",
        "DateTime": "拍摄时间",
        "DateTimeOriginal": "原始拍摄时间",
        "DateTimeDigitized": "数字化时间",
        "Software": "处理软件",
        "Orientation": "方向",
        "XResolution": "水平分辨率",
        "YResolution": "垂直分辨率",
        "ResolutionUnit": "分辨率单位",
        "ExifImageWidth": "图像宽度",
        "ExifImageHeight": "图像高度",
        "GPSInfo": "GPS信息",
    }

    print("  EXIF信息摘要:")
    found_any = False
    for tag, description in common_tags.items():
        if tag in exif_data:
            found_any = True
            print(f"    {description}: {exif_data[tag]}")

    # 如果有GPS信息，详细显示
    if "GPSInfo" in exif_data:
        found_any = True
        print(f"    GPS信息: {exif_data['GPSInfo']}")

    if not found_any:
        print("    未找到常见的EXIF信息")


def main():
    """主函数 - EXIF信息查看器"""
    print("EXIF信息查看工具")
    print("================")

    if len(sys.argv) > 1:
        folder_path = sys.argv[1]
    else:
        folder_path = input("请输入要检查的图片文件夹路径: ").strip()
        if not folder_path:
            folder_path = "."

    folder = Path(folder_path)
    if not folder.exists():
        print(f"错误: 文件夹不存在: {folder_path}")
        return

    # 支持的图片格式
    image_extensions = {".jpg", ".jpeg", ".png", ".tiff", ".bmp", ".webp"}

    # 收集所有图片文件
    image_files = []
    for file_path in folder.rglob("*"):
        if file_path.suffix.lower() in image_extensions and file_path.is_file():
            image_files.append(file_path)

    if not image_files:
        print(f"在 {folder_path} 中没有找到图片文件")
        return

    print(f"找到 {len(image_files)} 个图片文件")
    print("开始检查EXIF信息...")
    print()

    # 检查每个图片的EXIF信息
    images_with_exif = 0

    for i, image_path in enumerate(image_files):
        print(f"{i+1}. {image_path.name}")

        exif_data, error = get_exif_data(image_path)
        if error:
            print(f"  {error}")
            pass
        else:
            print_exif_summary(exif_data)
            if exif_data:
                images_with_exif += 1

        print()  # 空行分隔

    # 统计信息
    print("=" * 50)
    print(f"检查了 {len(image_files)} 个样本文件")
    print(f"其中 {images_with_exif} 个文件包含EXIF信息")


if __name__ == "__main__":
    main()
