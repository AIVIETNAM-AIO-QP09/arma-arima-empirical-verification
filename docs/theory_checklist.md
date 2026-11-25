# Danh sách nội dung lý thuyết cần kiểm chứng (khung Mục 4.2)

Ký hiệu: **[D]** = tính trên dữ liệu thật; **[M]** = mô phỏng có điều khiển (dùng mô hình đã khớp trên dữ liệu làm "sự thật", sinh lại nhiều chuỗi cùng độ dài với seed cố định, so tần suất mô phỏng với lý thuyết kèm MCSE). Mỗi bài giảng được kiểm chứng trên **cả 3 bộ** của nó; mỗi trường hợp đều có kết quả hoặc chẩn đoán điều kiện áp dụng và diễn giải. Bản nộp gộp các mục vào [một notebook](../AS3179_Nhom7.ipynb).

Cột `Trạng thái`: `xong` / `đang làm`. Cột `Ô notebook`: section tương ứng (tiêu đề `## <ID>`).

## Bài 11 (bộ HU, LY, DR) — `notebooks/bai11_arma.ipynb`

| ID | Nội dung (nguồn trong bài giảng) | Cách kiểm chứng | Kiểu | Bộ | Trạng thái | Ô notebook |
|---|---|---|---|---|---|---|
| 11.1 | Chuỗi thời gian, trung bình, tự hiệp phương sai; dừng nghiêm ngặt / dừng yếu; nhiễu trắng vs iid (ĐN 1–2) | Đồ thị chuỗi; trung bình và phương sai theo cửa sổ trượt; DR: không tương quan nhưng không iid | D | cả 3 | xong | §11.1 |
| 11.2 | Tính chất của γ: γ(0) ≥ 0, \|ρ(h)\| ≤ 1, γ(−h) = γ(h), Γₙ nửa xác định dương (MĐ 1) | γ̂ với mẫu số n (ĐN 3); trị riêng của Γ̂ₙ ≥ 0; so với mẫu số n − h | D | cả 3 | xong | §11.2 |
| 11.3 | Trung bình mẫu khi có phụ thuộc: Var Ȳ = (1/n)Σ(1 − \|h\|/n)γ(h) ≈ γ(0)τ/n, n_eff = n/τ; AR(1): τ = (1+φ)/(1−φ) (ĐL 1) | HU: so se iid với se có tính phụ thuộc; mô phỏng AR(1) φ = 0.6, n = 100, B = 2000: độ phủ KTC ngây thơ so với đã hiệu chỉnh | D + M | cả 3 | xong | §11.3 |
| 11.4 | ACF mẫu; dải iid ±1.96/√n; Bartlett; Ljung–Box Q_LB(H) = n(n+2)Σρ̂(h)²/(n−h) ≈ χ²_H (ĐL 2) | Tự tính và so với `acf`, `acorr_ljungbox`; mô phỏng nhiễu iid: tỷ lệ vượt dải ≈ 5%, Q_LB ~ χ²_H; DR: Q_LB của r và r² | D + M | cả 3 | xong | §11.4 |
| 11.5 | Toán tử lùi, quá trình tuyến tính, nhân quả; γ(h) = σ²Σψⱼψⱼ₊ₕ (ĐN 4, MĐ 2) | Trọng số ψ (`arma2ma`) và ACF lý thuyết (`arma_acf`) của mô hình đã khớp, chồng lên ACF mẫu | D | cả 3 | xong | §11.5 |
| 11.6 | AR(1): nghiệm nhân quả khi \|φ\| < 1, ρ(h) = φ^\|h\|, γ(0) = σ²/(1−φ²) (ĐL 3) | Khớp AR(1) (HU, xu thế trong exog); so ACF mẫu với φ̂^h | D (+M) | cả 3 | xong | §11.6 |
| 11.7 | AR(p): nhân quả ⇔ mọi nghiệm φ(z) có \|z\| > 1; Yule–Walker Γₚφ = γₚ (ĐL 4) | Giải YW bằng tay, so `yule_walker`; môđun nghiệm | D | cả 3 | xong | §11.7 |
| 11.8 | AR(2): tam giác nhân quả φ₁+φ₂ < 1, φ₂−φ₁ < 1, \|φ₂\| < 1; nghiệm phức → chu kỳ 2π/\|arg z\| (MĐ 3) | LY: YW AR(2), vị trí trong tam giác, chu kỳ ≈ 9.66 năm. Với DR, ta khớp thêm AR(2) và xét cả môđun nghiệm lẫn mức ý nghĩa của các hệ số. | D | cả 3 | xong | §11.8 |
| 11.9 | MA(q): ACF cắt cụt sau q; MA(1): ρ(1) = θ/(1+θ²), \|ρ(1)\| ≤ 0.5; khả nghịch; (θ, σ²) và (1/θ, θ²σ²) cùng ACF (ĐN 5, MĐ 4) | Khớp MA(1)/MA(2); mô phỏng MA(q) thấy ACF mẫu cắt cụt. Ta khớp MA(1) cho cả ba chuỗi và so ACF ở các độ trễ sau bậc mô hình với dải Bartlett. | D + M | cả 3 | xong | §11.9 |
| 11.10 | ARMA(p, q) nhân quả và khả nghịch, ψ(z) = θ(z)/φ(z), không nghiệm chung; thừa tham số (ĐL 5) | Khớp ARMA(1,1); kiểm tra nghiệm AR/MA; minh họa gần triệt tiêu nghiệm | D | cả 3 | xong | §11.10 |
| 11.11 | PACF α(h) = φ_hh; α(1) = ρ(1), α(2) = (ρ(2)−ρ(1)²)/(1−ρ(1)²); AR(p) cắt cụt sau p (ĐN 6, MĐ 5) | Tính tay (Durbin–Levinson), so `pacf`; dùng PACF đề xuất p | D | cả 3 | xong | §11.11 |
| 11.12 | Ước lượng Yule–Walker / OLS / ML; AR khớp bằng YW luôn nhân quả; phân phối tiệm cận (ĐL 6) | So φ̂ của YW, OLS (`AutoReg`), ML (`ARIMA`) kèm se; mô phỏng phân phối của φ̂ | D + M | cả 3 | xong | §11.12 |
| 11.13 | Chọn bậc bằng AIC/BIC; thẩm định cuốn chiếu | Lưới bậc; LY: AIC chọn p = 11, BIC chọn p = 2; HU: AR(1)/AR(2)/MA(2)/ARMA(1,1) với exog | D | cả 3 | xong | §11.13 |
| 11.14 | Chẩn đoán phần dư: ACF phần dư, Q_LB(H) với H − p − q bậc tự do, ACF của bình phương phần dư; checklist báo cáo ARMA | Đủ 5 bước checklist (vẽ → làm dừng → ACF/PACF → khớp ML → phần dư); DR: cụm biến động | D | cả 3 | xong | §11.14 |

## Bài 12 (bộ NI, AP, DP) — `notebooks/bai12_arima_du_bao.ipynb`

| ID | Nội dung (nguồn trong bài giảng) | Cách kiểm chứng | Kiểu | Bộ | Trạng thái | Ô notebook |
|---|---|---|---|---|---|---|
| 12.1 | Xu thế tất định vs ngẫu nhiên; I(d), nghiệm đơn vị (ĐN 1) | Đồ thị và ACF chuỗi gốc so với chuỗi sai phân | D | cả 3 | xong | §12.1 |
| 12.2 | Bước ngẫu nhiên: E Yₜ = Y₀ + δt, Var Yₜ = tσ², Cov(Yₛ, Yₜ) = min(s,t)σ², Corr = √(t/(t+h)) (ĐL 1) | Mô phỏng với δ̂, σ̂ của DP; so phương sai theo t. Ta kiểm tra gia số của cả ba chuỗi bằng Ljung--Box (10 độ trễ ở NI và DP, 12 ở AP). AP và DP dùng mẫu huấn luyện. | D + M | cả 3 | xong | §12.2 |
| 12.3 | Sai phân sửa được gì và làm hỏng gì; sai phân quá mức: ρ(1) → −½, θ̂ → −1, phương sai dài hạn bằng 0 (MĐ 1) | Sai phân thêm một lần cho NI và DP; khớp MA(1) cho chuỗi đã sai phân quá mức. Với AP ta so chuỗi log sau sai phân thường và mùa vụ với chính chuỗi đó sau khi sai phân thường thêm một lần. | D + M | cả 3 | xong | §12.3 |
| 12.4 | ADF (tới hạn 5% là −2.86 với hệ số chặn), KPSS (giả thuyết không ngược lại) (ĐL 2) | Cả 3 bộ, mức gốc và sai phân, kiểu `c`/`ct`; mô phỏng dưới H₀ thấy τ không theo phân phối t; NI: mâu thuẫn do đổi mức | D + M | cả 3 | xong | §12.4 |
| 12.5 | ARIMA(p, d, q): φ(B)∇^d Yₜ = c + θ(B)εₜ; trôi µ_W = c/φ(1) (ĐN 2) | NI: ARIMA(0,1,1); DP: bước ngẫu nhiên có trôi / ARIMA(1,1,0). Với AP, ta khớp ARIMA$(0,1,1)$ có trôi trên 120 tháng log hành khách và kiểm tra phần dư ở độ trễ 12. | D | cả 3 | xong | §12.5 |
| 12.6 | Ảnh hưởng vĩnh viễn của cú sốc: Ψₖ → θ(1)/φ(1); 1 cho RW, 1 + θ cho ARIMA(0,1,1) (ĐL 3) | Tính Ψₖ từ mô hình đã khớp. Để kiểm tra định lý một nghiệm đơn vị trên AP, ta dùng mô hình ARIMA không mùa vụ ở mục 5.2(a) làm đối chứng. | D | cả 3 | xong | §12.6 |
| 12.7 | ARIMA(0,1,1) ≡ làm trơn mũ đơn α = 1 + θ; mức cục bộ: σ_ε² = −θσ², σ_η² = (1+θ)²σ² | NI: đệ quy làm trơn tay và `SimpleExpSmoothing`, so dự báo ARIMA. Ta khớp SES trên mẫu huấn luyện của log AP và log DP, đối chiếu đệ quy với thư viện và kiểm tra phần dư. | D | cả 3 | xong | §12.7 |
| 12.8 | Dự báo h-bước tối ưu MSE, eₙ(h) = ΣΨⱼεₙ₊ₕ₋ⱼ, Var = σ²ΣΨⱼ²; RW: hσ²; ARIMA(0,1,1): σ²{1+(h−1)α²}; d = 0 hội tụ γ(0) (ĐL 4) | Độ rộng khoảng dự báo tay so `get_forecast`; mô phỏng độ phủ | D + M | cả 3 | xong | §12.8 |
| 12.9 | Dự báo trên thang log: khoảng chuyển đổi chính xác; e^m trung vị, e^{m+s²/2} trung bình (MĐ 2) | AP: cả trung vị và trung bình; DP: DAX sau 1, 20, 250 ngày. Ta khớp thêm ARIMA$(0,1,1)$ trên log lưu lượng của 80 năm đầu ở NI để kiểm tra phép đổi thang. | D | cả 3 | xong | §12.9 |
| 12.10 | Sai phân mùa vụ ∇ₛ; SARIMA; airline: ρ(1) = θ/(1+θ²), ρ(s) = Θ/(1+Θ²), ρ(s±1) = ρ(1)ρ(s) (ĐN 4, ĐL 5) | AP: log → ∇∇₁₂; ACF tại 1, 11, 12, 13 so với lý thuyết từ (θ̂, Θ̂). Với NI ta thử chu kỳ 12 năm; với DP ta thử chu kỳ 5 phiên trên mẫu huấn luyện. Ta so ACF ở một và hai chu kỳ và tỷ số phương sai sau khi sai phân mùa vụ thêm một lần. | D | cả 3 | xong | §12.10 |
| 12.11 | Mốc chuẩn (trung bình, naive, naive mùa vụ, trôi); MAE, RMSE, MAPE, MASE (ĐN 5) | Bảng độ chính xác trên tập kiểm định giữ lại | D | cả 3 | xong | §12.11 |
| 12.12 | Thẩm định trên gốc cuốn chiếu; bước chọn mô hình nằm trong thiết kế đánh giá | Cả 3 bộ; DP: dự báo 1 bước cho 360 ngày | D | cả 3 | xong | §12.12 |
| 12.13 | Hàm mất mát xác định phiếm hàm (RMSE ↔ trung bình, MAE ↔ trung vị); Diebold–Mariano (ĐL 6) | AP: DM airline vs naive mùa vụ trên gốc cuốn chiếu; thứ hạng theo RMSE và MAE. Ở DP, ta so dự báo có trôi với naive trên cùng 360 gốc một bước. Độ trôi cố định từ 1.500 phiên đầu; chênh lệch mất mát được tính theo thứ tự có trôi trừ naive. | D | cả 3 | xong | §12.13 |
| 12.14 | Checklist báo cáo dự báo ARIMA | Đủ 5 bước checklist cho cả 3 bộ | D | cả 3 | xong | §12.14 |

**Mở rộng tùy chọn ⋆** (chỉ khung, làm sau nếu còn thời gian): hồi quy giả tạo và đồng tích hợp log DAX ~ log SMI (Engle–Granger, Bài 12).

## Nội dung bổ sung gắn vào mục sẵn có (giữ nguyên 28 ID, không thêm ID mới)

Các mục dưới đây có trong bài giảng nhưng chỉ gián tiếp có trong danh sách ở trên; làm trong section được ghi ở cột cuối. Riêng hồi quy giả mạo (Bài 11 Ví dụ 1.2) làm trong 12.2 dưới dạng mô phỏng.

| Đề xuất | Nguồn | Gợi ý gắn vào |
|---|---|---|
| Hồi quy giả mạo (hai bước ngẫu nhiên độc lập, OLS, kiểm định 5%, 2000 lần) | Bài 11 Ví dụ 1.2; Bài 12 trang ⋆ cointegration | 12.1/12.2 (mô phỏng) |
| Dự báo AR(1): µ + φʰ(Yₙ − µ), MSE σ²(1−φ²ʰ)/(1−φ²) → γ(0) | Bài 11 ĐL 3(d) | 11.6 |
| So sánh SE của hệ số dốc xu thế: OLS (−0.0242, SE 0.0040) vs sai số AR(2) (SE 0.0081) | Bài 11 Ví dụ mẫu Huron + checklist ("SE có tính phụ thuộc") | 11.3 hoặc 11.14 |
| Thẩm định cuốn chiếu dự báo 1 bước lynx 1915–1934 (AIC vs BIC) | Bài 11 Ví dụ 5.2 | 11.13 (đã nhắc "thẩm định cuốn chiếu") |
| Công thức Bartlett cho SE của ρ̂(h) với MA(q) | Bài 11 ĐL 2(c) | 11.4 (đã nhắc "Bartlett") |
| Dải PACF ±1.96/√n | Bài 11 MĐ 5(d) | 11.11 |
| Chi phí của sai phân thừa / thiếu: Var(Yₙ₊ₕ − Ȳₙ) = σ²{(n−1)(2n−1)/(6n) + h} (33.8σ² với n = 100) | Bài 12 MĐ 1(c),(d) | 12.3 |
| Hàm dự báo dài hạn theo d và độ trôi; SARIMA hàm dự báo = a + bh + mₕ | Bài 12 ĐL 3(d), ĐL 5(c) | 12.5 / 12.10 |
| Độ phủ khoảng dự báo ARIMA(0,1,1), θ = −0.5, n = 100: 0.952, 0.936, 0.939 | Bài 12 Ví dụ 3.2 | 12.8 (đã có [M] "mô phỏng độ phủ") |
| So sánh 3 cách mô hình hóa mùa vụ (airline / 11 biến giả / Fourier) | Bài 12 Ví dụ 4.2 | 12.10 |
| Tỷ lệ bác bỏ ADF theo φ và n; iid + dịch mức | Bài 12 Ví dụ 1.2 | 12.4 (đã có [M]) |
| Thước đo: MAPE bất đối xứng; MASE bất biến thang | Bài 12 ĐL 6(b),(c) | 12.11 |
