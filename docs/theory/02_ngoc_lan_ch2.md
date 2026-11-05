# LÝ THUYẾT & HƯỚNG DẪN – NGỌC LAN (CHƯƠNG 2)

**Notebook:** [02_NGOC_LAN_chuong_2.ipynb](../../notebooks/02_NGOC_LAN_chuong_2.ipynb) · **Issue:** #3.

## 2.1 Tổng quan thương mại điện tử và logistics
- **Order fulfillment**: quy trình xử lý và hoàn thành đơn, có thể gồm phê duyệt, lấy/đóng gói, bàn giao và giao hàng.
- **SLA (Service Level Agreement)**: chuẩn thời gian/chất lượng dịch vụ theo cam kết của các bên; không tự đồng nhất SLA với ngày giao dự kiến của Olist.
- **Estimated delivery**: mốc ngày dự kiến; **actual delivery**: thời điểm giao thật. Tên biến được xác minh trên `olist_orders_dataset.csv`.
- **Phân tích nghiệp vụ:** khách hàng bị ảnh hưởng bởi giao trễ, bộ phận vận hành muốn ưu tiên nguồn lực trước khi quá hạn.

**Viết học thuật:** nêu định nghĩa có nguồn, giải thích bằng sơ đồ quy trình và dẫn liên hệ cụ thể tới đề tài.

## 2.2 Khai thác dữ liệu và EDA
Với Olist, 9 CSV có quan hệ 1–n. Các câu hỏi EDA phải tính ở **cấp đơn hàng** (`order_id` unique), không ở cấp item nếu kết luận là "tỷ lệ đơn". Các bước:
1. Hiểu bảng, khóa và khả năng thiếu dữ liệu.
2. Tổng hợp các bảng một-nhiều trước khi nối, tránh nhân bản đơn.
3. Xây dựng nhãn trễ theo ngày lịch, loại các trường hợp không đủ nhãn.
4. Tính phân phối các biến, tỷ lệ trễ theo tháng, vùng, danh mục và người bán.
5. Diễn giải biểu đồ bằng số lượng nhóm, không kết luận nhân quả từ sự khác biệt quan sát.

**Cần phân biệt EDA và dự báo:** EDA hậu nghiệm có thể dùng thông tin về kết quả giao hàng, nhưng feature dự báo tại phê duyệt không được biết tương lai.

## 2.3 Mô hình Machine Learning và Deep Learning
### Dummy Classifier
Mốc tham chiếu ("không học thông tin đặc trưng") để đánh giá một mô hình có hữu ích hơn baseline tối giản không.

### Random Forest
Một tập cây quyết định được học từ các mẫu bootstrap/ngẫu nhiên hóa đặc trưng; kết quả phân loại được tổng hợp qua các cây. Các tham số quan trọng: `n_estimators`, `max_depth`, `min_samples_leaf`, `class_weight`, `random_state`. Không bảo đảm vượt MLP trong mọi dữ liệu.

### Multi-Layer Perceptron (MLP)
Mạng nơ-ron truyền thẳng nhiều lớp: `h^(l)=σ(W^(l)h^(l-1)+b^(l))`. Đầu ra sigmoid cho bài toán nhị phân, tối ưu trọng số để giảm mất mát; MLP trong scikit-learn sử dụng thiết kế mạng tương ứng của `MLPClassifier`. Cần mã hóa biến phân loại, chuẩn hóa đầu vào số và kiểm soát overfitting (`alpha`, early stopping).

**So sánh phải công bằng:** cùng target, nguồn split, whitelist features và tập Test. Preprocessing có thể khác vì đặc thù thuật toán nhưng không chứa dữ liệu tương lai.

## 2.4 Độ đo
Với lớp dương là **giao trễ**:
- `Precision = TP/(TP+FP)`: tỷ lệ cảnh báo trễ đúng.
- `Recall = TP/(TP+FN)`: tỷ lệ đơn thực sự trễ được phát hiện.
- `F1 = 2×Precision×Recall/(Precision+Recall)`.
- `AP = Σ_n (R_n−R_(n−1))×P_n`: Average Precision tổng hợp đường PR theo bước tăng Recall. AP không nhất thiết bằng phép tích phân hình thang của đường PR.
- `FP`: số cảnh báo trễ sai.
- `Precision@K = TP@K/K`, `Recall@K = TP@K/TotalPositive`.

**Mất cân bằng nhãn:** nếu lớp trễ ít, chỉ báo Accuracy có thể gây hiểu nhầm; cần so sánh trên Precision–Recall và số cảnh báo sai.

## 2.5 Phương pháp tổng quan nghiên cứu liên quan
Chọn 3–5 bài có thể kiểm chứng: tác giả, năm, link DOI/URL, dữ liệu, mô hình, metric, đóng góp, giới hạn, điểm khác so với nhóm. Chủ đề liên quan: thời gian giao hàng, last-mile logistics, delay classification, tabular classification. Không tạo bảng "công trình liên quan" bằng tên bài, con số hoặc nguồn giả.

## Nguồn kỹ thuật tin cậy để tra cứu
- [Olist dataset (Kaggle)](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
- [RandomForestClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html)
- [MLPClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html)
- [average_precision_score](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.average_precision_score.html)
- [precision_recall_curve](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_recall_curve.html)

**Nghiệm thu:** mục 2.1–2.5 có định nghĩa + nguồn + giải thích có liên hệ bài toán; thuật toán/metric khớp Ch4–Ch5; không đưa kết quả Olist chưa chạy.
