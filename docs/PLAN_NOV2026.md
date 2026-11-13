# Kế hoạch thống nhất – hạn nội bộ 30/11/2026

Thời gian dự kiến bắt đầu từ 04/11/2026. Hạn nội bộ này do nhóm chốt, chưa thay thế lịch giảng viên. Xem [Google Sheets](https://docs.google.com/spreadsheets/d/1bbsNPpLUnJDNtUY-1TLw942ftK-fQfL8t-_j4jZkywY/edit) các tab `04_BAO_CAO`, `06_KE_HOACH`, `09_MOC_BAN_GIAO`, `10_QUY_UOC_CHUNG`.

| Hạn | Bàn giao bắt buộc | Người phụ trách |
|---|---|---|
| **06/11** | Chốt bài toán, mốc dự báo, nhãn, quy ước dữ liệu | Tấn Lên + Lam Linh |
| **12/11** | Bảng data một dòng/đơn, data dictionary + feature registry; nháp chương 1–2 | Lam Linh + Trúc Chi; Tấn Lên + Ngọc Lan |
| **16/11** | Chương 3, dữ liệu, EDA, QA và notebook chạy lại được | Lam Linh |
| **20/11** | RF pipeline, P/R/F1/AP/FP/Top-K trên Validation + split_id | Ngọc Lan |
| **21/11** | Tấn Lên huấn luyện MLP: pipeline, bảng Validation, loss và artifact | Tấn Lên (TV1) |
| **22/11** | Trúc Chi CHỈ fit Dummy, nhận RF Ngọc Lan và MLP Tấn Lên, chốt champion/threshold trên Validation | Trúc Chi + Ngọc Lan + Tấn Lên |
| **24/11** | Frozen Test predictions từ Trúc Chi; Vĩnh Chi tính lại cả RF/Dummy/MLP | Vĩnh Chi + Trúc Chi (Ngọc Lan RF, Tấn Lên MLP) |
| **27/11** | Bản đầy đủ Ch1–6 + phụ lục + Streamlit + slides draft | Tấn Lên + cả nhóm |
| **28/11** | Rà soát chéo và sửa lỗi | Cả nhóm |
| **30/11** | Đóng gói bản cuối, tập bảo vệ, kiểm tra khả năng tái lập | Tấn Lên + cả nhóm |

**Bàn giao:** Ch3 Lam Linh → Ch4 Trúc Chi chốt split → Ch2 Ngọc Lan train RF và Notebook 01 Tấn Lên train MLP → Ch4 Trúc Chi chỉ fit Dummy + tích hợp → Ch5 Vĩnh Chi Test độc lập → Ch6/FINAL Tấn Lên. Giữ 6 chương/27 mục.

### Thống nhất mỗi buổi kiểm tra
- Nội dung đã hoàn tất và URL commit/PR.
- Vướng mắc đang chặn tiến độ.
- Input cần người khác bàn giao (file, schema, dự đoán, model).
- Việc sẽ hoàn thành trước mốc tiếp theo.

Đề xuất họp nhanh: 08/11, 15/11, 22/11, 27/11, 29/11.
