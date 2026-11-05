# Đồ án thực tế Khoa học dữ liệu – Nhóm 02

**Tên đăng ký chính thức:** Phân tích dữ liệu đơn hàng và dự đoán nguy cơ giao hàng trễ trong thương mại điện tử.

**Nguồn dữ liệu:** [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce), Brazil 2016–2018. **Hạn hoàn tất nội bộ:** 30/11/2026.

**Trạng thái:** Bộ khung gồm **5 notebook cá nhân + 1 notebook FINAL**, tài liệu lý thuyết Markdown, kiểm tra dữ liệu, notebook mô hình và đánh giá. Chưa có dữ liệu hoặc điểm số thực nghiệm Olist cho tới khi nhóm chạy thực tế.

## Phân công và notebook

| Thành viên | Nội dung báo cáo | Notebook | Lý thuyết Markdown |
|---|---|---|---|
| **Tấn Lên** | Chương 1, Chương 6, phụ lục và tích hợp | [01_TAN_LEN](notebooks/01_TAN_LEN_chuong_1_6.ipynb) | [Lý thuyết Ch1/6](docs/theory/01_tan_len_ch1_ch6.md) |
| **Ngọc Lan** | Chương 2: cơ sở lý thuyết | [02_NGOC_LAN](notebooks/02_NGOC_LAN_chuong_2.ipynb) | [Lý thuyết Ch2](docs/theory/02_ngoc_lan_ch2.md) |
| **Lam Linh** | Chương 3: dữ liệu, EDA, feature | [03_LAM_LINH](notebooks/03_LAM_LINH_chuong_3.ipynb) | [Lý thuyết Ch3](docs/theory/03_lam_linh_ch3.md) |
| **Trúc Chi** | Chương 4: Dummy, RF, MLP và tuning | [04_TRUC_CHI](notebooks/04_TRUC_CHI_chuong_4.ipynb) | [Lý thuyết Ch4](docs/theory/04_truc_chi_ch4.md) |
| **Vĩnh Chi** | Chương 5: đánh giá, error analysis | [05_VINH_CHI](notebooks/05_VINH_CHI_chuong_5.ipynb) | [Lý thuyết Ch5](docs/theory/05_vinh_chi_ch5.md) |
| **Cả nhóm – Tấn Lên tích hợp** | Tổng hợp toàn bộ đồ án sau khi hoàn thành | [06_FINAL](notebooks/06_FINAL_tong_hop_do_an.ipynb) | [Hướng dẫn final](docs/theory/06_final_integration.md) |

[Hướng dẫn chi tiết từng notebook](docs/NOTEBOOK_GUIDE.md) · [Đề cương 6 chương / 27 hạng mục](docs/REPORT_OUTLINE.md) · [Kế hoạch tháng 11](docs/PLAN_NOV2026.md).

## Quy trình triển khai

```text
Tấn Lên (Ch1/Ch6) ─────────────────────────────────────────┐
Ngọc Lan (Ch2, lý thuyết) ──────────────────────────────────┤
Lam Linh  (Ch3: Olist 9 CSV → data cấp đơn)                 │
        ↓                                                    │
Trúc Chi  (Ch4: temporal split → Dummy/RF/MLP → Test preds) │
        ↓                                                    │
Vĩnh Chi  (Ch5: metric, PR Curve, Top-K và lỗi)              │
        └────────────────────────────────────────────────────┤
                                                             ↓
                                              06_FINAL (tổng hợp)
                                                             ↓
                                              Báo cáo + Streamlit + bảo vệ
```

**Thực thi thực nghiệm:** chạy notebook Ch3 → Ch4 → Ch5 → FINAL khi đã có dữ liệu Olist; Ch1 và Ch2 làm song song, rà soát trước khi chốt. **Không đào tạo mô hình trong FINAL.**

## Cài đặt

```bash
git clone https://github.com/tanlen06-debug/Do_An_Khoa_hoc_du_lieu---GR02.git
cd Do_An_Khoa_hoc_du_lieu---GR02
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
jupyter lab
```

Tải 9 tệp CSV vào `data/raw/` theo [data/README.md](data/README.md). Dữ liệu raw/processed, `joblib` và secrets không được push.

## Thống nhất chuyên môn

- **Mốc dự báo:** `order_approved_at`.
- **Nhãn trễ:** `DATE(actual_delivery) > DATE(estimated_delivery)`; `actual_delivery` chỉ dùng tạo nhãn và kiểm tra hậu nghiệm.
- **Grain:** một dòng cho mỗi `order_id`.
- **Temporal split** và fit preprocessing **train-only**; **chọn ngưỡng trên Validation**, Test chỉ đánh giá cuối.
- **Mô hình:** Dummy tham chiếu, Random Forest (ML), MLP (DL).
- **Đánh giá:** Precision, Recall, F1, Average Precision (AP), FP và Precision@K/Recall@K.
- **Giới hạn:** delivered-only, Brazil 2016–2018; dashboard chỉ là **demo hồi cứu**.

## Quy trình GitHub

Chỉ dùng **`main` làm nhánh gốc có sẵn**. Các thành viên **tự tạo nhánh** từ main lúc bắt đầu làm:
```bash
git switch main
git pull origin main
git switch -c feature/ten-cua-ban-nhiem-vu
# sửa file thuộc nhiệm vụ của mình
git add notebooks/03_LAM_LINH_chuong_3.ipynb
git commit -m "feat(ch03): implement Olist EDA"
git push -u origin feature/ten-cua-ban-nhiem-vu
```
Tạo Pull Request về main để được review; sau khi merge, xóa nhánh feature không còn dùng. Chi tiết tại [TEAM_WORKFLOW](docs/TEAM_WORKFLOW.md).

**Theo dõi công việc:** [Google Sheet GR02](https://docs.google.com/spreadsheets/d/1bbsNPpLUnJDNtUY-1TLw942ftK-fQfL8t-_j4jZkywY/edit) (tabs 04_BAO_CAO, 06_KE_HOACH, 09_MOC_BAN_GIAO) và [GitHub Issues](https://github.com/tanlen06-debug/Do_An_Khoa_hoc_du_lieu---GR02/issues).

**Kiểm thử code hiện có:** `pytest -q`. Chạy `streamlit run app/app.py` để mở dashboard khung (chưa gắn model khi chưa có kết quả thực nghiệm).
