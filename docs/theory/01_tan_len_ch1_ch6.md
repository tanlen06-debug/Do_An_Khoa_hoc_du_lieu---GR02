# LÝ THUYẾT & HƯỚNG DẪN – TẤN LÊN (CHƯƠNG 1, 6, PHỤ LỤC)

**Notebook:** [01_TAN_LEN_chuong_1_6.ipynb](../../notebooks/01_TAN_LEN_chuong_1_6.ipynb) · **GitHub Issues:** #2, #7, #9.  
**Thời điểm dự báo của đồ án:** `order_approved_at`; dữ liệu Olist Brazil 2016–2018.

## Chương 1 – Phát biểu bài toán khoa học

### 1.1 Tình huống thực tiễn
Trong một quy trình thương mại điện tử, đơn hàng trải qua phê duyệt, chuẩn bị, bàn giao đơn vị vận chuyển và giao hàng. Đội vận hành muốn **nhận biết rủi ro chậm giao trước khi kết quả xảy ra**, để ưu tiên kiểm tra các đơn có nguy cơ cao. Đồ án không tự động điều phối hãng vận chuyển hay khẳng định can thiệp giúp giảm trễ; đó là hướng đánh giá triển khai sau.

**Cách viết:** (1) quy trình TMĐT có dẫn nguồn; (2) vấn đề giao trễ; (3) yêu cầu dự báo sớm; (4) liên hệ nguồn dữ liệu Olist.

### 1.2 Bài toán phân loại nhị phân
Đơn vị quan sát: một `order_id`. Tập có nhãn đang đề xuất chỉ gồm đơn `delivered`, đã phê duyệt, có đủ hai ngày giao thực tế/dự kiến.

- `y=1`: `DATE(order_delivered_customer_date) > DATE(order_estimated_delivery_date)`
- `y=0`: hai ngày hợp lệ và thực tế **không sau** dự kiến.
- `p(y=1|X,t0)`: xác suất ước lượng tại thời điểm duyệt đơn; đầu vào `X` phải biết được tại `t0`.

Mục tiêu không phải dự đoán chính xác ngày giao (regression), cũng không phải sử dụng hai ngày giao để "dự đoán" (rò rỉ nhãn). Ngày giao thực tế chỉ làm *ground truth*.

### 1.3 Mục tiêu và câu hỏi nghiên cứu
- Câu 1: tỷ lệ đơn giao trễ trong dữ liệu Olist quan sát được là bao nhiêu và phân bố theo tháng, vùng, người bán, danh mục có khác nhau không?
- Câu 2: chỉ dùng thuộc tính trước/lúc phê duyệt, Random Forest và MLP có nâng hiệu quả xếp hạng rủi ro so với Dummy không?
- Câu 3: khi chỉ theo dõi Top-K đơn, chất lượng cảnh báo và số cảnh báo sai như thế nào?
- Câu 4: dashboard nguyên mẫu thể hiện insight và danh sách ưu tiên ra sao?

Viết mục tiêu đo lường được bằng EDA, bảng metrics Test và demo. **Không đưa ra kết luận trước khi chạy thực nghiệm.**

### 1.4 Phạm vi và hạn chế
- Olist: giao dịch Brazil 2016–2018; không tương đương Shopee/TikTok Shop/Lazada tại Việt Nam năm 2026.
- Delivered-only gây *selection bias* vì đã loại đơn bị hủy/chưa có kết quả.
- Dự báo sớm cần kiểm tra **feature availability** tại `order_approved_at`.
- Dashboard dùng dữ liệu lịch sử / mô phỏng, chưa có pipeline realtime và phân tích hiệu quả can thiệp thực địa.

## Chương 6 – Nguyên mẫu ứng dụng
**Đầu vào:** file processed đã kiểm tra, model pipeline lưu trong `models/champion.joblib`, metadata (feature list và threshold), bảng KPI + dự đoán Test Ch5.

**Giao diện 1 – EDA lịch sử:** số đơn có nhãn, số và tỷ lệ trễ, tỷ lệ trễ theo tháng/bang/danh mục. Tất cả chỉ số phải nêu mẫu số.

**Giao diện 2 – Hỗ trợ ưu tiên:** nhận các cột feature hợp lệ ở `t0`, gọi `predict_proba`, xếp hạng xác suất giảm dần, chọn Top-K. Ngưỡng cảnh báo được lựa chọn trên Validation, không đổi theo Test.

**Kiểm thử:** test khi thiếu model, input thiếu cột, số âm/NaN, thay đổi nguồn dữ liệu, sai categorical, giao diện không crash, có ảnh chụp dự phòng. Streamlit chỉ là công cụ demo; thiếu model phải thông báo chứ không dự đoán ngẫu nhiên.

## Phụ lục và hướng dẫn báo cáo
- Mã nguồn, môi trường Python và version thư viện; đường dẫn tải Olist và giấy phép theo nguồn.
- Seed/cutoff phân chia, cấu hình model, định nghĩa nhãn, nhật ký kiểm soát leakage.
- Hướng dẫn chạy `pip install -r requirements.txt`, thứ tự notebook, `streamlit run app/app.py`.
- Kết luận dựa trên bảng Ch5 và hạn chế thật, không hứa hiệu quả chưa kiểm chứng.

**Điều kiện nghiệm thu:** báo cáo Ch1 và Ch6 khớp dữ liệu, mô hình, kết quả; hình và bảng có chú thích; link notebook/PR có minh chứng.

## MLP – Trách nhiệm bổ sung của Tấn Lên (TV1), sản phẩm cho mục 4.4 của Chương 4
Tấn Lên **trực tiếp huấn luyện MLP** trong các cell thực nghiệm mới thuộc `notebooks/01_TAN_LEN_chuong_1_6.ipynb`, sử dụng `src.experiment.get_shared_splits` và `SAFE_FEATURES` do Trúc Chi thống nhất.

- Pipeline: imputer, `StandardScaler` cho numeric, one-hot cho categorical, `MLPClassifier` với `early_stopping`.
- Chọn `hidden_layer_sizes`/`alpha` bằng AP Validation, ngưỡng F1 Validation; trình bày training loss và P/R/F1/AP/FP/Top-K Validation.
- Bàn giao `models/tan_len_mlp.joblib`, `data/processed/mlp_val_predictions.csv`, `mlp_metadata.json` cho Trúc Chi.
- **Trúc Chi chỉ dùng kết quả TV1 để biên soạn mục 4.4**, không fit lại MLP. Vĩnh Chi độc lập kiểm tra Test cuối cùng. Tấn Lên vẫn chịu trách nhiệm Ch1/Ch6/FINAL, không thay đổi cấu trúc báo cáo.
