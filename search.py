import os
import fnmatch

# ==============================
# HƯỚNG DẪN SỬ DỤNG
# ==============================
# 1. Chạy đoạn code này.
# 2. Nhập đường dẫn thư mục bạn muốn tìm kiếm.
# 3. Nhập từ khóa bạn muốn tìm (ví dụ: "report", "photo", "báo cáo").
# ==============================

def find_file_by_name(directory, keyword):
    """
    Tìm kiếm các file có tên chứa từ khóa trong một thư mục và các thư mục con.

    Args:
        directory (str): Đường dẫn thư mục gốc để tìm kiếm.
        keyword (str): Từ khóa để tìm kiếm trong tên file.

    Returns:
        list: Một danh sách các đường dẫn đầy đủ của các file tìm thấy.
    """
    matching_files = []
    # Dùng os.walk để duyệt qua tất cả các thư mục và file
    for root, _, files in os.walk(directory):
        for filename in files:
            # Kiểm tra xem từ khóa có trong tên file hay không
            if keyword.lower() in filename.lower():
                full_path = os.path.join(root, filename)
                matching_files.append(full_path)
    return matching_files

def main():
    """Chức năng chính để chạy chương trình."""
    # Lấy đường dẫn từ người dùng
    search_directory ="/home/admin/Downloads/D02"
    if not os.path.isdir(search_directory):
        print("Lỗi: Đường dẫn không hợp lệ. Vui lòng thử lại.")
        return

    # Lấy từ khóa từ người dùng
    search_keyword = "IMG20220617122126"

    print(f"\nĐang tìm kiếm file có tên chứa '{search_keyword}' trong '{search_directory}'...")
    
    found_files = find_file_by_name(search_directory, search_keyword)

    if found_files:
        print("\n✅ Đã tìm thấy các file sau:")
        for file_path in found_files:
            print(f"  - {file_path}")
    else:
        print("\n❌ Không tìm thấy file nào phù hợp.")

if __name__ == "__main__":
    main()
