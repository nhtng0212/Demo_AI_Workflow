#!/bin/bash

# ==============================================================================
# Tên file: health.sh
# Mục đích: Kiểm tra và báo cáo nhanh trạng thái tài nguyên hệ thống (RAM, Disk).
# ==============================================================================

echo "========================================"
echo "      BÁO CÁO TRẠNG THÁI HỆ THỐNG       "
echo "      Thời gian: $(date "+%Y-%m-%d %H:%M:%S")"
echo "========================================"
echo ""

# 1. Kiểm tra không gian ổ đĩa (Disk Space)
# Lệnh 'df -h' hiển thị dung lượng ổ đĩa. 
# 'grep -vE "^Filesystem|tmpfs|cdrom"' dùng để loại bỏ các dòng không quan trọng.
echo "[1] TRẠNG THÁI Ổ ĐĨA CỨNG (Disk Space):"
df -h | awk 'NR==1 || /^\/dev/' | awk '{printf "  - %-15s: Sử dụng %s trên tổng số %s (Tỷ lệ: %s)\n", $1, $3, $2, $5}'
echo ""

# 2. Kiểm tra bộ nhớ RAM (Memory Usage)
# Lệnh 'free -m' hiển thị RAM theo Megabytes.
echo "[2] TRẠNG THÁI BỘ NHỚ RAM (Memory):"
if command -v free > /dev/null; then
    # Dành cho hệ thống Linux (như Kali, Ubuntu mà bạn hay dùng)
    free -m | awk 'NR==2{printf "  - Tổng cộng: %s MB\n  - Đã dùng  : %s MB\n  - Còn trống: %s MB\n", $2, $3, $4}'
else
    # Dành cho macOS (phòng trường hợp chạy trên máy Mac)
    echo "  - (Chưa hỗ trợ lệnh 'free' trên hệ điều hành này)"
fi
echo ""

# 3. Kiểm tra Tải hệ thống (System Load / Uptime)
# Lệnh 'uptime' hiển thị thời gian máy đã chạy và tải trung bình trong 1, 5, 15 phút qua.
echo "[3] TRẠNG THÁI TẢI HỆ THỐNG (System Load):"
UPTIME_INFO=$(uptime)
echo "  - Chi tiết: $UPTIME_INFO"
echo ""

echo "========================================"
echo "          KẾT THÚC BÁO CÁO              "
echo "========================================"