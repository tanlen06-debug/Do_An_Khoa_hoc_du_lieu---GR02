# Quy trình làm việc GitHub – Nhóm 02

## Vai trò (theo phân công báo cáo)

- Tấn Lên: Chương 1, Chương 6, phụ lục, trưởng nhóm / review tích hợp.
- Ngọc Lan: Chương 2 (lý thuyết, trích dẫn và consistency).
- Lam Linh: Chương 3 (data ingestion, preprocessing, EDA, feature registry).
- Trúc Chi: Chương 4 (split, baseline, ML, MLP, tuning).
- Vĩnh Chi: Chương 5 (test report, error analysis, Top-K, limitations).

## Nhánh và Pull Request

`main`: nhánh tích hợp có review. Mỗi thành viên làm trên nhánh được phân theo chương (xem GitHub branches), có thể tạo nhánh công việc phụ theo mẫu `feature/ch03-short-task` nếu cần.

```bash
git clone https://github.com/tanlen06-debug/Do_An_Khoa_hoc_du_lieu---GR02.git
cd Do_An_Khoa_hoc_du_lieu---GR02
git switch main
git pull origin main
git switch -c feature/ch03-data-audit
# thực hiện thay đổi và tự kiểm tra...
git add <duong-dan-file-cua-minh>
git commit -m "feat(ch03): add Olist profiling notebook"
git push -u origin feature/ch03-data-audit
# Tạo Pull Request từ feature/... vào main trên GitHub
```

**Không dùng `git add .` nếu chưa kiểm tra `git status`.** Trước khi tạo PR, chạy `pytest -q`, kiểm tra notebook không có dữ liệu nhạy cảm / output quá lớn, mô tả kết quả và link Issue.

## Nguyên tắc phối hợp

1. Không tự sửa đầu ra đã được owner khác bàn giao (không sửa định nghĩa is_late, split hay test scores khi chưa trao đổi).
2. Data owner xuất một dataset/scheme duy nhất, lập `data dictionary`, kiểm tra số bản ghi và hash/version.
3. Model owner dùng schema/data split đã đóng băng; không tính giá trị tương lai cho feature.
4. Evaluation owner nhận file xác suất trên **tập Test cố định**, đối soát với số liệu model owner.
5. Dashboard owner chỉ tải pipeline đã kiểm tra và dữ liệu demo hợp lệ; không tự huấn luyện lại bằng Test.
6. Người review kiểm tra code, kết quả, leakage, tương thích schema và thông tin nguồn trước khi merge.
7. Khi gặp blocker quá 24h, mở Issue hoặc ghi vào tab `11_LOG_VUONG_MAC`; trao đổi trước khi đổi hợp đồng dữ liệu.
8. Cuối ngày có làm việc: cập nhật trạng thái và link minh chứng ở Google Sheets.

## Quy tắc commit

- `docs(ch02): add literature comparison`
- `feat(ch03): create one-order dataset`
- `feat(ch04): train random forest`
- `test: add late label edge cases`
- `fix(ch05): correct AP reporting`

## Nguyên tắc nghiệm thu

PR phải có: mục tương ứng 04_BAO_CAO, file thay đổi, cách chạy, số liệu/hình minh chứng (nếu đã có), kiểm tra đối chiếu với owner liền kề, và xác nhận không có Data Leakage.
