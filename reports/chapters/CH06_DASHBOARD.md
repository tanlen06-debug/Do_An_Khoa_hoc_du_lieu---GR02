# Chương 6. Dashboard, kiểm thử và kết luận

**Phụ trách** Tấn Lên. **Trạng thái ngày 28/11/2026** Dashboard đạt các hạng mục kiểm thử trình diễn hồi cứu trong Bảng 6.1.

## 6.1 Thiết kế Dashboard Streamlit

Dashboard hỗ trợ phân tích đơn hàng Olist và lập danh sách ưu tiên theo điểm nguy cơ giao trễ tại thời điểm phê duyệt đơn (`order_approved_at`). Tab **Phân tích lịch sử (EDA)** hiển thị số đơn có nhãn, số đơn trễ, tỷ lệ trễ và biểu đồ theo tháng, bang khách hàng và nhóm giá trị đơn. Có thể lọc theo tháng và bang. Thống kê tỷ lệ trễ theo bang giới hạn ở các bang có ít nhất 30 đơn trong phạm vi lọc.

Tab **Dự đoán & Top-K** nạp mô hình đã huấn luyện và đối chiếu mã phân chia dữ liệu (`split_id`), SHA-256 của dữ liệu và danh sách năm đặc trưng với metadata bàn giao. Tab này nhận đơn từ tập Test đã đóng băng hoặc CSV có `order_id` và đủ năm cột đặc trưng. Các đơn được xếp theo điểm nguy cơ giảm dần. Người dùng chọn số lượng đơn cần rà soát bằng thanh K và tải CSV kết quả. Ngưỡng gắn cờ cảnh báo được giữ ở mức đã chốt trên Validation. Chỉ số Test được tính ngoại tuyến tại Chương 5. [Mã Dashboard](../../app/app.py)

## 6.2 Kiểm thử và hướng dẫn dùng

Từ thư mục gốc của dự án, cài các thư viện và chuẩn bị bộ dữ liệu, metadata và mô hình theo hướng dẫn của nhóm. Chạy `python -m streamlit run app/app.py`, sau đó mở địa chỉ cục bộ do Streamlit hiển thị. [Hướng dẫn và danh sách tệp đầu vào](../../app/README.md)

**Bảng 6.1. Kết quả kiểm thử Dashboard với dữ liệu và mô hình bàn giao**

| Hạng mục | Kết quả quan sát | Trạng thái |
| --- | --- | --- |
| Khởi động, hiển thị EDA và lọc | EDA hiển thị 96.456 đơn có nhãn, 6.534 đơn trễ (6,77%). Lọc bang SP trong ba tháng đầu năm 2018 cho 8.578 đơn, trong đó 575 đơn trễ (6,70%). | Đạt |
| Nạp mô hình và xếp hạng Test | Xác minh MLP với `split_id` `72c64fdd7b6de725a531` và ngưỡng 0,10. Chấm điểm 14.469 đơn. Thay K từ 100 xuống 50 trả về đúng 50 đơn đứng đầu. | Đạt |
| Xuất CSV | Tải qua máy chủ Streamlit được bảng EDA theo tháng và danh sách Top-100 với các cột `rank`, `order_id`, `risk_probability`, `warning`. | Đạt |
| Nhập CSV đặc trưng | CSV hợp lệ được chấm điểm. Cột nhãn bổ sung được bỏ qua và điểm giữ nguyên. Thiếu cột bắt buộc, dữ liệu phi số hoặc thời gian phê duyệt âm đều nhận thông báo lỗi. | Đạt |
| Thiếu tệp mô hình | Mô phỏng thiếu `champion.joblib` cho thấy EDA vẫn hiển thị và tab dự đoán báo thiếu mô hình. | Đạt |
| Ô bang khách hàng để trống | Ô `customer_state` trống hoặc chỉ chứa khoảng trắng được xử lý bằng bộ điền giá trị thiếu của mô hình. Dashboard chấm điểm và xếp hạng đủ 3 đơn trong tệp kiểm thử. | Đạt |

Kết quả lấy từ phiên chạy Streamlit cục bộ và kiểm thử tương tác qua `AppTest` ngày 28/11/2026. Sau khi sửa xử lý ô bang khách hàng trống, cả Cell 3 và Cell 4 chạy thành công trong Jupyter. Bộ kiểm thử tự động của dự án đạt 19/19. [Notebook Chương 6](../../notebooks/01_TAN_LEN_chuong_1_6.ipynb) · [Kiểm thử Dashboard](../../tests/test_dashboard_utils.py)

## 6.3 Kết luận và hướng phát triển

Đề tài đã xây dựng được nguyên mẫu phân tích lịch sử và lập danh sách đơn cần rà soát tại thời điểm phê duyệt. Theo `experiment_metadata.json` của bộ mô hình dùng trong lần chạy, MLP của Tấn Lên được chọn dựa trên Average Precision (AP) cao nhất trên Validation (0,065428, so với 0,064839 của Random Forest). Dashboard sử dụng MLP đã đóng băng với ngưỡng cảnh báo 0,10. Các chỉ số Validation và Test trong mục này đã được đối chiếu bằng cách chạy lại các mô hình đã huấn luyện trên cùng mã phân chia dữ liệu. [Giao thức thực nghiệm](../../docs/EXPERIMENT_PROTOCOL.md)

Trên tập Test theo thời gian gồm **14.469 đơn, trong đó 619 đơn trễ (4,28%)**, Random Forest đạt AP 0,046804, Dummy đạt 0,042781 và MLP đạt 0,039463. Như vậy, thứ hạng mô hình theo AP thay đổi giữa Validation và Test. Ở ngưỡng 0,10, MLP phát 3.642 cảnh báo, gồm **132 đơn giao trễ và 3.510 đơn giao đúng hạn**, tương ứng Precision 3,62% và Recall 21,32%. Ngưỡng này bỏ sót 487 đơn giao trễ. [Bảng chỉ số Test](../tables/model_metrics.csv)

Khi giới hạn rà soát ở **Top-100**, MLP đưa 6 đơn giao trễ và 94 đơn giao đúng hạn vào danh sách. Tỷ lệ đơn trễ trong danh sách là 6,00% (gấp 1,40 lần mức nền Test), nhưng chỉ bao phủ 0,97% tổng số đơn trễ. Kết quả này phù hợp với vai trò minh họa cách ưu tiên rà soát và cho thấy độ bao phủ còn thấp khi ngân sách kiểm tra hạn chế. [Bảng phân tích Top-K](../tables/topk_analysis.csv)

Dashboard đạt các hạng mục kiểm thử để trình diễn hồi cứu. Mức cảnh báo sai, độ bao phủ và phạm vi mẫu gồm đơn đã giao có nhãn tại Brazil giai đoạn 2016–2018 giới hạn khả năng áp dụng vào vận hành thực tế. Hướng phát triển là đánh giá mô hình trên dữ liệu logistics mới, kiểm tra độ hiệu chuẩn của điểm nguy cơ và đo hiệu quả can thiệp theo chi phí rà soát.

**Đối chiếu trước khi chốt báo cáo tổng hợp.** Notebook Chương 4 đang lưu kết quả chọn Random Forest với AP Validation 0,067137, trong khi bộ tệp dùng để nghiệm thu Dashboard xác nhận MLP. Phần diễn giải của notebook Chương 5 ghi 136 cảnh báo đúng của Random Forest trên Test. Phép tính lại với bộ mô hình đang dùng cho 142 cảnh báo đúng, khớp bảng CSV. Cần thống nhất bộ mô hình và số liệu giữa các chương khi chốt bản tổng hợp. [Notebook Chương 4](../../notebooks/04_TRUC_CHI_chuong_4.ipynb) · [Notebook Chương 5](../../notebooks/05_VINH_CHI_chuong_5.ipynb)
