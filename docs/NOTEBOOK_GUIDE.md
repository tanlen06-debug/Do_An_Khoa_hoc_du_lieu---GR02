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

Lấy dữ liệu gốc từ https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce vào `data/raw/`; 9 CSV không được commit. Các notebook tìm repo root qua `docs/DATA_CONTRACT.md`; mở từ repo root hoặc thư mục `notebooks/`.

## Hướng dẫn viết từng cell
- **Markdown (trước code):** mục đích, giả định, đầu vào/đầu ra, ý nghĩa lý thuyết, cảnh báo leakage.
- **Code:** lệnh đọc dữ liệu, kiểm tra QA, pipeline, metric, hình minh họa. Tên biến thống nhất.
- **Markdown (sau code):** số mẫu, KPI, insight có dữ liệu minh chứng, giới hạn, kết luận nhỏ.
- Mỗi biểu đồ/bảng nên có tên, trục/đơn vị, cỡ mẫu và vị trí trích dẫn trong báo cáo.
- **Trạng thái khởi tạo:** không notebook nào có số liệu thực nghiệm Olist; các cells chỉ trả kết quả sau khi chạy với dữ liệu gốc.

## Đảm bảo các thành viên không làm trùng
- Tấn Lên: không chạy lại RF/MLP trong notebook Ch1/6 hoặc FINAL.
- Ngọc Lan: chỉ demo thuật toán trên bộ ví dụ giả định được ghi rõ; số liệu thực lấy từ Ch3–Ch5.
- Lam Linh: chịu trách nhiệm duy nhất trong việc định nghĩa nhãn và xuất bảng cấp đơn.
- Trúc Chi: không tự thay đổi label/feature contract, model so sánh có cùng split, không tune Test.
- Vĩnh Chi: không fit lại mô hình, dùng một frozen Test predictions để tính tất cả chỉ số.
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
