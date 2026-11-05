# QUY ƯỚC TỔNG HỢP 5 NOTEBOOK → 06_FINAL

**Tài liệu dành cho cả nhóm; người chịu trách nhiệm chốt notebook final: Tấn Lên.**

## Sơ đồ xử lý và trách nhiệm

| Chủ sở hữu | Notebook | Tác dụng | Đầu ra liên chương |
|---|---|---|---|
| Tấn Lên | `01_TAN_LEN_chuong_1_6.ipynb` | Tổng quan, thiết kế Dashboard, kiểm tra các đầu ra và viết kết luận | Ch1/Ch6, app, README |
| Ngọc Lan | `02_NGOC_LAN_chuong_2.ipynb` | Thuật toán, độ đo, nghiên cứu liên quan | Ch2, nguồn học thuật |
| Lam Linh | `03_LAM_LINH_chuong_3.ipynb` | Tải, làm sạch, join, tạo nhãn, EDA, feature engineering | `orders_model_ready.csv` + schema |
| Trúc Chi | `04_TRUC_CHI_chuong_4.ipynb` | Temporal split, pipelines, Dummy/RF/MLP, chọn threshold | `test_predictions.csv`, model và metadata |
| Vĩnh Chi | `05_VINH_CHI_chuong_5.ipynb` | Đánh giá frozen Test, PR Curve, error analysis, Top-K | `model_metrics.csv`, `topk_analysis.csv`, đồ thị |
| Cả nhóm / Tấn Lên tích hợp | `06_FINAL_tong_hop_do_an.ipynb` | Kiểm chứng nhất quán, tổng hợp KPI và luận điểm bảo vệ | Notebook minh chứng và kết luận cuối |

## Thứ tự thực thi thực tế
Không nhất thiết chạy 01 và 02 trước vì đây là notebook tổng quan/lý thuyết. Khi cần **tái lập phần thực nghiệm**, chạy theo thứ tự:
```
03_LAM_LINH_chuong_3.ipynb
  → 04_TRUC_CHI_chuong_4.ipynb
     → 05_VINH_CHI_chuong_5.ipynb
        → 06_FINAL_tong_hop_do_an.ipynb
```
Notebook 01/02 được hoàn thành song song và rà soát trước khi đóng gói final. Dashboard chạy bằng `streamlit run app/app.py` sau khi tích hợp model được duyệt.

## Hợp đồng dữ liệu giữa các notebook
- **Ch3 → Ch4:** `data/processed/orders_model_ready.csv` (mỗi `order_id` duy nhất; `is_late` theo ngày; có `order_approved_at`, `order_delivered_customer_date` chỉ để kiểm tra label maturity; chỉ dùng feature whitelist trong X).
- **Ch4 → Ch5:** `test_predictions.csv` có `order_id,y_true,p_dummy,p_rf,p_mlp,y_pred_champion`, `experiment_metadata.json` gồm features, threshold, champion, cutoff và seed, model artifact `models/champion.joblib`.
- **Ch5 → FINAL:** `reports/tables/model_metrics.csv`, `topk_analysis.csv`, `reports/figures/pr_curve_test.png`, nhận xét có nguồn.
- **FINAL → Báo cáo:** bảng kết quả theo mô hình, hình PR, Top-K, EDA và kết luận trùng một tập dữ liệu và một version model.

## Điều kiện nghiệm thu FINAL
- [ ] 6 chương + phụ lục đầy đủ theo `docs/REPORT_OUTLINE.md`.
- [ ] Có QA data, kiểm tra uniqueness và thống kê đơn thiếu nhãn.
- [ ] Có temporal split và kiểm soát leakage đúng mốc duyệt.
- [ ] Có đủ Dummy, RF, MLP và so sánh trên frozen Test, không chọn ngưỡng bằng Test.
- [ ] AP, Precision, Recall, F1, FP, Top-K truy ngược được code.
- [ ] Dashboard chạy được với model đã chọn; thông báo rõ giới hạn nghiên cứu.
- [ ] Có README, quy định tải data và lệnh tái lập môi trường.
- [ ] Tất cả thành viên xác nhận phần mình và cập nhật Google Sheet.

**Lưu ý:** Không push dữ liệu gốc, file processed, model lớn hoặc thông tin bí mật lên GitHub.
