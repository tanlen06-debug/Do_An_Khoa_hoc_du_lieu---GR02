# Dữ liệu Olist – đọc trước khi tải

Nguồn: [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) trên Kaggle.

Tải bộ dữ liệu từ Kaggle, giải nén và đặt 9 CSV sau trực tiếp trong `data/raw/` của repository.

```text
olist_customers_dataset.csv
olist_geolocation_dataset.csv
olist_order_items_dataset.csv
olist_order_payments_dataset.csv
olist_order_reviews_dataset.csv
olist_orders_dataset.csv
olist_products_dataset.csv
olist_sellers_dataset.csv
product_category_name_translation.csv
```

Nhánh `main` đã có 9 tệp được theo dõi bằng Git LFS. Nếu máy đã cài Git LFS, có thể dùng `git lfs pull` để lấy nội dung thay cho tải từ Kaggle. Tệp bắt đầu bằng `version https://git-lfs.github.com/spec/v1` chỉ là con trỏ. Khi gặp con trỏ, hãy lấy tệp CSV thật bằng một trong hai cách trên. Giữ nguyên tên và nội dung của CSV.

Sau khi có đủ dữ liệu, cài phụ thuộc bằng `python -m pip install -r requirements.txt` và chạy từ đầu [notebook Chương 3](../notebooks/03_LAM_LINH_chuong_3.ipynb). Notebook lưu dữ liệu cấp đơn ở `data/processed/`. Đối chiếu tên, dung lượng và SHA256 của 9 tệp gốc với [source_manifest.csv](../reports/tables/source_manifest.csv).

Khi bàn giao cho Chương 4, dùng `orders_model_ready.csv`, `data_manifest.json` và `feature_whitelist.json` để kiểm tra dữ liệu. `orders_baseline_input.csv` chứa khóa, nhãn và 5 đặc trưng. `orders_split_metadata.csv` chứa các mốc thời gian phục vụ chia tập. Notebook 04 hiện đọc `orders_model_ready.csv` và chỉ chọn 5 cột trong danh sách đặc trưng. Chia sẻ gói dữ liệu đã xử lý qua kênh nội bộ của nhóm.
