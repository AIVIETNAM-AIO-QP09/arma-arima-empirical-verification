# Bố cục báo cáo (đã thống nhất)

Tiểu luận nhóm; không nhắc "bài giảng", không đánh số 11.x/12.x trong báo cáo (số hiệu notebook chỉ dùng nội bộ, xem bảng đối ứng cuối file).

## Quy ước các cấp
| Cấp | Ký hiệu | Ví dụ | Định dạng |
|---|---|---|---|
| 1 | Chương N | CHƯƠNG 4. KIỂM CHỨNG CHUỖI DỪNG VÀ MÔ HÌNH ARMA | in hoa, đậm, sang trang mới |
| 2 | N.n | 4.2 Mô hình ARMA | đậm |
| 3 | N.n.n | 4.2.1 Quá trình tuyến tính và mô hình AR | đậm nghiêng |
| 4 | a), b), c)… | a) Mô hình AR(1) | đậm, thụt lề, một dòng riêng |
| 5 | (i), (ii), (iii) | (i) Hồ Huron | nghiêng, đầu đoạn (diễn giải theo từng bộ dữ liệu) |
| Thành phần | không đánh số | *Cách triển khai.* | đậm nghiêng, đầu đoạn |

Tối đa ba cấp số. Tiêu đề: cụm danh từ, chỉ viết hoa chữ đầu (trừ cấp 1), không dấu hai chấm. Độ dài tối đa: cấp 2 là 5 từ, cấp 3 là 6 từ, cấp 4 là 7 từ.

## Nguyên tắc "một nơi duy nhất"
Công thức, định nghĩa, định lý chỉ ở Chương 2. Mô tả bộ dữ liệu chỉ ở Bảng 3.1. Phương pháp chung chỉ ở §3.3. Danh mục nội dung chỉ ở Bảng 1.1 (Bảng 6.1 chỉ ghi số hiệu và xếp loại). Nhận xét từng mục là kết luận cục bộ; Chương 6 là đối chiếu xuyên mục; Chương 7 trả lời các câu hỏi kiểm chứng ở §1.2.
Địa chỉ song song: `2.1`–`2.2` ↔ `4.1`–`4.2`; `2.3`–`2.5` ↔ `5.1`–`5.3`; cấp 3 và cấp 4 trùng nhau (kết quả `2.2.1(c)` được kiểm chứng ở `4.2.1(c)`).

Mỗi mục cấp 4 có sáu thành phần cố định: *Nội dung lý thuyết cần kiểm chứng* (một câu, dẫn tới địa chỉ ở Chương 2) · *Cách triển khai* (có dòng **Bộ áp dụng** và lý do với bộ không áp dụng) · *Mã lệnh Python* · *Kết quả tính toán* · *Phân tích và diễn giải* · *Nhận xét* (kèm xếp loại phù hợp / phù hợp một phần / không phù hợp).

## Cấu trúc
- **Mở đầu:** Trang bìa (thông tin nhóm) · Mục lục
- **Chương 1. Giới thiệu:** 1.1 Bối cảnh · 1.2 Mục tiêu (ba câu hỏi kiểm chứng) · 1.3 Phạm vi (Bảng 1.1) · 1.4 Bố cục
- **Chương 2. Cơ sở lý thuyết:** 2.1 Chuỗi dừng và tự tương quan (2.1.1 Tính dừng và cấu trúc phụ thuộc; 2.1.2 Công cụ chẩn đoán) · 2.2 Mô hình ARMA (2.2.1 Quá trình tuyến tính và mô hình AR; 2.2.2 Mô hình MA và ARMA; 2.2.3 Ước lượng và chẩn đoán mô hình) · 2.3 Chuỗi không dừng và ARIMA (2.3.1 Tính không dừng và nghiệm đơn vị; 2.3.2 Mô hình ARIMA) · 2.4 Dự báo (2.4.1 Hàm dự báo; 2.4.2 Khoảng dự báo) · 2.5 Đánh giá dự báo (2.5.1 Đánh giá độ chính xác; 2.5.2 So sánh và báo cáo) · 2.6 Mô phỏng Monte Carlo
- **Chương 3. Dữ liệu và phương pháp:** 3.1 Mô tả dữ liệu (Bảng 3.1) · 3.2 Xử lý dữ liệu (tiền xử lý; khám phá) · 3.3 Phương pháp kiểm chứng (đối chiếu với phần mềm; mô phỏng; đánh giá dự báo; tái lập) · 3.4 Tiêu chí đánh giá (thang xếp loại)
- **Chương 4. Kiểm chứng chuỗi dừng và mô hình ARMA:** 4.1 Chuỗi dừng và tự tương quan · 4.2 Mô hình ARMA
- **Chương 5. Kiểm chứng chuỗi không dừng và dự báo:** 5.1 Chuỗi không dừng và ARIMA · 5.2 Dự báo · 5.3 Đánh giá dự báo
- **Chương 6. Thảo luận:** 6.1 Mức độ phù hợp (Bảng 6.1) · 6.2 Khác biệt giữa các bộ dữ liệu · 6.3 Ảnh hưởng của đặc điểm dữ liệu · 6.4 Mức độ thỏa mãn giả thiết · 6.5 Hạn chế
- **Chương 7. Kết luận**
- **Tài liệu tham khảo** (nhóm Tài liệu; nhóm Nguồn dữ liệu)
- **Phụ lục:** A. Phân công nhiệm vụ · B. Mã nguồn và tái lập

## Quyết định đã chốt
- Phần mở rộng (đồng tích hợp log DAX ~ log SMI, Engle–Granger) **nhét thành đoạn ngắn cuối** `2.3.1(b)` (lý thuyết) và `5.1.1(b)` (kiểm chứng), gắn nhãn "mở rộng"; không tạo mục riêng; danh mục vẫn 28 nội dung. Nguồn: notebook Bài 12, mục ⋆, bảng `tab_b12_ext_cointegration`.
- Ký hiệu cấp 4 là `a)`; có dùng cấp 5 `(i), (ii), (iii)`; mục 6.4 đổi tên thành **"Mức độ thỏa mãn giả thiết"** (song song với 6.1 "Mức độ phù hợp"; phương án dự phòng: "Điều kiện áp dụng").
- Khung LaTeX theo template người dùng cung cấp (bìa có logo và nền, đầu/chân trang, mục lục): `reports/report/main.tex` + `chapters/`.
- Còn chờ quyết: dòng "cặp bài giảng" trên bìa (đang để TODO); danh sách thành viên, học kỳ, giảng viên (TODO).

## Bảng đối ứng số hiệu (nội bộ)
| Địa chỉ báo cáo | Mã notebook | Nội dung | Bộ dữ liệu chính |
|---|---|---|---|
| 4.1.1(a) | 11.1 | Tính dừng và nhiễu trắng | HU, LY, DR |
| 4.1.1(b) | 11.2 | Tính chất của tự hiệp phương sai | HU, LY, DR |
| 4.1.1(c) | 11.3 | Trung bình mẫu của chuỗi phụ thuộc | HU (+ mô phỏng) |
| 4.1.2(a) | 11.4 | Tự tương quan và kiểm định Ljung–Box | HU, LY, DR |
| 4.1.2(b) | 11.11 | Tự tương quan riêng phần | HU, LY, DR |
| 4.2.1(a) | 11.5 | Quá trình tuyến tính | HU, LY |
| 4.2.1(b) | 11.6 | Mô hình AR(1) | HU |
| 4.2.1(c) | 11.7 | Mô hình AR(p) và hệ Yule–Walker | LY, HU |
| 4.2.1(d) | 11.8 | Mô hình AR(2) | LY |
| 4.2.2(a) | 11.9 | Mô hình MA(q) | DR, HU |
| 4.2.2(b) | 11.10 | Mô hình ARMA(p, q) | HU, LY |
| 4.2.3(a) | 11.12 | Ước lượng tham số | LY, HU |
| 4.2.3(b) | 11.13 | Lựa chọn bậc | LY, HU |
| 4.2.3(c) | 11.14 | Chẩn đoán phần dư | HU, LY, DR |
| 5.1.1(a) | 12.1 | Xu thế tất định và ngẫu nhiên | NI, AP, DP |
| 5.1.1(b) | 12.2 (+ ⋆) | Bước ngẫu nhiên (+ mở rộng đồng tích hợp) | DP |
| 5.1.1(c) | 12.3 | Sai phân và sai phân quá mức | NI, DP |
| 5.1.1(d) | 12.4 | Kiểm định nghiệm đơn vị | NI, AP, DP |
| 5.1.2(a) | 12.5 | Mô hình ARIMA và độ trôi | NI, DP |
| 5.1.2(b) | 12.10 | Mô hình ARIMA mùa vụ | AP |
| 5.2.1(a) | 12.6 | Ảnh hưởng vĩnh viễn của cú sốc | NI, DP |
| 5.2.1(b) | 12.7 | Làm trơn mũ và mô hình mức cục bộ | NI |
| 5.2.2(a) | 12.8 | Dự báo tối ưu và khoảng dự báo | NI, AP, DP |
| 5.2.2(b) | 12.9 | Dự báo trên thang logarit | AP, DP |
| 5.3.1(a) | 12.11 | Mốc chuẩn và thước đo sai số | NI, AP, DP |
| 5.3.1(b) | 12.12 | Gốc cuốn chiếu | NI, AP, DP |
| 5.3.2(a) | 12.13 | Hàm mất mát và kiểm định Diebold–Mariano | AP, NI |
| 5.3.2(b) | 12.14 | Quy trình báo cáo dự báo | NI, AP, DP |
