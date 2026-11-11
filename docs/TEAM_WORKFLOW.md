# QUY TRÌNH GITHUB – NHÓM 02 (CẬP NHẬT 05/11/2026)

## Quy ước nhánh
**Chỉ duy trì sẵn `main`** – nhánh tích hợp có tài liệu và notebook chung. **Nhóm trưởng không tạo sẵn branch cá nhân.** Mỗi thành viên tự tạo nhánh từ `main` mới nhất và đặt tên `feature/<thanh-vien>-<nhiem-vu>` khi bắt đầu.

```bash
git clone https://github.com/tanlen06-debug/Do_An_Khoa_hoc_du_lieu---GR02.git
cd Do_An_Khoa_hoc_du_lieu---GR02
git switch main
git pull origin main
git switch -c feature/lam-linh-ch03-data
# Chỉnh sửa và kiểm thử, không commit CSV, model lớn, token
git status
git add notebooks/03_LAM_LINH_chuong_3.ipynb
git commit -m "feat(ch03): add validated Olist features"
git push -u origin feature/lam-linh-ch03-data
# Tạo Pull Request về main; khi được duyệt thì merge.
```

**Sau khi nhánh feature đã merge và không còn cần giữ, người tạo có thể xóa nhánh của mình trên GitHub.** Không bao giờ xóa `main`.

## Mỗi thành viên làm trong file nào?
| Thành viên | Notebook chính | Markdown lý thuyết | File báo cáo |
|---|---|---|---|
| Tấn Lên | `01_TAN_LEN_chuong_1_6.ipynb` | `docs/theory/01_tan_len_ch1_ch6.md` | `CH01_OVERVIEW.md`, `CH06_DASHBOARD.md`, `APPENDIX.md` |
| Ngọc Lan | `02_NGOC_LAN_chuong_2.ipynb` | `docs/theory/02_ngoc_lan_ch2.md` | `CH02_THEORY.md` |
| Lam Linh | `03_LAM_LINH_chuong_3.ipynb` | `docs/theory/03_lam_linh_ch3.md` | `CH03_DATA.md` |
| Trúc Chi | `04_TRUC_CHI_chuong_4.ipynb` | `docs/theory/04_truc_chi_ch4.md` | `CH04_MODELING.md` |
| Vĩnh Chi | `05_VINH_CHI_chuong_5.ipynb` | `docs/theory/05_vinh_chi_ch5.md` | `CH05_RESULTS.md` |
| Cả nhóm | `06_FINAL_tong_hop_do_an.ipynb` | `docs/theory/06_final_integration.md` | Báo cáo và slide cuối |

Đừng sửa cùng lúc notebook của người khác trên nhiều nhánh. Mọi thay đổi vào `src/` hoặc hợp đồng dữ liệu cần được owner liên quan review trước khi merge.

## Trình tự & bàn giao
Lam Linh Ch3 → Trúc Chi chốt split → Ngọc Lan train RF/Validation → Trúc Chi train Dummy/MLP, nạp RF, xuất Test → Vĩnh Chi đánh giá độc lập 3 model trên Test → Tấn Lên FINAL.

- Ch3: `data/processed/orders_model_ready.csv`; schema, nhãn, QA, feature whitelist.
- Ch2 (Ngọc Lan): `rf_val_predictions.csv`, `rf_metadata.json`, `models/ngoc_lan_random_forest.joblib`, chung split_id.
- Ch4 (Trúc Chi): `test_predictions.csv`, `experiment_metadata.json`, `models/dummy_truc_chi.joblib`, `models/mlp_truc_chi.joblib`, `models/champion.joblib`; chọn threshold/champion trên Validation.
- Ch5 (Vĩnh Chi): độc lập kiểm tra Test predictions từ 3 fitted model rồi xuất `model_metrics.csv`, `topk_analysis.csv`, `pr_curve_test.png`.
- Ch6/FINAL: kiểm tra file, áp dụng model đã review và tổng hợp báo cáo. **Không dùng Test để lựa chọn mô hình.**

## Tiêu chí PR
1. Có mô tả task/Issue, file đã thay đổi, lệnh chạy, ảnh/bảng và tình trạng chạy thật.
2. Chạy `pytest -q` và notebook từ đầu (khi đã có data); không commit notebook output quá lớn.
3. Không commit CSV gốc/processed, model lớn, file `.env`, token.
4. Không thêm biến dữ liệu sau `order_approved_at` vào X.
5. Có người nhận bàn giao review và cập nhật `Google Sheets 04_BAO_CAO / 06_KE_HOACH`.

## Hạn triển khai
Theo `docs/PLAN_NOV2026.md`: chốt bài toán 06/11, dataset 12–16/11, model 22/11, Test 24/11, báo cáo/demo 27/11 và hoàn tất nội bộ 30/11/2026.

**Nguồn quy tắc:** [Notebook guide](NOTEBOOK_GUIDE.md), [Data contract](DATA_CONTRACT.md), [Experiment protocol](EXPERIMENT_PROTOCOL.md), [Final integration](theory/06_final_integration.md).
