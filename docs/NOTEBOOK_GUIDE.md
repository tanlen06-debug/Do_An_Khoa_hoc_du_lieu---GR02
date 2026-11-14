# HƯỚNG DẪN SỬ DỤNG 6 NOTEBOOK CHUNG – NHÓM 02

## Bộ notebook bắt buộc
1. `notebooks/01_TAN_LEN_chuong_1_6.ipynb` – Tấn Lên, Ch1 + Ch6 + phụ lục.
2. `notebooks/02_NGOC_LAN_chuong_2.ipynb` – Ngọc Lan, Ch2.
3. `notebooks/03_LAM_LINH_chuong_3.ipynb` – Lam Linh, Ch3.
4. `notebooks/04_TRUC_CHI_chuong_4.ipynb` – Trúc Chi, Ch4.
5. `notebooks/05_VINH_CHI_chuong_5.ipynb` – Vĩnh Chi, Ch5.
6. `notebooks/06_FINAL_tong_hop_do_an.ipynb` – cả nhóm rà soát, Tấn Lên tích hợp.

Mỗi notebook có Markdown nền tảng, nội dung phải trình bày theo mục báo cáo, mã khởi đầu, điều kiện chạy, file đầu vào/đầu ra, gợi ý nhận xét và checklist nghiệm thu. Tài liệu lý thuyết riêng ở `docs/theory/`.

## Mở môi trường
```bash
git clone https://github.com/tanlen06-debug/Do_An_Khoa_hoc_du_lieu---GR02.git
cd Do_An_Khoa_hoc_du_lieu---GR02
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
jupyter lab
```

Lấy 9 CSV gốc tại `data/raw/` bằng `git lfs pull` (nhánh `main` theo dõi bằng Git LFS), hoặc tải trực tiếp từ https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce. Các notebook tìm repo root qua `docs/DATA_CONTRACT.md`; mở từ repo root hoặc thư mục `notebooks/`.

## Hướng dẫn viết từng cell
- **Markdown (trước code):** mục đích, giả định, đầu vào/đầu ra, ý nghĩa lý thuyết, cảnh báo leakage.
- **Code:** lệnh đọc dữ liệu, kiểm tra QA, pipeline, metric, hình minh họa. Tên biến thống nhất.
- **Markdown (sau code):** số mẫu, KPI, insight có dữ liệu minh chứng, giới hạn, kết luận nhỏ.
- Mỗi biểu đồ/bảng nên có tên, trục/đơn vị, cỡ mẫu và vị trí trích dẫn trong báo cáo.
- **Trạng thái khởi tạo:** không notebook nào có số liệu thực nghiệm Olist; các cells chỉ trả kết quả sau khi chạy với dữ liệu gốc.

## Quy định lưu output notebook trên GitHub
- **Được phép commit notebook `.ipynb` đã chạy**, bao gồm `execution_count` và các output dạng bảng, văn bản, hình/biểu đồ minh chứng cho dữ liệu thật. Notebook chưa chạy (output rỗng) vẫn hợp lệ.
- Chỉ commit kết quả **thực sự được tạo từ code và dữ liệu hợp lệ**, không sửa số liệu thủ công hoặc tạo output giả. Ghi phiên bản dataset, seed và cách chạy để nhóm có thể tái lập.
- Không commit output chứa thông tin cá nhân, đường dẫn riêng tư, secret, dữ liệu gốc/processed toàn bộ, hoặc hình/output quá lớn; chỉ giữ bảng tóm tắt và biểu đồ cần thiết. CSV và mô hình lớn trao đổi theo kênh bàn giao riêng.
- Không commit output lỗi/traceback. Nếu chạy lại phát sinh lỗi, sửa code, chạy lại và xác minh trước khi tạo PR.
- `python -m pytest -q` kiểm tra cú pháp Python, cấu trúc output, và từ chối `output_type = error`. CI **không chạy lại toàn bộ notebook bằng 9 CSV**, nên nhóm trưởng và người nhận vẫn cần review kết quả thật và kiểm tra tái lập.
- Lưu ý notebook có output ảnh sẽ làm Git diff và kích thước repository lớn hơn; ưu tiên minh chứng gọn và liên kết tới `reports/figures/` khi phù hợp.

## Đảm bảo các thành viên không làm trùng
- Tấn Lên (TV1): **huấn luyện MLP tại notebook 01**, bàn giao artifact/Validation cho Ch4; FINAL không huấn luyện lại model. RF do Ngọc Lan, Dummy do Trúc Chi.
- Ngọc Lan: trực tiếp huấn luyện Random Forest trên Train chung, đo P/R/F1/AP/FP/Top-K Validation và bàn giao RF artifact cho Trúc Chi.
- Lam Linh: chịu trách nhiệm duy nhất trong việc định nghĩa nhãn và xuất bảng cấp đơn.
- Trúc Chi: tạo split chung và CHỈ train Dummy; tiếp nhận RF của Ngọc Lan và MLP của Tấn Lên, kiểm tra cùng split_id, chọn champion/ngưỡng trên Validation, xuất frozen Test; không fit lại RF/MLP.
- Vĩnh Chi: không fit lại mô hình; tải RF Ngọc Lan, Dummy Trúc Chi, MLP Tấn Lên để kiểm tra lại xác suất frozen Test rồi tính metrics và Top-K.
- FINAL: đọc, đối chiếu artifact và tổng hợp; không train lại sau khi biết Test.

## Tự tạo nhánh GitHub
Nhóm thống nhất **chỉ duy trì nhánh `main` làm gốc; thành viên tự tạo nhánh khi bắt đầu làm việc**.

```bash
git switch main
git pull origin main
git switch -c feature/ten-thanh-vien-nhiem-vu
# Sửa notebook của mình, kiểm tra, commit, push
git add notebooks/03_LAM_LINH_chuong_3.ipynb docs/theory/03_lam_linh_ch3.md
git commit -m "feat(ch03): prepare Olist orders dataset"
git push -u origin feature/ten-thanh-vien-nhiem-vu
```

Đây là ví dụ tên nhánh; mỗi thành viên dùng tên phù hợp và tạo Pull Request về `main` khi muốn bàn giao. Không dùng nhánh cá nhân có sẵn từ lần thiết lập cũ.

## Khác biệt giữa tồn tại file và hoàn thành
Notebook có nhiều cell hướng dẫn **không có nghĩa nhiệm vụ đã hoàn thành**. Chỉ đánh dấu `Hoàn thành` ở Sheets khi có chạy thành công, minh chứng, review và bản báo cáo đúng mẫu.

## Thứ tự chạy mới: không trùng việc
Ch3 Lam Linh → Ch4 Trúc Chi **tạo split chung** → Ch2 Ngọc Lan **RF**, notebook 01 Tấn Lên **MLP** (cùng Train/Validation) → Ch4 Trúc Chi **chỉ fit Dummy, tích hợp RF+MLP** → Ch5 Vĩnh Chi **đánh giá lại ba model trên Test** → FINAL. Đọc [giao thức chung](EXPERIMENT_PROTOCOL.md).

**Notebook 01 đã thêm khối thực nghiệm MLP cho TV1:** artifact `tan_len_mlp.joblib`, `mlp_val_predictions.csv`, `mlp_metadata.json`. Mục 4.4 vẫn ở Ch4 và do Trúc Chi trình bày dựa trên sản phẩm của TV1.
