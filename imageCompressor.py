import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
from PIL import Image
import logging


def setup_logging():
    """设置日志记录"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("imageCompressor.log", encoding="utf-8"),
            # logging.StreamHandler(sys.stdout),
        ],
    )


def get_image_files(folder_path, days=7):
    """获取文件夹中的所有图片文件"""
    image_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"}
    image_files = []
    file_count = 0

    try:
        folder = Path(folder_path)
        if not folder.exists():
            logging.error(f"文件夹不存在: {folder_path}")
            return []

        for file_path in folder.rglob("*"):
            if file_path.suffix.lower() in image_extensions and file_path.is_file():
                if is_old_image(file_path, days):
                    image_files.append(file_path)
                file_count += 1

        if not len(image_files):
            logging.info(f"找到 {file_count} 个图片文件，其中没有过期文件")
            print(f"找到 {file_count} 个图片文件，其中没有过期文件")
            return []
        info = f"找到 {file_count} 个图片文件，其中过期{len(image_files)}个"
        logging.info(info)
        print(info)
        return image_files

    except Exception as e:
        logging.error(f"扫描文件夹时出错: {e}")
        return []


def is_old_image(file_path, days=7):
    """检查图片是否超过指定天数"""
    try:
        # 获取文件的修改时间
        mtime = file_path.stat().st_mtime
        file_date = datetime.fromtimestamp(mtime)
        cutoff_date = datetime.now() - timedelta(days=days)

        return file_date < cutoff_date

    except Exception as e:
        logging.error(f"检查文件时间失败 {file_path}: {e}")
        return False


def compress_image(input_path, output_path, quality=65):
    """压缩图片并保存，正确处理不同图像模式"""
    try:
        with Image.open(input_path) as img:
            # 根据图像模式和格式决定如何处理
            if img.mode in ("RGBA", "LA") or (
                img.mode == "P" and "transparency" in img.info
            ):
                # 带有透明度的图像
                if img.format == "PNG" or output_path.suffix.lower() in (
                    ".png",
                    ".webp",
                ):
                    # 保持PNG或WebP格式以保留透明度
                    img.save(output_path, "PNG", optimize=True)
                else:
                    # 转换为JPEG时需要移除透明度
                    background = Image.new("RGB", img.size, (255, 255, 255))
                    if img.mode in ("RGBA", "LA"):
                        # 合并RGBA图像到白色背景
                        background.paste(img, mask=img.split()[-1])
                    else:
                        # 对于调色板模式
                        background.paste(
                            img,
                            mask=img.getchannel("A") if "A" in img.getbands() else None,
                        )
                    img = background
                    img.save(output_path, "JPEG", quality=quality, optimize=True)
            elif img.mode != "RGB":
                # 其他非RGB模式转换为RGB
                img = img.convert("RGB")
                img.save(output_path, "JPEG", quality=quality, optimize=True)
            else:
                # 已经是RGB模式，直接保存
                if img.format == "PNG" or output_path.suffix.lower() == ".png":
                    img.save(output_path, "PNG", optimize=True)
                else:
                    img.save(output_path, "JPEG", quality=quality, optimize=True)

        return True

    except Exception as e:
        logging.error(f"压缩图片失败 {input_path}: {e}")
        return False


def get_file_size(file_path):
    """获取文件大小（MB）"""
    return file_path.stat().st_size / (1024 * 1024)


def process_old_images(folder_path, days=7, quality=65, backup=True):
    """处理旧图片文件"""
    processed_count = 0
    total_saved = 0
    old_images = get_image_files(folder_path, days)
    total = len(old_images)
    if not total:
        return
    for i, image_path in enumerate(old_images):
        try:
            original_size = get_file_size(image_path)

            if backup:
                # 创建备份文件
                backup_path = image_path.with_suffix(".bak" + image_path.suffix)
                image_path.rename(backup_path)
                input_file = backup_path
            else:
                input_file = image_path

            # 临时输出文件
            temp_output = image_path.with_suffix(".temp" + image_path.suffix)

            # 压缩图片
            if compress_image(input_file, temp_output, quality):
                compressed_size = get_file_size(temp_output)

                # 检查压缩效果
                if compressed_size < original_size:
                    # 删除原文件或备份文件
                    if backup:
                        input_file.unlink()
                    else:
                        image_path.unlink()

                    # 重命名临时文件为原文件名
                    temp_output.rename(image_path)

                    saved = original_size - compressed_size
                    total_saved += saved
                    processed_count += 1

                    progress = (i + 1) / total * 100
                    print(
                        f"\r处理进度: {i+1}/{total} ({progress:.1f}%)",
                        end="",
                        flush=True,
                    )

                    logging.info(
                        f"压缩成功: {image_path.name} "
                        f"({original_size:.2f}MB -> {compressed_size:.2f}MB, "
                        f"节省: {saved:.2f}MB)"
                    )
                else:
                    # 压缩后文件更大，保留原文件
                    temp_output.unlink()
                    if backup:
                        input_file.rename(image_path)
                    logging.warning(f"压缩无效，保留原文件: {image_path.name}")

            else:
                # 压缩失败，恢复备份
                if backup:
                    input_file.rename(image_path)
                logging.error(f"压缩失败: {image_path.name}")

        except Exception as e:
            logging.error(f"处理文件失败 {image_path}: {e}")
            # 恢复备份文件
            if backup and "backup_path" in locals() and backup_path.exists():
                backup_path.rename(image_path)

    print()  # 换行
    logging.info(
        f"处理完成: 共处理 {processed_count} 个文件，节省 {total_saved:.2f} MB"
    )
    print(f"处理完成: 共处理 {processed_count} 个文件，节省 {total_saved:.2f} MB")


def main():
    """主函数"""
    setup_logging()

    if len(sys.argv) < 2:
        print("图片压缩工具")
        print("=============")

        folder_path = input("请输入指定目录（默认当前目录）: ").strip()
        if not folder_path:
            folder_path = "."

        days_input = input("请输入过期天数（默认7天）: ").strip()
        days = int(days_input) if days_input else 7

        quality_input = input("请输入压缩质量10-100（默认65%）: ").strip()
        quality = int(quality_input) if quality_input else 65
    else:
        folder_path = sys.argv[1]
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
        quality = int(sys.argv[3]) if len(sys.argv) > 3 else 65

    # 验证输入
    if not os.path.exists(folder_path):
        print(f"错误: 指定的文件夹不存在: {folder_path}")
        logging.error(f"指定的文件夹不存在: {folder_path}")
        sys.exit(1)

    if quality < 10 or quality > 100:
        print("错误: 质量参数应在10-100之间")
        logging.error("质量参数应在10-100之间")
        sys.exit(1)

    print(f"\n开始处理文件夹: {folder_path}")
    print(f"设置: 天数={days}, 质量={quality}")
    print("正在扫描和压缩图片...")
    logging.info(f"开始处理文件夹: {folder_path}, 天数={days}, 质量={quality}")

    process_old_images(folder_path, days, quality, backup=True)


if __name__ == "__main__":
    main()
