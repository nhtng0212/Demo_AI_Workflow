# Tài Liệu Demo: Agent Workflow Tự Động Hóa (LangGraph)

## 1. Các Use Cases Demo Hiện Tại (Phase 1)

Đây là các luồng (flows) đã được lập trình và chạy thực tế trong phiên bản hiện tại.

### Use Case 1: Tự động hóa Git Push
*   **Mô tả:** Tự động hóa quy trình đẩy mã nguồn lên kho lưu trữ.
*   **Input (Ví dụ):** 
    *   *"Đẩy code lên git giúp tôi"*
    *   *"Hãy commit và push các thay đổi hiện tại"*
*   **Luồng xử lý (Workflow):**
    1.  `Classifier Node` phân tích NLU và gán nhãn `intent = git_push`.
    2.  `Router` điều hướng luồng sang `GitPush Node`.
    3.  `GitPush Node` gọi file `auto_push.sh` qua `subprocess` (Thực thi chuỗi lệnh: `git add .` -> `git commit -m "Auto-commit: [Timestamp]"` -> `git push origin main`).
*   **Output:** Trả về log terminal chi tiết từ shell script.

### Use Case 2: Báo cáo trạng thái (Health Check)
*   **Mô tả:** Kiểm tra và báo cáo nhanh tình trạng máy chủ (RAM, CPU, Disk space).
*   **Input:** *"Kiểm tra trạng thái server"*
*   **Workflow:** Gán nhãn `health_check` -> Gọi Node chạy file `health.sh` (chạy các lệnh `top`, `df -h`) -> LLM tóm tắt log hệ thống thành ngôn ngữ tự nhiên.

### Use Case 3: Xử lý ngoại lệ (Fallback / Out of Scope)
*   **Mô tả:** Hệ thống từ chối an toàn các yêu cầu không nằm trong phạm vi kịch bản.
*   **Input (Ví dụ):**
    *   *"Hôm nay thời tiết thế nào?"*
    *   *"Tạo cho tôi một file database"*
*   **Luồng xử lý (Workflow):**
    1.  `Classifier Node` phân tích và gán nhãn `intent = unknown`.
    2.  `Router` điều hướng luồng sang `NotSupported Node`.
*   **Output:** Thông báo: *"Xin lỗi, hiện tại tôi chưa có chức năng này."*

## 4. Cách chạy Demo
1. Đảm bảo đã thiết lập biến môi trường `GOOGLE_API_KEY` trong file `.env`.
2. Chạy lệnh: `python3 main.py`
3. Nhập câu lệnh điều khiển tại prompt: `[INPUT] Nhập yêu cầu của bạn:`
