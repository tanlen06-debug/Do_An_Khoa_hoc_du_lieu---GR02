# CH02 THEORY

**Phụ trách:** Ngọc Lan. **Trạng thái:** Đang hoàn thiện Chương 2; Random Forest đã huấn luyện và đánh giá trên Validation, đang chờ nghiệm thu.

## 2.1 Cơ sở e-commerce logistics

### 2.1.1. Khái niệm và đặc điểm logistics thương mại điện tử

Logistics là quá trình tổ chức, quản lý và phối hợp các hoạt động liên quan đến lưu chuyển, lưu trữ hàng hóa và thông tin từ nơi cung ứng đến người tiêu dùng.

Trong thương mại điện tử, logistics không chỉ bao gồm hoạt động vận chuyển mà còn liên quan đến tiếp nhận đơn hàng, quản lý kho, đóng gói, giao nhận và xử lý đổi trả. Theo Savills Vietnam, E-logistics đóng vai trò kết nối hoạt động bán hàng trực tuyến với quá trình đưa hàng hóa đến khách hàng.

So với logistics truyền thống, logistics thương mại điện tử thường phải xử lý nhiều đơn hàng nhỏ, phân phối đến các địa điểm nhận hàng khác nhau và đáp ứng kỳ vọng về thời gian giao hàng của khách hàng.

Đối với đề tài của nhóm, hoạt động logistics thương mại điện tử là bối cảnh trực tiếp của bài toán dự đoán nguy cơ giao hàng trễ. Việc phân tích dữ liệu đơn hàng giúp nhóm tìm hiểu những yếu tố có thể liên quan đến tiến độ giao nhận và xây dựng mô hình hỗ trợ cảnh báo sớm.

### 2.1.2. Quy trình xử lý và giao nhận đơn hàng

Quá trình hoàn tất đơn hàng trong thương mại điện tử gồm nhiều hoạt động như tiếp nhận đơn hàng, xác nhận thanh toán, chuẩn bị sản phẩm, đóng gói, bàn giao cho đơn vị vận chuyển và giao hàng đến khách.

Với bộ dữ liệu Brazilian E-Commerce Public Dataset by Olist, vòng đời đơn hàng có thể được mô tả qua các mốc thời gian:

1. `order_purchase_timestamp`: Thời điểm khách hàng đặt hàng.
2. `order_approved_at`: Thời điểm đơn hàng được phê duyệt.
3. `order_delivered_carrier_date`: Thời điểm đơn được bàn giao cho đơn vị vận chuyển.
4. `order_delivered_customer_date`: Thời điểm khách hàng thực tế nhận hàng.

Ngoài ra, dữ liệu còn có `order_estimated_delivery_date`, thể hiện ngày giao dự kiến.

Các mốc thời gian này giúp nhóm nghiên cứu tiến trình giao nhận và xác định tình trạng đúng hạn của đơn hàng.

Tuy nhiên, không phải tất cả thông tin đều có thể sử dụng làm đầu vào mô hình. Đề tài chọn thời điểm `order_approved_at` làm mốc dự báo, do đó các thông tin chỉ xuất hiện sau thời điểm phê duyệt không được đưa vào đặc trưng dự đoán.

### 2.1.3. Thời gian giao hàng và mức độ đáp ứng dịch vụ

Thời gian giao hàng phản ánh khoảng thời gian từ khi khách hàng đặt mua đến khi nhận được sản phẩm. Trong hoạt động logistics, việc theo dõi thời gian xử lý và giao nhận có ý nghĩa đối với chất lượng dịch vụ.

Theo IBM, Service Level Agreement (SLA) là thỏa thuận xác định các tiêu chuẩn dịch vụ, mức hiệu suất cần đáp ứng và trách nhiệm của các bên.

Trong phạm vi nghiên cứu Olist, nhóm sử dụng ngày giao dự kiến và ngày giao thực tế để xác định trạng thái giao hàng trễ. Đây là quy ước đo lường của đồ án, không có nghĩa bộ dữ liệu cung cấp đầy đủ một hợp đồng SLA.

Đối với các đơn đã giao thành công và đủ thông tin xác định nhãn, biến mục tiêu `is_late` được quy định như sau:

- `is_late = 1`: Ngày giao thực tế muộn hơn ngày giao dự kiến.
- `is_late = 0`: Ngày giao thực tế sớm hơn hoặc bằng ngày giao dự kiến.

Hai mốc thời gian được so sánh theo phần ngày (`DATE`), không so sánh trực tiếp giờ và phút.

Các đơn chưa giao thành công hoặc thiếu thông tin cần thiết không được tự động gán nhãn 0.

### 2.1.4. Những yếu tố liên quan đến nguy cơ giao hàng trễ

Nguy cơ giao hàng trễ có thể liên quan đến nhiều yếu tố như khu vực nhận hàng, thời điểm phát sinh đơn, đặc điểm sản phẩm, số lượng hàng hóa và năng lực xử lý của hệ thống giao nhận.

Trong bộ dữ liệu Olist, một số thông tin có thể được nghiên cứu thông qua dữ liệu đơn hàng, khách hàng, người bán, sản phẩm và các mốc thời gian.

Tuy nhiên, việc một yếu tố có liên hệ với tình trạng giao hàng trễ trong dữ liệu lịch sử chưa đủ để kết luận đó là nguyên nhân trực tiếp gây ra giao trễ.

Đồng thời, những thông tin chỉ có sau thời điểm phê duyệt hoặc chưa được xác minh thời điểm xuất hiện không được tự ý sử dụng làm đặc trưng huấn luyện.

Theo giao thức thực nghiệm của nhóm, Random Forest sử dụng năm đặc trưng đầu vào đã thống nhất:

- `purchase_month_number`
- `purchase_weekday`
- `purchase_hour`
- `approval_delay_hours`
- `customer_state`

Năm đặc trưng này được dùng để dự đoán nguy cơ giao hàng trễ tại thời điểm đơn được phê duyệt.

### 2.1.5. Vai trò của phân tích dữ liệu trong dự đoán nguy cơ giao hàng trễ

Dữ liệu phát sinh trong quá trình mua bán và giao nhận hàng hóa có thể hỗ trợ doanh nghiệp theo dõi hoạt động, nhận diện xu hướng và nghiên cứu các yếu tố liên quan đến chất lượng giao hàng.

Trong đề tài này, nhóm sử dụng dữ liệu lịch sử Olist để xây dựng bài toán phân loại nhị phân nhằm dự đoán nguy cơ giao hàng trễ.

Mô hình Random Forest và MLP được sử dụng để học mối quan hệ giữa các đặc trưng đầu vào với nhãn `is_late`, còn Dummy Classifier đóng vai trò mô hình tham chiếu.

Kết quả dự đoán có thể được nghiên cứu để xây dựng danh sách đơn hàng cần ưu tiên theo dõi. Tuy nhiên, khả năng ứng dụng phải được đánh giá bằng những kết quả thực nghiệm thực tế, đặc biệt là số cảnh báo sai và tỷ lệ phát hiện đơn trễ.

Dữ liệu Olist chủ yếu phản ánh hoạt động tại Brazil trong giai đoạn 2016–2018. Vì vậy, kết quả nghiên cứu không mặc nhiên đại diện cho các nền tảng thương mại điện tử hiện nay hoặc thị trường Việt Nam.

**Nguồn tham khảo chính cho mục 2.1:**

- [Savills Vietnam – E-commerce Logistics](https://industrial.savills.com.vn/vi/e-commerce-logistics-la-gi/)
- [IBM – Service Level Agreement](https://www.ibm.com/think/topics/service-level-agreement)
- [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
- [DATA_CONTRACT.md – Quy ước dữ liệu và nhãn của nhóm](../../docs/DATA_CONTRACT.md)

## 2.2 Khai thác dữ liệu và EDA

### 2.2.1. Khái quát về khai thác dữ liệu và EDA

Khai thác dữ liệu (Data Mining) là quá trình sử dụng các phương pháp thống kê và thuật toán nhằm phát hiện những đặc điểm, quy luật hoặc thông tin hữu ích từ dữ liệu. Trong đề tài này, khai thác dữ liệu giúp nhóm tìm hiểu các thông tin liên quan đến đơn hàng, hoạt động giao nhận và nguy cơ giao hàng trễ.

Phân tích khám phá dữ liệu (Exploratory Data Analysis – EDA) được sử dụng nhằm tìm hiểu cấu trúc, phân phối, chất lượng và những điểm bất thường của dữ liệu trước khi xây dựng mô hình dự đoán.

Đối với bộ dữ liệu Olist, EDA và kiểm tra chất lượng dữ liệu có vai trò hỗ trợ nhận diện các giá trị thiếu, bản ghi trùng, sự khác biệt về kiểu dữ liệu và các trường thông tin cần được xử lý.

Tuy nhiên, kết quả phân tích mô tả chỉ phản ánh những đặc điểm quan sát được trong dữ liệu lịch sử, chưa đủ cơ sở để khẳng định quan hệ nguyên nhân – kết quả.

### 2.2.2. Phương pháp kiểm tra chất lượng dữ liệu thô – T05

Trong nhiệm vụ T05, Ngọc Lan phối hợp với Lam Linh kiểm tra chất lượng của 9 tệp CSV thuộc bộ dữ liệu Brazilian E-Commerce Public Dataset by Olist.

Quá trình kiểm tra được thực hiện bằng thư viện Pandas thông qua các phương thức `read_csv()`, `isna()`, `duplicated()`, `dtypes`, `nunique()`, `describe()` và `value_counts()`.

Nhóm tiến hành thống kê số dòng, số cột, giá trị thiếu, bản ghi trùng, kiểu dữ liệu và một số giá trị bất thường của từng bảng. Các kết quả được tổng hợp thành các bảng QA nhằm cung cấp thông tin trước khi tiến hành làm sạch và tích hợp dữ liệu.

**Bảng 2.1. Tổng hợp kết quả Data Profiling trên 9 bảng Olist**

| Bảng dữ liệu | Số dòng | Số cột | Số ô thiếu | Dòng trùng hoàn toàn |
|---|---:|---:|---:|---:|
| orders | 99.441 | 8 | 4.908 | 0 |
| customers | 99.441 | 5 | 0 | 0 |
| items | 112.650 | 7 | 0 | 0 |
| payments | 103.886 | 5 | 0 | 0 |
| reviews | 99.224 | 7 | 145.903 | 0 |
| products | 32.951 | 9 | 2.448 | 0 |
| sellers | 3.095 | 4 | 0 | 0 |
| geolocation | 1.000.163 | 5 | 0 | 261.831 |
| translation | 71 | 2 | 0 | 0 |

*Nguồn: Kết quả chạy thực tế nhiệm vụ T05, notebook 02 – Ngọc Lan, dữ liệu Olist.*

Từ bảng trên có thể thấy dữ liệu thô có sự khác biệt rõ rệt về quy mô giữa các bảng. Bảng `geolocation` có nhiều bản ghi nhất, trong khi bảng `translation` chỉ có 71 dòng.

Tổng cộng 52 cột dữ liệu đã được kiểm tra. Kết quả cho thấy vấn đề giá trị thiếu tập trung chủ yếu ở các bảng `orders`, `reviews` và `products`. Bảng `geolocation` có số lượng lớn dòng trùng hoàn toàn, cần được xem xét trong quá trình xử lý dữ liệu.

### 2.2.3. Phân tích Missing Values và Duplicate Rows

**a. Giá trị thiếu trong bảng orders**

Bảng `orders` ghi nhận 4.908 ô thiếu, trong đó:

- `order_delivered_customer_date`: 2.965 giá trị thiếu.
- `order_delivered_carrier_date`: 1.783 giá trị thiếu.
- `order_approved_at`: 160 giá trị thiếu.

Các trường này liên quan đến những mốc thời gian trong quá trình xử lý và giao nhận đơn hàng. Vì vậy, cần kiểm tra điều kiện chọn mẫu và tính đầy đủ của thông tin trước khi xác định nhãn giao hàng trễ.

Không thể mặc định mọi giá trị thiếu đều là lỗi, bởi một số đơn hàng có thể chưa hoàn thành quá trình giao nhận tại thời điểm dữ liệu được ghi nhận.

**b. Giá trị thiếu trong bảng reviews**

Bảng `reviews` có 145.903 ô thiếu. Đáng chú ý, trường `review_comment_title` thiếu 87.656 giá trị và `review_comment_message` thiếu 58.247 giá trị.

Đây là những trường bình luận không bắt buộc. Vì vậy, không nên tự động loại bỏ toàn bộ bản ghi chỉ vì khách hàng không nhập tiêu đề hoặc nội dung đánh giá.

Đồng thời, thông tin đánh giá được ghi nhận sau giao dịch không phù hợp để làm đặc trưng đầu vào cho mô hình dự đoán tại thời điểm đơn hàng vừa được phê duyệt.

**c. Giá trị thiếu trong bảng products**

Bảng `products` ghi nhận 2.448 ô thiếu, liên quan đến danh mục sản phẩm, độ dài tên, độ dài mô tả, số lượng ảnh và một số thông số kích thước, trọng lượng.

Việc xử lý những giá trị thiếu này cần dựa trên ý nghĩa của từng thuộc tính. Không nên điền giá trị hoặc loại bỏ bản ghi khi chưa đánh giá ảnh hưởng đến kết quả phân tích.

**d. Bản ghi trùng trong bảng geolocation**

Bảng `geolocation` ghi nhận 261.831 dòng trùng hoàn toàn.

Ngoài vấn đề trùng lặp, bảng địa lý có thể chứa nhiều bản ghi tương ứng với cùng một tiền tố mã bưu chính. Vì vậy, việc sử dụng dữ liệu địa lý cần kiểm tra cấu trúc và tổng hợp phù hợp trước khi kết nối với các bảng khác.

Nếu kết nối trực tiếp các bảng có quan hệ một-nhiều mà không kiểm soát số dòng, kết quả thống kê ở cấp độ đơn hàng có thể bị sai lệch.

Trong nhiệm vụ T05, Ngọc Lan chỉ ghi nhận và báo cáo các vấn đề chất lượng dữ liệu. Công việc làm sạch, tích hợp và xử lý các trường hợp bất thường thuộc quy trình Chương 3 của Lam Linh.

### 2.2.4. Kiểm tra khóa và giá trị bất thường

Ngoài thống kê giá trị thiếu và bản ghi trùng, nhiệm vụ T05 còn thực hiện tám quy tắc kiểm tra chất lượng dữ liệu.

**Bảng 2.2. Kết quả kiểm tra khóa và giá trị bất thường**

| Bảng | Nội dung kiểm tra | Số dòng vi phạm |
|---|---|---:|
| orders | Thiếu `order_id` | 0 |
| orders | Trùng `order_id` | 0 |
| items | Giá sản phẩm âm | 0 |
| items | Phí vận chuyển âm | 0 |
| items | Trùng khóa ghép `order_id`, `order_item_id` | 0 |
| reviews | Điểm đánh giá nằm ngoài 1–5 | 0 |
| payments | Giá trị thanh toán âm | 0 |
| payments | Trùng khóa ghép `order_id`, `payment_sequential` | 0 |

*Nguồn: Bảng `ngoc_lan_t05_checks.csv`, kết quả kiểm tra thực tế của Ngọc Lan.*

Kết quả cho thấy cả tám quy tắc đều không phát hiện dòng vi phạm. Điều này giúp xác nhận một số điều kiện cơ bản về tính hợp lệ của khóa và các giá trị số.

Tuy nhiên, kết quả trên không có nghĩa toàn bộ dữ liệu đã sạch. Các vấn đề khác như giá trị thiếu, dòng trùng của bảng địa lý và tính hợp lệ giữa các mốc thời gian vẫn cần được đánh giá trong quá trình xử lý dữ liệu.

### 2.2.5. Thống kê mô tả và vai trò của EDA

Bên cạnh kiểm tra chất lượng dữ liệu, nhóm còn thống kê mô tả đối với giá sản phẩm, phí vận chuyển, giá trị thanh toán và trạng thái đơn hàng.

Trong kết quả T05, giá sản phẩm có trung vị 74,99 BRL, phí vận chuyển có trung vị 16,26 BRL và giá trị thanh toán có trung vị 100 BRL.

Các giá trị này phản ánh đặc điểm phân phối của những trường dữ liệu tương ứng. Tuy nhiên, giá sản phẩm và phí vận chuyển được thống kê ở cấp bản ghi sản phẩm trong đơn hàng, không phải tổng giá trị mỗi đơn hàng.

Bảng `orders` có 96.478 bản ghi mang trạng thái `delivered` trong dữ liệu thô. Đây chưa phải số lượng đơn cuối cùng được đưa vào mô hình, bởi quá trình chọn mẫu còn yêu cầu đầy đủ thông tin phê duyệt và thời gian giao hàng để xác định nhãn.

Phần phân tích khám phá chuyên sâu, bao gồm phân bố đơn hàng theo thời gian, khu vực khách hàng, người bán và các nhóm giá trị, được Lam Linh thực hiện trong Chương 3.

Kết quả EDA của Chương 3 là cơ sở để nhóm hiểu rõ hơn về dữ liệu và thảo luận các đặc điểm liên quan đến nguy cơ giao hàng trễ. Tuy nhiên, việc lựa chọn đặc trưng cho mô hình vẫn phải tuân theo thời điểm dự báo `order_approved_at` và danh sách đặc trưng đã được thống nhất.

### 2.2.6. Kết luận kết quả kiểm tra dữ liệu T05

Nhiệm vụ T05 đã hoàn thành việc kiểm tra chất lượng dữ liệu thô trên đầy đủ 9 bảng CSV Olist, với tổng cộng 52 cột.

Kết quả ghi nhận các vấn đề đáng chú ý gồm giá trị thiếu ở bảng `orders`, `reviews`, `products` và 261.831 dòng trùng hoàn toàn trong bảng `geolocation`. Đồng thời, tám quy tắc kiểm tra khóa và giá trị bất thường không phát hiện dòng vi phạm.

Các kết quả được lưu thành ba tệp:

- [Bảng tổng hợp QA](../tables/ngoc_lan_t05_summary.csv)
- [Bảng QA theo từng cột](../tables/ngoc_lan_t05_columns.csv)
- [Bảng kiểm tra giá trị bất thường](../tables/ngoc_lan_t05_checks.csv)

Những bảng này được sử dụng để đối chiếu chất lượng dữ liệu với Lam Linh. Ngọc Lan không tự ý thay đổi dữ liệu gốc hoặc thực hiện lại nhiệm vụ làm sạch, tích hợp và xây dựng nhãn đã được phân công cho Chương 3.

*Nguồn dữ liệu: [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce). Mã nguồn và kết quả thực nghiệm được trình bày trong [Notebook Chương 2 – Ngọc Lan](../../notebooks/02_NGOC_LAN_chuong_2.ipynb).*

## 2.3 Thuật toán ML và DL

### 2.3.1. Tổng quan về học máy và bài toán phân loại nhị phân

Học máy (Machine Learning – ML) là một lĩnh vực của trí tuệ nhân tạo, trong đó mô hình được xây dựng để học các quy luật từ dữ liệu và đưa ra dự đoán đối với những trường hợp mới.

Trong đề tài "Phân tích dữ liệu đơn hàng và dự đoán nguy cơ giao hàng trễ trong thương mại điện tử", nhóm sử dụng phương pháp học có giám sát (Supervised Learning) để giải quyết bài toán phân loại nhị phân.

Biến mục tiêu của bài toán là `is_late`, gồm hai giá trị:

- `is_late = 0`: Đơn hàng không giao trễ.
- `is_late = 1`: Đơn hàng giao trễ.

Mục tiêu của mô hình là ước lượng xác suất một đơn hàng có nguy cơ giao trễ dựa trên những thông tin đã có tại thời điểm đơn được phê duyệt (`order_approved_at`).

Nhóm lựa chọn ba phương pháp gồm Dummy Classifier, Random Forest và mạng nơ-ron đa lớp MLP. Trong đó, Dummy Classifier đóng vai trò mô hình tham chiếu, còn Random Forest và MLP được sử dụng để nghiên cứu khả năng học từ dữ liệu.

### 2.3.2. Thuật toán Dummy Classifier

Dummy Classifier là mô hình phân loại đơn giản, thường được sử dụng để tạo mức kết quả tham chiếu (Baseline) khi đánh giá các thuật toán học máy.

Khác với những mô hình học các mối quan hệ giữa đặc trưng và nhãn, Dummy Classifier đưa ra dự đoán theo một quy tắc cố định, chẳng hạn dự đoán lớp phổ biến nhất hoặc sử dụng tỷ lệ xuất hiện của các lớp trong dữ liệu huấn luyện.

Trong bài toán Olist, Dummy Classifier giúp xác định mức đánh giá cơ sở. Nếu một mô hình phức tạp như Random Forest hoặc MLP không cải thiện được kết quả so với Dummy, nhóm cần xem xét lại hiệu quả của mô hình.

Do dữ liệu có sự mất cân bằng giữa đơn giao trễ và không giao trễ, việc sử dụng mô hình tham chiếu đặc biệt cần thiết để tránh đánh giá quá cao hiệu quả chỉ dựa trên Accuracy.

Theo phân công của nhóm, **Trúc Chi là thành viên trực tiếp huấn luyện Dummy Classifier** trên tập Train chung và cung cấp kết quả Validation để so sánh với các mô hình còn lại.

Ngọc Lan không huấn luyện lại Dummy trong notebook Chương 2 mà chỉ sử dụng kết quả tham chiếu phù hợp khi nhận xét Random Forest.

### 2.3.3. Thuật toán Random Forest

Random Forest là thuật toán học tập kết hợp (Ensemble Learning), được giới thiệu bởi Breiman (2001). Thuật toán sử dụng nhiều cây quyết định để tạo ra kết quả dự đoán chung, thay vì chỉ phụ thuộc vào một cây.

Trong quá trình huấn luyện, Random Forest sử dụng kỹ thuật Bootstrap Sampling, tức là lấy mẫu ngẫu nhiên có hoàn lại từ dữ liệu huấn luyện để xây dựng các cây quyết định. Bên cạnh đó, thuật toán sử dụng cơ chế lựa chọn ngẫu nhiên tập đặc trưng tại những lần phân chia nút.

Đối với bài toán phân loại, xác suất dự đoán của Random Forest được xác định bằng cách tổng hợp xác suất từ các cây trong mô hình.

**Ưu điểm của Random Forest:**

- Có khả năng học các mối quan hệ phi tuyến giữa đặc trưng và biến mục tiêu.
- Phù hợp để thử nghiệm trên dữ liệu dạng bảng.
- Có thể kết hợp với các phương pháp xử lý giá trị thiếu và mã hóa biến phân loại trong Pipeline.
- Việc kết hợp nhiều cây giúp giảm sự phụ thuộc vào một cây quyết định riêng lẻ.

**Hạn chế của Random Forest:**

- Có thể tiêu tốn thời gian huấn luyện và bộ nhớ khi số lượng cây lớn.
- Hiệu quả phụ thuộc vào cấu hình siêu tham số và đặc điểm dữ liệu.
- Có thể tạo nhiều cảnh báo sai khi áp dụng cho dữ liệu mất cân bằng.
- Kết quả dự đoán chưa phản ánh trực tiếp nguyên nhân khiến đơn hàng giao trễ.

Trong đồ án, Ngọc Lan được phân công trực tiếp huấn luyện và tinh chỉnh Random Forest trên tập Train chung. Việc lựa chọn cấu hình và ngưỡng phân loại được thực hiện trên Validation, không sử dụng Test.

### 2.3.4. Mạng nơ-ron đa lớp MLP

Multi-Layer Perceptron (MLP) là mô hình mạng nơ-ron nhân tạo gồm lớp đầu vào, một hoặc nhiều lớp ẩn và lớp đầu ra.

Mỗi nơ-ron tiếp nhận thông tin từ lớp trước, thực hiện phép tính có trọng số và sử dụng hàm kích hoạt để tạo ra đầu ra.

Quá trình huấn luyện MLP sử dụng phương pháp lan truyền ngược (Backpropagation) kết hợp thuật toán tối ưu nhằm điều chỉnh trọng số và giảm sai số dự đoán.

MLP có khả năng học các mối quan hệ phi tuyến phức tạp. Tuy nhiên, hiệu quả của mô hình phụ thuộc vào kiến trúc mạng, tốc độ học, số vòng lặp và cách xử lý dữ liệu đầu vào.

Đối với dữ liệu dạng bảng, các đặc trưng số thường cần được chuẩn hóa, còn các biến phân loại cần được mã hóa phù hợp trước khi đưa vào mô hình.

Trong đồ án, MLP được sử dụng để so sánh với Random Forest trên cùng bộ dữ liệu và cùng giao thức chia tập.

**Tấn Lên là thành viên trực tiếp huấn luyện MLP** trong notebook 01. Kết quả của mô hình này sẽ được bàn giao cho Trúc Chi để tích hợp và so sánh trên Validation.

Ngọc Lan chỉ trình bày cơ sở lý thuyết của MLP trong Chương 2, không thực hiện huấn luyện lại mô hình này.

### 2.3.5. Phương pháp xây dựng và huấn luyện Random Forest trên dữ liệu Olist

**a. Dữ liệu đầu vào và cách chia tập**

Mô hình Random Forest được huấn luyện trên dữ liệu đã được Lam Linh xử lý và chuyển về cấp độ đơn hàng. 

Ba tập sau chia có tổng cộng 91.436 đơn hàng, gồm 64.416 mẫu Train, 12.551 mẫu Validation và 14.469 mẫu Test.

Số lượng này thấp hơn 96.456 dòng của tập model-ready ở Chương 3. Nguyên nhân là quy trình `get_shared_splits()` kiểm tra tính hợp lệ của thời gian, nhãn và áp dụng điều kiện nhãn đã trưởng thành tại các mốc chia tập (label maturity).

Số lượng mẫu bị loại theo từng điều kiện cần được đối chiếu với kết quả chia tập của Trúc Chi trước khi nghiệm thu chính thức.


Nhóm sử dụng bộ chia dữ liệu chung do Trúc Chi quản lý, với mã định danh:

`split_id = 72c64fdd7b6de725a531`

Số lượng mẫu trong các tập được sử dụng như sau:

| Tập dữ liệu | Số đơn hàng | Vai trò |
|---|---:|---|
| Train | 64.416 | Huấn luyện Random Forest |
| Validation | 12.551 | Lựa chọn cấu hình và đánh giá trong quá trình phát triển |
| Test | 14.469 | Dành cho đánh giá độc lập của Vĩnh Chi |

Mô hình chỉ được huấn luyện trên Train. Tập Validation được sử dụng để lựa chọn siêu tham số và ngưỡng phân loại, trong khi Test không được dùng để điều chỉnh mô hình.

**b. Lựa chọn đặc trưng đầu vào**

Nhóm sử dụng năm đặc trưng đã được thống nhất trong giao thức thực nghiệm:

| Đặc trưng | Ý nghĩa |
|---|---|
| `purchase_month_number` | Tháng đặt hàng |
| `purchase_weekday` | Thứ trong tuần khi đặt hàng |
| `purchase_hour` | Giờ đặt hàng |
| `approval_delay_hours` | Thời gian từ khi đặt đến khi đơn được phê duyệt |
| `customer_state` | Bang nhận hàng của khách |

Các thông tin chỉ xuất hiện sau thời điểm phê duyệt, như ngày giao hàng thực tế hoặc đánh giá sau giao dịch, không được sử dụng làm đặc trưng dự đoán.

**c. Xây dựng Pipeline tiền xử lý**

Trong notebook, Ngọc Lan sử dụng `Pipeline` và `ColumnTransformer` của thư viện scikit-learn để kết hợp các bước tiền xử lý với Random Forest.

Đối với các đặc trưng số, giá trị thiếu được xử lý bằng `SimpleImputer(strategy="median")`.

Đối với biến phân loại, nhóm sử dụng `SimpleImputer(strategy="most_frequent")`, sau đó mã hóa bằng `OneHotEncoder(handle_unknown="ignore")`.

Quá trình tiền xử lý được học từ tập Train thông qua Pipeline. Khi đánh giá trên Validation, nhóm chỉ sử dụng mô hình và các bước tiền xử lý đã được huấn luyện, không fit lại trên Validation.

Cách thực hiện này giúp giảm nguy cơ rò rỉ thông tin giữa các tập dữ liệu.

**d. Thiết lập cấu hình Random Forest**

Các tham số được sử dụng trong thực nghiệm gồm:

| Tham số | Giá trị | Mục đích |
|---|---|---|
| `n_estimators` | 200 | Sử dụng 200 cây quyết định |
| `class_weight` | `balanced_subsample` | Điều chỉnh trọng số các lớp theo từng mẫu bootstrap |
| `random_state` | 42 | Cố định yếu tố ngẫu nhiên để hỗ trợ tái lập |
| `min_samples_leaf` | 2, 5, 10 | So sánh ảnh hưởng của số mẫu tối thiểu tại nút lá |

Tham số `n_estimators=200` được giữ cố định trong ba cấu hình thử nghiệm. Nhóm sử dụng `class_weight="balanced_subsample"` nhằm điều chỉnh trọng số giữa hai lớp trong điều kiện dữ liệu mất cân bằng.

Tham số `random_state=42` được sử dụng để kiểm soát yếu tố ngẫu nhiên trong quá trình huấn luyện.

Đối với `min_samples_leaf`, nhóm thử nghiệm ba giá trị 2, 5 và 10. Tham số này quy định số mẫu tối thiểu tại một nút lá, qua đó ảnh hưởng đến độ phức tạp của cây quyết định.

**e. Kết quả lựa chọn cấu hình bằng Validation**

Sau khi huấn luyện ba cấu hình trên cùng tập Train, nhóm tính Average Precision (AP) trên Validation để lựa chọn mô hình.

| `min_samples_leaf` | AP Validation |
|---|---:|
| 2 | 0,055444 |
| 5 | 0,058271 |
| 10 | **0,067137** |

*Nguồn: Kết quả chạy thực tế notebook 02 – Ngọc Lan.*

Kết quả cho thấy `min_samples_leaf=10` đạt AP Validation cao nhất trong ba cấu hình đã thử.

Vì vậy, nhóm lựa chọn Random Forest với 200 cây và `min_samples_leaf=10` làm mô hình chính để tiếp tục đánh giá.

Việc lựa chọn này chỉ phản ánh cấu hình tốt nhất trong phạm vi ba giá trị đã thử nghiệm, không có nghĩa đây là cấu hình tối ưu trong mọi trường hợp.

**f. Lưu mô hình và bàn giao**

Sau khi hoàn thành huấn luyện và đánh giá Validation, Ngọc Lan lưu lại ba tệp:

- `models/ngoc_lan_random_forest.joblib`: Pipeline Random Forest đã huấn luyện.
- `data/processed/rf_val_predictions.csv`: Mã đơn hàng, nhãn thực tế và xác suất dự đoán trên Validation.
- `data/processed/rf_metadata.json`: Thông tin cấu hình, đặc trưng, split và kết quả Validation.

Mô hình đã được kiểm tra nạp lại trên máy huấn luyện và tái lập xác suất Validation với sai lệch lớn nhất khoảng `2,22 × 10⁻¹⁶`.

Kết quả kiểm tra này xác nhận khả năng tái lập cục bộ của artifact. Việc bàn giao và xác nhận độc lập của Trúc Chi là bước nghiệm thu tiếp theo.

### 2.3.6. Nhận xét và giới hạn phương pháp

Qua quá trình thực nghiệm, Random Forest đã được huấn luyện thành công trên tập Train chung, sử dụng đúng năm đặc trưng và lựa chọn cấu hình theo AP Validation.

Việc đặt tiền xử lý và bộ phân loại trong cùng Pipeline giúp thống nhất cách xử lý dữ liệu khi huấn luyện, đánh giá và nạp lại mô hình.

Tuy nhiên, chất lượng của Random Forest vẫn phụ thuộc vào khả năng biểu diễn thông tin của năm đặc trưng đầu vào. Ngoài ra, dữ liệu giao hàng trễ có sự mất cân bằng giữa hai lớp nên cần đánh giá thêm Precision, Recall, F1-score, số cảnh báo sai và Top-K.

Kết quả đánh giá chi tiết của Random Forest được trình bày tại mục 2.4. Việc so sánh chính thức giữa Dummy, Random Forest và MLP sẽ do Trúc Chi tích hợp trên Validation, trước khi Vĩnh Chi thực hiện đánh giá độc lập trên Test.

**Nguồn tham khảo:**

- Breiman, L. (2001). *Random Forests*. https://doi.org/10.1023/A:1010933404324
- Scikit-learn – DummyClassifier: https://scikit-learn.org/stable/modules/generated/sklearn.dummy.DummyClassifier.html
- Scikit-learn – Ensemble Methods: https://scikit-learn.org/stable/modules/ensemble.html
- Scikit-learn – Neural Network Models: https://scikit-learn.org/stable/modules/neural_networks_supervised.html
- [Giao thức thực nghiệm GR02](../../docs/EXPERIMENT_PROTOCOL.md)
- [Notebook thực nghiệm Random Forest – Ngọc Lan](../../notebooks/02_NGOC_LAN_chuong_2.ipynb)

## 2.4 Độ đo cho dữ liệu mất cân bằng

### 2.4.1. Dữ liệu mất cân bằng trong bài toán phân loại

Dữ liệu mất cân bằng (Imbalanced Data) xảy ra khi số lượng mẫu giữa các lớp có sự chênh lệch đáng kể. Trong bài toán dự đoán giao hàng trễ, số đơn giao trễ thường ít hơn số đơn giao đúng hạn.

Đối với tập Validation được nhóm sử dụng, có tổng cộng 12.551 đơn hàng, trong đó 539 đơn giao trễ và 12.012 đơn không giao trễ. Tỷ lệ đơn giao trễ chiếm khoảng 4,29%.

Sự mất cân bằng này khiến việc chỉ sử dụng Accuracy để đánh giá mô hình có thể gây hiểu nhầm. Ví dụ, một mô hình luôn dự đoán tất cả đơn hàng không trễ vẫn có Accuracy cao nhưng không phát hiện được đơn giao trễ nào.

Vì vậy, nhóm lựa chọn các độ đo phù hợp hơn gồm Precision, Recall, F1-score, Average Precision (AP), False Positive (FP) và Top-K để đánh giá Random Forest.

### 2.4.2. Ma trận nhầm lẫn (Confusion Matrix)

Confusion Matrix được sử dụng để so sánh kết quả dự đoán của mô hình với nhãn thực tế.

Trong bài toán của nhóm, lớp dương (Positive) là đơn giao trễ và lớp âm (Negative) là đơn không giao trễ.

Bốn trường hợp của ma trận nhầm lẫn gồm:

- **True Positive (TP):** Đơn thực tế giao trễ và được mô hình dự đoán giao trễ.
- **True Negative (TN):** Đơn thực tế không trễ và được dự đoán đúng.
- **False Positive (FP):** Đơn thực tế không trễ nhưng bị cảnh báo giao trễ.
- **False Negative (FN):** Đơn thực tế giao trễ nhưng mô hình không phát hiện được.

**Bảng 2.3. Confusion Matrix của Random Forest trên Validation**

| Nhãn thực tế | Dự đoán không trễ (0) | Dự đoán giao trễ (1) |
|---|---:|---:|
| Không giao trễ (0) | TN = 8.822 | FP = 3.190 |
| Giao trễ (1) | FN = 317 | TP = 222 |

*Nguồn: Kết quả chạy thực tế Random Forest trên tập Validation trong notebook 02.*

Từ bảng trên, mô hình nhận diện đúng 222 đơn giao trễ nhưng bỏ sót 317 đơn giao trễ. Đồng thời, có 3.190 đơn thực tế không trễ bị mô hình cảnh báo sai.

Tổng số mẫu trong Confusion Matrix là 12.551, khớp với quy mô của tập Validation.

Kết quả này cho thấy Random Forest có khả năng nhận diện một phần đơn hàng giao trễ, nhưng vẫn tạo ra số lượng cảnh báo sai đáng kể.

### 2.4.3. Precision, Recall và F1-score

**a. Precision**

Precision thể hiện tỷ lệ dự đoán giao trễ đúng trong tổng số đơn hàng được mô hình cảnh báo giao trễ.

Công thức:

`Precision = TP / (TP + FP)`

Với kết quả Random Forest:

`Precision = 222 / (222 + 3190) = 0,065064`

Precision đạt khoảng **6,51%**.

Điều này có nghĩa là trong những đơn được mô hình cảnh báo giao trễ, chỉ khoảng 6,51% thực sự giao trễ.

Kết quả Precision thấp cho thấy mô hình còn tạo ra nhiều cảnh báo sai, gây hạn chế nếu áp dụng trực tiếp vào quy trình vận hành.

**b. Recall**

Recall thể hiện tỷ lệ đơn giao trễ được phát hiện đúng trong tổng số đơn thực tế giao trễ.

Công thức:

`Recall = TP / (TP + FN)`

Với kết quả thực nghiệm:

`Recall = 222 / (222 + 317) = 0,411874`

Recall đạt khoảng **41,19%**.

Điều này cho thấy Random Forest phát hiện được khoảng 41,19% số đơn giao trễ thực tế trong tập Validation, đồng thời vẫn bỏ sót khoảng 58,81%.

**c. F1-score**

F1-score là trung bình điều hòa của Precision và Recall, phản ánh sự cân bằng giữa hai chỉ số.

Công thức:

`F1 = 2 × Precision × Recall / (Precision + Recall)`

Kết quả mô hình:

`F1-score = 0,112377`

Giá trị F1-score cho thấy hiệu quả kết hợp giữa khả năng cảnh báo chính xác và khả năng phát hiện đơn trễ vẫn còn hạn chế.

Nguyên nhân chủ yếu là Precision thấp, mặc dù Recall đã nhận diện được một phần các đơn thuộc lớp giao trễ.

### 2.4.4. Precision–Recall Curve và Average Precision

Precision–Recall Curve (PR Curve) thể hiện mối quan hệ giữa Precision và Recall khi thay đổi ngưỡng phân loại.

Đối với bài toán có dữ liệu mất cân bằng, PR Curve giúp quan sát trực tiếp khả năng phát hiện lớp dương và sự đánh đổi giữa số cảnh báo đúng với số cảnh báo sai.

Average Precision (AP) là chỉ số tổng hợp chất lượng xếp hạng dựa trên đường Precision–Recall. Theo cách tính của scikit-learn, AP được xác định từ tổng có trọng số của các giá trị Precision tương ứng với mức tăng Recall.

Cần phân biệt AP với diện tích PR-AUC tính bằng phương pháp hình thang, vì hai cách tính có thể cho kết quả khác nhau.

Trong thực nghiệm, nhóm sử dụng `average_precision_score` của scikit-learn để đánh giá và lựa chọn cấu hình Random Forest.

Sau khi huấn luyện ba cấu hình với `min_samples_leaf` lần lượt bằng 2, 5 và 10, kết quả AP Validation như sau:

| `min_samples_leaf` | AP Validation |
|---|---:|
| 2 | 0,055444 |
| 5 | 0,058271 |
| 10 | **0,067137** |

Cấu hình `min_samples_leaf=10` đạt AP cao nhất trong ba cấu hình đã thử nên được nhóm lựa chọn để tiếp tục đánh giá.

Kết quả AP = 0,067137 phản ánh khả năng xếp hạng nguy cơ giao hàng trễ của mô hình trên tập Validation. Tuy nhiên, chỉ số này chưa đủ để kết luận mô hình có thể triển khai hiệu quả trong thực tế mà cần xem xét thêm Precision, Recall và chi phí cảnh báo sai.

### 2.4.5. False Positive và đánh giá Top-K

**a. False Positive**

False Positive (FP) là trường hợp mô hình dự đoán một đơn hàng có nguy cơ giao trễ nhưng thực tế đơn hàng được giao đúng hạn.

Trong ứng dụng thực tế, cảnh báo sai có thể khiến doanh nghiệp phải dành nguồn lực kiểm tra những đơn hàng không thực sự cần can thiệp.

Với ngưỡng phân loại 0,25, Random Forest tạo ra:

- 222 cảnh báo đúng (TP).
- 3.190 cảnh báo sai (FP).
- Tổng cộng 3.412 đơn được cảnh báo có nguy cơ giao trễ.

Như vậy, phần lớn các cảnh báo tại ngưỡng này không chính xác. Nếu doanh nghiệp kiểm tra tất cả 3.412 đơn được cảnh báo, khối lượng xử lý có thể lớn so với số đơn giao trễ thực sự được phát hiện.

Tuy nhiên, việc tăng ngưỡng để giảm FP có thể khiến mô hình bỏ sót thêm đơn giao trễ. Do đó, lựa chọn ngưỡng cần xem xét sự đánh đổi giữa Precision và Recall, thay vì chỉ tập trung giảm cảnh báo sai.

**b. Đánh giá Top-K**

Top-K là phương pháp sắp xếp đơn hàng theo xác suất giao trễ dự đoán từ cao xuống thấp, sau đó lựa chọn K đơn đứng đầu để ưu tiên theo dõi.

Các chỉ số được sử dụng gồm:

`Precision@K = Số đơn giao trễ thực tế trong Top-K / K`

`Recall@K = Số đơn giao trễ thực tế trong Top-K / Tổng số đơn giao trễ`

**Bảng 2.4. Kết quả đánh giá Top-K của Random Forest trên Validation**

| K | TP@K | FP@K | Precision@K | Recall@K |
|---|---:|---:|---:|---:|
| 50 | 9 | 41 | 18,00% | 1,67% |
| 100 | 14 | 86 | 14,00% | 2,60% |
| 200 | 27 | 173 | 13,50% | 5,01% |

*Nguồn: Kết quả chạy thực tế Random Forest trên tập Validation trong notebook 02.*

Kết quả cho thấy khi lựa chọn 50 đơn hàng có điểm nguy cơ cao nhất, mô hình phát hiện đúng 9 đơn giao trễ, đạt Precision@50 = 18%.

Khi mở rộng danh sách lên 100 và 200 đơn, số đơn giao trễ được phát hiện tăng lên lần lượt là 14 và 27. Tuy nhiên, Precision@K giảm tương ứng.

Điều này cho thấy việc mở rộng số lượng đơn ưu tiên có thể giúp phát hiện thêm đơn trễ nhưng đồng thời làm tăng số cảnh báo sai.

Top-K có thể là một hướng hỗ trợ vận hành trong trường hợp doanh nghiệp chỉ có khả năng kiểm tra một số lượng đơn hàng giới hạn. Tuy nhiên, khả năng áp dụng cần được đánh giá thêm trên dữ liệu độc lập.

### 2.4.6. Kết quả đánh giá tổng hợp Random Forest trên Validation

Sau quá trình huấn luyện và lựa chọn cấu hình, nhóm sử dụng Random Forest với các tham số:

- `n_estimators=200`
- `min_samples_leaf=10`
- `class_weight="balanced_subsample"`
- `random_state=42`

Theo giao thức thực nghiệm trong `src/experiment.py`, nhóm thử nghiệm 17 ngưỡng phân loại từ 0,10 đến 0,90 với bước tăng 0,05 trên tập Validation.

Ngưỡng được lựa chọn dựa trên F1-score cao nhất. Trường hợp nhiều ngưỡng có cùng F1-score, nhóm ưu tiên ngưỡng có số False Positive thấp hơn.

Kết quả thực nghiệm cho thấy ngưỡng 0,25 được lựa chọn cho Random Forest trên Validation.

**Bảng 2.5. Tổng hợp kết quả Random Forest trên Validation**

| Chỉ số | Kết quả |
|---|---:|
| Số đơn Validation | 12.551 |
| Số đơn giao trễ thực tế | 539 |
| AP | 0,067137 |
| Precision | 0,065064 |
| Recall | 0,411874 |
| F1-score | 0,112377 |
| Threshold | 0,25 |
| TP | 222 |
| FP | 3.190 |
| FN | 317 |
| TN | 8.822 |
| Precision@50 | 0,180 |
| Precision@100 | 0,140 |
| Precision@200 | 0,135 |

*Nguồn: Notebook 02 – Ngọc Lan, kết quả đánh giá trên Validation; split_id = `72c64fdd7b6de725a531`.*

Các kết quả cho thấy Random Forest có khả năng nhận diện một phần các đơn hàng giao trễ, nhưng hiệu quả phân loại tại ngưỡng lựa chọn chưa cao.

Đặc biệt, Precision = 6,51% và FP = 3.190 cho thấy số lượng cảnh báo sai là vấn đề đáng chú ý nếu sử dụng mô hình để hỗ trợ nhân viên giám sát đơn hàng.

Ngược lại, các kết quả Top-K cho thấy việc lựa chọn một danh sách nhỏ theo điểm nguy cơ có thể mang lại tỷ lệ cảnh báo đúng cao hơn so với việc kiểm tra tất cả các đơn vượt ngưỡng 0,25.

### 2.4.7. So sánh với Dummy Classifier và hạn chế thực tế

Trong bài toán này, Dummy Classifier được sử dụng làm mô hình tham chiếu.

Với chiến lược dự đoán xác suất không đổi theo tỷ lệ lớp trong Train (`strategy="prior"`), AP tham chiếu trên Validation bằng tỷ lệ lớp giao trễ của tập này, xấp xỉ 0,042945.

Trong khi đó, Random Forest đạt AP = 0,067137, cao hơn mức tham chiếu khoảng 0,024192.

Kết quả cho thấy Random Forest đã học được một phần thông tin có ích để xếp hạng nguy cơ giao trễ thay vì đưa ra xác suất giống nhau cho mọi đơn hàng.

Tuy nhiên, đây mới là so sánh với mức AP tham chiếu của Dummy theo chiến lược `prior`. Kết quả so sánh chính thức giữa Dummy, Random Forest và MLP cần được đối chiếu với các mô hình thực tế do Trúc Chi tích hợp trên cùng Validation.

**Hạn chế của Random Forest**

Thứ nhất, số lượng cảnh báo sai vẫn cao. Tại ngưỡng 0,25, mô hình đưa ra 3.190 cảnh báo sai, gây khó khăn nếu doanh nghiệp phải kiểm tra toàn bộ các đơn được dự đoán có nguy cơ giao trễ.

Thứ hai, Recall đạt 41,19%, nghĩa là mô hình vẫn bỏ sót hơn một nửa số đơn thực tế giao trễ. Vì vậy, không thể sử dụng kết quả này như một hệ thống cảnh báo đầy đủ.

Thứ ba, mô hình chỉ sử dụng năm đặc trưng đầu vào đã được nhóm kiểm tra về thời điểm xuất hiện. Cách tiếp cận này giúp hạn chế rò rỉ dữ liệu nhưng cũng giới hạn lượng thông tin có thể sử dụng để dự đoán.

Thứ tư, dữ liệu nghiên cứu thuộc giai đoạn 2016–2018 tại Brazil và chỉ bao gồm những đơn đủ điều kiện xác định nhãn. Vì vậy, kết quả chưa thể khái quát trực tiếp cho mọi đơn hàng hoặc các hệ thống thương mại điện tử hiện nay.

**Kết luận**

Random Forest đã hoàn thành quá trình huấn luyện và đánh giá trên tập Validation theo giao thức chung của nhóm.

Mô hình đạt AP = 0,067137, cao hơn mức tham chiếu Dummy xấp xỉ 0,042945 nhưng vẫn còn hạn chế về Precision, Recall và số cảnh báo sai.

Vì vậy, kết quả hiện tại phù hợp với mục tiêu nghiên cứu, đánh giá và thử nghiệm khả năng hỗ trợ ưu tiên đơn hàng, chưa đủ cơ sở để khẳng định mô hình sẵn sàng triển khai thực tế.

Toàn bộ số liệu trình bày trong mục này là kết quả trên Validation. Việc đánh giá cuối cùng trên tập Test được thực hiện độc lập bởi Vĩnh Chi trong Chương 5.

**Nguồn tham khảo:**

- [Scikit-learn – Precision, Recall và F1-score](https://scikit-learn.org/stable/modules/model_evaluation.html)
- [Scikit-learn – Average Precision](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.average_precision_score.html)
- [Scikit-learn – DummyClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.dummy.DummyClassifier.html)
- [Notebook thực nghiệm RF – Ngọc Lan](../../notebooks/02_NGOC_LAN_chuong_2.ipynb)
- [Giao thức thực nghiệm GR02](../../docs/EXPERIMENT_PROTOCOL.md)

## 2.5 Công trình liên quan

### 2.5.1. Nghiên cứu của Salari và cộng sự (2022)

**Tên công trình:** *Real-Time Delivery Time Forecasting and Promising in Online Retailing: When Will Your Package Arrive?*

**Tác giả:** Nooshin Salari, Sheng Liu và Zuo-Jun Max Shen (2022).

**Nguồn:** https://doi.org/10.1287/msom.2022.1081

**Mục tiêu nghiên cứu**

Salari và cộng sự (2022) nghiên cứu việc dự báo thời gian giao hàng trong thương mại điện tử nhằm hỗ trợ doanh nghiệp đưa ra ngày giao hàng cam kết phù hợp với khách hàng.

Nghiên cứu nhấn mạnh rằng việc dự báo thời gian giao hàng không chỉ liên quan đến độ chính xác mà còn ảnh hưởng đến sự hài lòng của khách hàng và hiệu quả kinh doanh.

**Dữ liệu và phương pháp**

Các tác giả sử dụng dữ liệu thực tế từ nền tảng thương mại điện tử JD.com.

Nghiên cứu áp dụng các phương pháp dự báo dựa trên cây quyết định và mở rộng Quantile Regression Forest để ước lượng phân phối thời gian giao hàng.

Từ kết quả dự báo, nhóm nghiên cứu xây dựng quy tắc lựa chọn ngày giao hàng cam kết có xét đến chi phí và tác động đến hoạt động bán hàng.

**Kết quả nghiên cứu**

Kết quả mô phỏng cho thấy chính sách cam kết giao hàng được đề xuất có khả năng cải thiện doanh số khoảng 6,1% so với chính sách hiện tại.

Điều này cho thấy dự báo thời gian giao hàng có thể mang lại giá trị hỗ trợ quyết định vận hành, thay vì chỉ phục vụ mục đích dự đoán.

**Hạn chế**

Công trình tập trung vào dự báo thời gian giao hàng và tối ưu ngày cam kết, không trực tiếp giải quyết bài toán phân loại nhị phân đơn hàng giao trễ.

Ngoài ra, dữ liệu JD.com và điều kiện vận hành của nền tảng này có thể khác với bộ dữ liệu Olist.

**Khả năng áp dụng vào đồ án**

Nghiên cứu giúp nhóm nhận thấy vai trò của việc dự báo sớm đối với hoạt động logistics.

Trong đồ án Olist, nhóm lựa chọn thời điểm `order_approved_at` để dự đoán nguy cơ giao hàng trễ. Kết quả dự đoán được kỳ vọng hỗ trợ nhận diện và ưu tiên theo dõi các đơn hàng có nguy cơ cao.

Tuy nhiên, nhóm không trực tiếp áp dụng thuật toán tối ưu ngày giao cam kết của nghiên cứu này.

### 2.5.2. Nghiên cứu của Saini và cộng sự (2026)

**Tên công trình:** *Interpretable and Leakage-Aware Prediction of Shipment Delays in Global Supply Chains: A Random Forest–SHAP Workflow with Multi-Model Benchmarking on the DataCo Dataset.*

**Tác giả:** Divyansh Saini, Harman Singh và Bhavya Agarwal (2026).

**Nguồn:** https://doi.org/10.1108/MSCRA-04-2026-0035

**Mục tiêu nghiên cứu**

Saini và cộng sự (2026) nghiên cứu việc dự đoán độ trễ xuất hàng trong chuỗi cung ứng, đồng thời tập trung kiểm soát hiện tượng rò rỉ dữ liệu (Data Leakage).

Các tác giả cho rằng một mô hình có thể đạt kết quả đánh giá rất cao nhưng không phản ánh đúng khả năng dự đoán thực tế nếu sử dụng những thông tin chỉ xuất hiện sau thời điểm cần dự báo.

**Dữ liệu và phương pháp**

Nghiên cứu sử dụng 172.765 bản ghi vận chuyển đã hoàn thành từ bộ dữ liệu DataCo.

Các tác giả kiểm tra thời điểm xuất hiện của từng đặc trưng để xác định thông tin có thể sử dụng hợp lệ tại thời điểm đặt hàng.

Sau khi kiểm soát rò rỉ dữ liệu, nhóm nghiên cứu huấn luyện và so sánh nhiều mô hình, trong đó có Random Forest, đồng thời sử dụng SHAP để phân tích khả năng giải thích của mô hình.

**Kết quả nghiên cứu**

Random Forest khi chỉ sử dụng những đặc trưng hợp lệ tại thời điểm dự báo đạt R² = 0,2719.

Khi bổ sung những thông tin hậu nghiệm, kết quả R² tăng lên 0,7589. Mức chênh lệch 0,4870 cho thấy dữ liệu rò rỉ có thể làm tăng đáng kể hiệu quả đánh giá biểu kiến của mô hình.

Kết quả nhấn mạnh tầm quan trọng của việc kiểm tra thời điểm xuất hiện của đặc trưng trước khi huấn luyện.

**Hạn chế**

Nghiên cứu sử dụng bộ dữ liệu DataCo và tập trung vào dự đoán độ trễ xuất hàng theo phương pháp hồi quy.

Trong khi đó, đồ án Olist của nhóm giải quyết bài toán phân loại nguy cơ giao hàng trễ. Vì vậy, không thể so sánh trực tiếp R² trong nghiên cứu với AP hoặc F1-score của Random Forest trên Olist.

**Khả năng áp dụng vào đồ án**

Đây là công trình có ý nghĩa trực tiếp đối với phương pháp xây dựng mô hình của nhóm.

Nhóm chọn thời điểm dự báo `order_approved_at` và chỉ sử dụng năm đặc trưng đã được kiểm tra về khả năng xuất hiện tại thời điểm đó.

Những thông tin hậu giao như `order_delivered_customer_date`, `order_delivered_carrier_date` và `review_score` không được sử dụng làm đặc trưng đầu vào.

Ngoài ra, Random Forest chỉ được huấn luyện trên Train, lựa chọn cấu hình và ngưỡng phân loại bằng Validation. Test được giữ độc lập cho giai đoạn đánh giá cuối cùng.

### 2.5.3. Nghiên cứu của Zhang và cộng sự (2026)

**Tên công trình:** *A Deep Tabular Learning Framework for E-Commerce Delivery Delay Prediction and Cost-Sensitive Operational Risk Mitigation.*

**Tác giả:** Yuxuan Zhang, Yangxin Wang và Yuanyuan Wang (2026).

**Nguồn:** https://doi.org/10.3390/a19070597

**Mục tiêu nghiên cứu**

Zhang và cộng sự (2026) nghiên cứu việc ứng dụng mô hình học sâu trên dữ liệu dạng bảng để dự đoán nguy cơ giao hàng trễ trong thương mại điện tử.

Bên cạnh khả năng dự đoán, nghiên cứu còn xem xét cách sử dụng kết quả mô hình nhằm hỗ trợ các quyết định vận hành có tính đến chi phí.

**Dữ liệu và phương pháp**

Nghiên cứu sử dụng dữ liệu logistics thương mại điện tử công khai trên Kaggle.

Các tác giả đề xuất kiến trúc Gated Feature Interaction Multilayer Perceptron (GFI-MLP), cho phép khai thác những tương tác giữa các đặc trưng trong dữ liệu bảng.

Mô hình được so sánh với nhiều phương pháp học máy và học sâu khác để đánh giá hiệu quả dự đoán.

**Kết quả nghiên cứu**

GFI-MLP đạt AUC = 0,8464 và F1-score = 0,8236 trên bộ dữ liệu được nghiên cứu.

Kết quả cho thấy mô hình mạng nơ-ron có thể khai thác hiệu quả các quan hệ trong dữ liệu logistics thương mại điện tử khi được xây dựng và huấn luyện phù hợp.

**Hạn chế**

Nghiên cứu sử dụng bộ dữ liệu và phương pháp xử lý khác với đồ án Olist.

Ngoài ra, GFI-MLP là kiến trúc có cơ chế tương tác đặc trưng chuyên biệt, phức tạp hơn MLP thông thường mà nhóm đang thực hiện.

Do đó, không thể dùng trực tiếp AUC hoặc F1-score của nghiên cứu để kết luận MLP chắc chắn tốt hơn Random Forest trên dữ liệu Olist.

**Khả năng áp dụng vào đồ án**

Nghiên cứu cung cấp cơ sở tham khảo cho việc sử dụng MLP trong bài toán dự đoán nguy cơ giao hàng trễ.

Trong đồ án, Tấn Lên phụ trách huấn luyện MLP, còn Ngọc Lan phụ trách Random Forest. Hai mô hình sử dụng chung dữ liệu, đặc trưng và giao thức chia tập để bảo đảm khả năng so sánh.

Việc mô hình nào phù hợp hơn cần dựa trên kết quả Validation và Test thực tế của nhóm, không dựa trên kết quả từ một nghiên cứu sử dụng bộ dữ liệu khác.

### 2.5.4. Tổng hợp và định hướng áp dụng vào đề tài

**Bảng 2.6. Tổng hợp và so sánh các công trình nghiên cứu liên quan**

| Nghiên cứu | Phương pháp và kết quả chính | Hạn chế | Khả năng áp dụng |
|---|---|---|---|
| Salari và cộng sự (2022) | Dự báo phân phối thời gian giao hàng; chính sách đề xuất cải thiện doanh số khoảng 6,1% trong mô phỏng | Dự báo thời gian giao, không trực tiếp phân loại giao trễ | Tham khảo vai trò của dự báo sớm trong hỗ trợ vận hành |
| Saini và cộng sự (2026) | Random Forest, SHAP và kiểm soát Data Leakage; R² = 0,2719 khi không dùng thông tin hậu nghiệm, tăng lên 0,7589 khi có leakage | Bài toán hồi quy về độ trễ xuất hàng, khác Olist | Kiểm soát đặc trưng theo thời điểm dự báo và tránh rò rỉ dữ liệu |
| Zhang và cộng sự (2026) | GFI-MLP; AUC = 0,8464 và F1-score = 0,8236 | Khác dữ liệu Olist và khác MLP thông thường | Tham khảo việc sử dụng và so sánh mô hình mạng nơ-ron trên dữ liệu bảng |

*Nguồn: Tác giả tổng hợp từ Salari và cộng sự (2022), Saini và cộng sự (2026), Zhang và cộng sự (2026).*

Qua ba nghiên cứu trên, nhóm nhận thấy rằng dự đoán giao hàng trễ không chỉ phụ thuộc vào thuật toán mà còn liên quan đến chất lượng dữ liệu, thời điểm có thông tin và mục tiêu đánh giá.

Nghiên cứu của Salari và cộng sự cho thấy giá trị của dự báo sớm đối với hoạt động logistics. Saini và cộng sự nhấn mạnh nguy cơ rò rỉ dữ liệu khi sử dụng thông tin hậu nghiệm. Trong khi đó, Zhang và cộng sự cho thấy tiềm năng của mô hình mạng nơ-ron trong việc khai thác dữ liệu dạng bảng.

Từ các kết quả nghiên cứu này, nhóm lựa chọn xây dựng bài toán phân loại nguy cơ giao hàng trễ tại thời điểm `order_approved_at` trên bộ dữ liệu Olist.

Ba mô hình được sử dụng trong đồ án gồm Dummy Classifier, Random Forest và MLP. Các mô hình được huấn luyện, tích hợp và đánh giá theo cùng giao thức nhằm bảo đảm khả năng so sánh.

Do dữ liệu có sự mất cân bằng giữa đơn giao trễ và không giao trễ, nhóm sử dụng các chỉ số Average Precision, Precision, Recall, F1-score, False Positive và Top-K để đánh giá.

Bên cạnh đó, nhóm chú trọng kiểm soát rò rỉ thông tin và tách biệt vai trò của Train, Validation và Test.

Những nghiên cứu liên quan cung cấp cơ sở lý thuyết và phương pháp tham khảo, nhưng kết quả cuối cùng của đồ án phải dựa trên thực nghiệm thực tế với bộ dữ liệu Olist.

**Tài liệu tham khảo cho mục 2.5**

[1] Salari, N., Liu, S., & Shen, Z.-J. M. (2022). Real-Time Delivery Time Forecasting and Promising in Online Retailing: When Will Your Package Arrive? *Manufacturing & Service Operations Management, 24*(3), 1421–1436. https://doi.org/10.1287/msom.2022.1081

[2] Saini, D., Singh, H., & Agarwal, B. (2026). Interpretable and leakage-aware prediction of shipment delays in global supply chains: A Random Forest–SHAP workflow with multi-model benchmarking on the DataCo dataset. *Modern Supply Chain Research and Applications, 8*(3), 419–433. https://doi.org/10.1108/MSCRA-04-2026-0035

[3] Zhang, Y., Wang, Y., & Wang, Y. (2026). A Deep Tabular Learning Framework for E-Commerce Delivery Delay Prediction and Cost-Sensitive Operational Risk Mitigation. *Algorithms, 19*(7), 597. https://doi.org/10.3390/a19070597

## PHỤ LỤC A – Ghi chú nghiệm thu nội bộ

*Nội dung dưới đây được giữ từ khung phân công của nhóm trưởng để theo dõi tiến độ; không thuộc các tiểu mục lý thuyết 2.1–2.5.*

> Đồng bộ số liệu, tên biến và trích dẫn với phần triển khai / notebook liên quan trước khi tạo PR.

**Cập nhật phân công 2.3–2.4:** Ngọc Lan trực tiếp huấn luyện Random Forest trên Train chung và đánh giá Precision/Recall/F1/AP/FP/Top-K trên Validation. Bổ sung vào các mục 2.3–2.4 thông số RF, bảng Validation, `split_id`, giải thích kết quả và link notebook (chỉ sau khi chạy). Không báo kết quả Test trong Chương 2; bàn giao artifact cho Trúc Chi.
