import os
import shutil
from pathlib import Path
from tqdm import tqdm
from collections import defaultdict
import filetype

# ==============================
# CONFIG
# ==============================
SOURCE_DIR = "/home/admin/Downloads/D01"  # thư mục gốc chứa dữ liệu
DEST_DIR = "/home/admin/Downloads/D02"  # nơi lưu file phân loại
MOVE_FILES = False  # True = di chuyển, False = sao chép

# Định nghĩa loại file dựa trên MIME type
# Có thể thêm các MIME type khác nếu cần
MIME_CATEGORIES = {
    "images": ["image/jpeg", "image/png", "image/gif", "image/bmp", "image/tiff", "image/webp", "image/svg+xml"],
    "videos": ["video/mp4", "video/x-matroska", "video/x-msvideo", "video/quicktime", "video/x-flv", "video/x-ms-wmv"],
    "audios": ["audio/mpeg", "audio/wav", "audio/flac", "audio/aac", "audio/x-m4a", "audio/ogg"],
    "documents": ["application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "text/plain", "application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.ms-powerpoint", "application/vnd.openxmlformats-officedocument.presentationml.presentation", "text/csv"],
    "archives": ["application/zip", "application/x-rar-compressed", "application/x-7z-compressed", "application/x-tar", "application/gzip"],
}

def get_category_by_mime(filepath):
    """
    Xác định danh mục file dựa trên MIME type.
    """
    try:
        kind = filetype.guess(filepath)
        if kind:
            mime_type = kind.mime
            for cat, mime_list in MIME_CATEGORIES.items():
                if mime_type in mime_list:
                    return cat
    except Exception as e:
        print(f"Lỗi khi xác định MIME type cho {filepath}: {e}")

    # Trở lại phương pháp cũ nếu không xác định được MIME type
    ext = filepath.suffix.lower()
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat
    return "others"

# Định nghĩa loại file bằng đuôi file (dùng cho trường hợp dự phòng)
CATEGORIES = {
    "images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp", ".svg"],
    "videos": [".mp4", ".mkv", ".avi", ".mov", ".flv", ".wmv"],
    "audios": [".mp3", ".wav", ".flac", ".aac", ".m4a", ".ogg"],
    "documents": [".pdf", ".doc", ".docx", ".txt", ".xlsx", ".xls", ".ppt", ".pptx", ".csv"],
    "archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
}

# ==============================
# THỰC HIỆN
# ==============================
source = Path(SOURCE_DIR)
dest = Path(DEST_DIR)
dest.mkdir(parents=True, exist_ok=True)

# Lấy toàn bộ file
all_files = [f for f in source.rglob("*") if f.is_file()]

# Bộ đếm thống kê
stats = defaultdict(int)

# Hiển thị tiến trình với tqdm
for filepath in tqdm(all_files, desc="Đang phân loại", unit="file"):
    category = get_category_by_mime(filepath)
    target_dir = dest / category
    target_dir.mkdir(parents=True, exist_ok=True)

    target_file = target_dir / filepath.name

    # tránh ghi đè -> thêm hậu tố nếu trùng tên
    if target_file.exists():
        base, ext = os.path.splitext(filepath.name)
        i = 1
        while True:
            new_name = f"{base}_{i}{ext}"
            target_file = target_dir / new_name
            if not target_file.exists():
                break
            i += 1

    if MOVE_FILES:
        shutil.move(str(filepath), str(target_file))
    else:
        shutil.copy2(str(filepath), str(target_file))

    # Cập nhật thống kê
    stats[category] += 1

print("\n✅ Hoàn tất phân loại file!")
print("📊 Thống kê kết quả:")
for cat, count in stats.items():
    print(f"  - {cat}: {count} file")
