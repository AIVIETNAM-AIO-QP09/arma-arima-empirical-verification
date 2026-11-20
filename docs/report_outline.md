# Bố cục báo cáo (đã thống nhất)

Tiểu luận nhóm; không nhắc "bài giảng", không đánh số 11.x/12.x trong báo cáo (số hiệu notebook chỉ dùng nội bộ, xem bảng đối ứng cuối file).

## Quy ước các cấp
| Cấp | Ký hiệu | Ví dụ | Định dạng |
|---|---|---|---|
| 1 | Chương N | CHƯƠNG 4. KIỂM CHỨNG CHUỖI DỪNG VÀ MÔ HÌNH ARMA | in hoa, đậm, sang trang mới |
| 2 | N.n | 4.2 Mô hình ARMA | đậm |
| 3 | N.n.n (chỉ ở Chương 2) | 2.1.2 Mô hình ARMA | đậm nghiêng |
| 4 | a), b), c)… | a) Mô hình AR(1) | đậm, thụt lề, một dòng riêng |
| 5 | (i), (ii), (iii) | (i) Hồ Huron | nghiêng, đầu đoạn (diễn giải theo từng bộ dữ liệu) |
| Thành phần | không đánh số | *Cách triển khai.* | đậm nghiêng, đầu đoạn |

Tối đa ba cấp số. Tiêu đề: cụm danh từ, chỉ viết hoa chữ đầu (trừ cấp 1), không dấu hai chấm. Độ dài tối đa: cấp 2 là 5 từ, cấp 3 là 6 từ, cấp 4 là 7 từ.

## Nguyên tắc "một nơi duy nhất"
Công thức, định nghĩa, định lý chỉ ở Chương 2. Mô tả bộ dữ liệu chỉ ở Bảng 3.1. Phương pháp chung chỉ ở §3.3. Danh mục nội dung chỉ ở Bảng 1.1 (Bảng 7.1 chỉ ghi số hiệu và xếp loại). Nhận xét từng mục là kết luận cục bộ; Chương 7 là đối chiếu xuyên mục; Chương 8 trả lời các câu hỏi kiểm chứng ở §1.2.
Địa chỉ song song: mục `2.1`, `2.2`, `2.3` được kiểm chứng lần lượt ở Chương 4, 5, 6; mục con `2.m.n` ↔ mục `(m+3).n`, cấp 4 trùng nhau (kết quả `2.1.2(c)` được kiểm chứng ở `4.2(c)`). Chương 2 gồm đúng 3 mục × 3 mục con; Monte Carlo chuyển về §3.3.

Mỗi mục cấp 4 có sáu thành phần cố định: *Nội dung lý thuyết cần kiểm chứng* (một câu, dẫn tới địa chỉ ở Chương 2) · *Cách triển khai* (có dòng **Bộ áp dụng** và lý do với bộ không áp dụng) · *Mã lệnh Python* · *Kết quả tính toán* · *Phân tích và diễn giải* · *Nhận xét* (kèm xếp loại phù hợp / phù hợp một phần / không phù hợp).

## Cấu trúc
- **Mở đầu:** Trang bìa (thông tin nhóm) · Mục lục
- **Chương 1. Giới thiệu:** 1.1 Bối cảnh · 1.2 Mục tiêu (ba câu hỏi kiểm chứng) · 1.3 Phạm vi (Bảng 1.1) · 1.4 Bố cục
- **Chương 2. Cơ sở lý thuyết:** 2.1 Chuỗi dừng và mô hình ARMA (2.1.1 Chuỗi dừng; 2.1.2 Mô hình ARMA; 2.1.3 Xây dựng mô hình ARMA) · 2.2 Chuỗi không dừng và mô hình ARIMA (2.2.1 Chuỗi không dừng; 2.2.2 Mô hình ARIMA; 2.2.3 Xây dựng mô hình ARIMA) · 2.3 Dự báo và đánh giá dự báo (2.3.1 Hàm dự báo; 2.3.2 Khoảng dự báo; 2.3.3 Đánh giá dự báo). Địa chỉ 2.m.n(z) được kiểm chứng tại (m+3).n(z).
- **Chương 3. Dữ liệu và phương pháp:** 3.1 Mô tả dữ liệu (Bảng 3.1) · 3.2 Xử lý dữ liệu (tiền xử lý; khám phá) · 3.3 Phương pháp kiểm chứng (đối chiếu với phần mềm; mô phỏng; đánh giá dự báo; tái lập) · 3.4 Tiêu chí đánh giá (thang xếp loại)
- **Chương 4. Kiểm chứng chuỗi dừng và mô hình ARMA:** 4.1 Chuỗi dừng (4) · 4.2 Mô hình ARMA (5) · 4.3 Xây dựng mô hình ARMA (5)
- **Chương 5. Kiểm chứng chuỗi không dừng và mô hình ARIMA:** 5.1 Chuỗi không dừng (2) · 5.2 Mô hình ARIMA (2) · 5.3 Xây dựng mô hình ARIMA (2)
- **Chương 6. Kiểm chứng dự báo và đánh giá dự báo:** 6.1 Hàm dự báo (2) · 6.2 Khoảng dự báo (2) · 6.3 Đánh giá dự báo (4)
- **Chương 7. Thảo luận:** 7.1 Mức độ phù hợp (Bảng 7.1) · 7.2 Khác biệt giữa các bộ dữ liệu · 7.3 Ảnh hưởng của đặc điểm dữ liệu · 7.4 Mức độ thỏa mãn giả thiết · 7.5 Hạn chế
- **Chương 8. Kết luận**
- **Tài liệu tham khảo** (nhóm Tài liệu; nhóm Nguồn dữ liệu)
- **Phụ lục:** A. Phân công nhiệm vụ · B. Mã nguồn và tái lập

## Quyết định đã chốt
- Phần mở rộng (đồng tích hợp log DAX ~ log SMI, Engle–Granger) **nhét thành đoạn ngắn cuối** `2.2.1(b)` (lý thuyết) và `5.1(b)` (kiểm chứng), gắn nhãn "mở rộng"; không tạo mục riêng; danh mục vẫn 28 nội dung. Nguồn: notebook Bài 12, mục ⋆, bảng `tab_b12_ext_cointegration`.
- Ký hiệu cấp 4 là `a)`; có dùng cấp 5 `(i), (ii), (iii)`; mục 7.4 đổi tên thành **"Mức độ thỏa mãn giả thiết"** (song song với 7.1 "Mức độ phù hợp"; phương án dự phòng: "Điều kiện áp dụng").
- Khung LaTeX theo template người dùng cung cấp (bìa có logo và nền, đầu/chân trang, mục lục): `reports/report/main.tex` + `chapters/`.
- Còn chờ quyết: dòng "cặp bài giảng" trên bìa (đang để TODO); danh sách thành viên, học kỳ, giảng viên (TODO).

## Bảng đối ứng số hiệu (nội bộ)
| Địa chỉ báo cáo | Mã notebook | Nội dung | Bộ dữ liệu chính |
|---|---|---|---|
| 4.1(a) | 11.1 | Tính dừng và nhiễu trắng | HU, LY, DR |
| 4.1(b) | 11.2 | Tính chất của tự hiệp phương sai | HU, LY, DR |
| 4.1(c) | 11.3 | Trung bình mẫu của chuỗi phụ thuộc | HU (+ mô phỏng) |
| 4.1(d) | 11.5 | Quá trình tuyến tính | HU, LY |
| 4.2(a) | 11.6 | Mô hình AR(1) | HU |
| 4.2(b) | 11.7 | Mô hình AR(p) và hệ Yule–Walker | LY, HU |
| 4.2(c) | 11.8 | Mô hình AR(2) | LY |
| 4.2(d) | 11.9 | Mô hình MA(q) | DR, HU |
| 4.2(e) | 11.10 | Mô hình ARMA(p, q) | HU, LY |
| 4.3(a) | 11.4 | Tự tương quan và kiểm định Ljung–Box | HU, LY, DR |
| 4.3(b) | 11.11 | Tự tương quan riêng phần | HU, LY, DR |
| 4.3(c) | 11.12 | Ước lượng tham số | LY, HU |
| 4.3(d) | 11.13 | Lựa chọn bậc | LY, HU |
| 4.3(e) | 11.14 | Chẩn đoán phần dư | HU, LY, DR |
| 5.1(a) | 12.1 | Xu thế tất định và ngẫu nhiên | NI, AP, DP |
| 5.1(b) | 12.2 (+ ⋆) | Bước ngẫu nhiên (+ mở rộng đồng tích hợp) | DP |
| 5.2(a) | 12.5 | Mô hình ARIMA và độ trôi | NI, DP |
| 5.2(b) | 12.10 | Mô hình ARIMA mùa vụ | AP |
| 5.3(a) | 12.3 | Sai phân và sai phân quá mức | NI, DP |
| 5.3(b) | 12.4 | Kiểm định nghiệm đơn vị | NI, AP, DP |
| 6.1(a) | 12.6 | Ảnh hưởng vĩnh viễn của cú sốc | NI, DP |
| 6.1(b) | 12.7 | Làm trơn mũ và mô hình mức cục bộ | NI |
| 6.2(a) | 12.8 | Dự báo tối ưu và khoảng dự báo | NI, AP, DP |
| 6.2(b) | 12.9 | Dự báo trên thang logarit | AP, DP |
| 6.3(a) | 12.11 | Mốc chuẩn và thước đo sai số | NI, AP, DP |
| 6.3(b) | 12.12 | Gốc cuốn chiếu | NI, AP, DP |
| 6.3(c) | 12.13 | Hàm mất mát và kiểm định Diebold–Mariano | AP, NI |
| 6.3(d) | 12.14 | Quy trình báo cáo dự báo | NI, AP, DP |
