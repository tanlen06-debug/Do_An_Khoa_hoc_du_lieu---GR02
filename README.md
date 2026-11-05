# Đồ án thực tế Khoa học dữ liệu – Nhóm 02

**Tên đăng ký:** Phân tích dữ liệu đơn hàng và dự đoán nguy cơ giao hàng trễ trong thương mại điện tử.

**Bộ dữ liệu nghiên cứu:** [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) (Brazil, 2016–2018). **Hạn hoàn tất nội bộ: 30/11/2026.**

> Trạng thái: cấu trúc khởi tạo; chưa có dữ liệu tải về, mô hình đã huấn luyện, kết quả thực nghiệm hoặc dự báo sản xuất. Không trình bày ví dụ chưa kiểm chứng thành kết quả đồ án.

## Phân công theo đề cương đã chốt

| Thành viên | Chương | Phạm vi |
|---|---|---|
| **Tấn Lên (nhóm trưởng)** | 1, 6, phụ lục | Phát biểu bài toán, Dashboard Streamlit, kết luận, tích hợp và bảo vệ |
| **Ngọc Lan** | 2 | Logistics, EDA, Random Forest, MLP, độ đo, nghiên cứu liên quan |
| **Lam Linh** | 3 | Nguồn dữ liệu, ghép 9 CSV, nhãn, EDA, kiểm toán rò rỉ dữ liệu |
| **Trúc Chi** | 4 | Chia theo thời gian, pipeline, Dummy, Random Forest, MLP, chọn ngưỡng |
| **Vĩnh Chi** | 5 | Test metrics, PR curve, phân tích lỗi, đánh giá Top-K, hạn chế |

Đề cương: **6 chương / 26 tiểu mục + 1 phụ lục (27 hạng mục)**. Xem [đề cương chi tiết](docs/REPORT_OUTLINE.md) và [kế hoạch giao việc](docs/PLAN_NOV2026.md).

[Bảng Google Sheets quản lý nhóm](https://docs.google.com/spreadsheets/d/1bbsNPpLUnJDNtUY-1TLw942ftK-fQfL8t-_j4jZkywY/edit) là nơi cập nhật tiến độ; GitHub lưu code, tài liệu kỹ thuật, Issues và Pull Requests.

## Sơ đồ thư mục

```text
Do_An_Khoa_hoc_du_lieu---GR02/
├── .github/                  # Template cho Issue và Pull Request
├── app/                      # Streamlit: Chương 6
├── config/                   # Quy ước cấu hình môi trường
├── data/
│   ├── raw/                  # 9 CSV Olist (không push)
│   └── processed/            # Dataset 1 hàng/order_id (không push)
├── docs/                     # Quy ước, hợp đồng dữ liệu, kế hoạch, đề cương
├── models/                   # Model artifacts, tài liệu (model nhị phân không push)
├── notebooks/
│   ├── 01_data_audit.ipynb
│   ├── 02_prepare_orders.ipynb
│   ├── 03_eda.ipynb
│   ├── 04_train_models.ipynb
│   └── 05_evaluate_models.ipynb
├── reports/
│   ├── chapters/             # Chương 1–6, phụ lục
│   ├── figures/              # Hình báo cáo có thể tái lập
│   └── tables/               # Bảng báo cáo có thể tái lập
├── src/                      # Hàm dùng chung, test được
├── tests/                    # Kiểm tra nhãn và khóa order_id
├── .gitignore
├── requirements.txt
└── README.md
```

## Bắt đầu làm việc

```bash
git clone https://github.com/tanlen06-debug/Do_An_Khoa_hoc_du_lieu---GR02.git
cd Do_An_Khoa_hoc_du_lieu---GR02
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest -q
streamlit run app/app.py
```

Tải 9 tệp CSV từ Kaggle vào `data/raw/` theo [hướng dẫn dữ liệu](data/README.md). Notebook hiện là **khung hướng dẫn**; cần triển khai code, kiểm tra và thay thế phần TODO bằng kết quả chạy thực tế.

## Nguyên tắc thống nhất (không được đổi tùy ý)

1. **Thời điểm dự báo:** `order_approved_at` (đề xuất đã dùng trong kế hoạch), chỉ dùng đặc trưng thực sự có ở thời điểm này.
2. **Nhãn:** `is_late=1` khi **ngày** giao thực tế > **ngày** giao dự kiến; sử dụng ngày giao thực tế để tạo nhãn, **không dùng làm đầu vào**.
3. **Đơn vị quan sát:** một `order_id` = một dòng ở bảng cuối. Kiểm tra join one-to-many và dòng trùng.
4. **Thiết kế đánh giá:** Train/Validation/Test theo thời gian. Fit preprocessing chỉ trên Train, chọn tham số/ngưỡng ở Validation, Test để đánh giá cuối.
5. **Mô hình:** Dummy (baseline tham chiếu), Random Forest (ML) và MLP (DL); kết quả được đánh giá bằng Precision, Recall, F1, Average Precision (AP), cảnh báo sai và Top-K.
6. **Giới hạn:** huấn luyện trên các đơn đã giao có nhãn; dữ liệu Brazil 2016–2018 không đại diện tự động cho thị trường Việt Nam 2026.

Đọc [DATA_CONTRACT](docs/DATA_CONTRACT.md), [EXPERIMENT_PROTOCOL](docs/EXPERIMENT_PROTOCOL.md), [TEAM_WORKFLOW](docs/TEAM_WORKFLOW.md) **trước khi code**.

## Giao việc và kiểm tra

- Thành viên làm trên nhánh cá nhân/chương, tạo Pull Request (PR) vào `main`, có bằng chứng chạy và người review.
- **Không push trực tiếp vào `main`**, không force-push, không commit CSV gốc/đã xử lý, token, môi trường ảo hoặc model lớn.
- `main` chứa phiên bản đã review; GitHub Issues dùng theo dõi công việc, Google Sheets theo dõi mốc nội bộ.
- Lộ trình bàn giao: **Lam Linh → Trúc Chi → Vĩnh Chi → Tấn Lên**; Ngọc Lan viết lý thuyết song song và đối chiếu cách cài đặt.

**Chú ý:** Tài khoản GitHub của Ngọc Lan, Lam Linh, Trúc Chi và Vĩnh Chi chưa được xác minh; chỉ gán assignee khi biết đúng username và đã có quyền truy cập repository.
