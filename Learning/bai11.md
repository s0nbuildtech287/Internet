# Bài 11: TCP và UDP - Port & Handshake

## 1. Port (Cổng) là gì?

Nếu IP là địa chỉ của một ngôi nhà thì Port là số phòng trong ngôi nhà đó.

IP giúp dữ liệu tới đúng máy.

Port giúp dữ liệu tới đúng ứng dụng.

Ví dụ:


IP: 203.0.113.5
Port: 443


→ Máy có IP 203.0.113.5

→ Ứng dụng HTTPS (Web bảo mật)

### Phạm vi Port

- 0 - 1023: Well-known Ports (dịch vụ chuẩn)
- 1024 - 49151: Registered Ports
- 49152 - 65535: Dynamic/Private Ports

Một kết nối được xác định bởi:


IP nguồn
Port nguồn
IP đích
Port đích


---

## 2. Các Port phổ biến

| Port | Dịch vụ | Giao thức |
|------|----------|-----------|
| 80 | HTTP | TCP |
| 443 | HTTPS | TCP |
| 53 | DNS | UDP (chủ yếu) |
| 22 | SSH | TCP |
| 25 | SMTP (Email) | TCP |
| 67/68 | DHCP | UDP |

---

## 3. TCP là gì?

TCP (Transmission Control Protocol) là giao thức truyền dữ liệu **đảm bảo**.

Đặc điểm:

- Có kết nối (Connection-oriented)
- Đảm bảo dữ liệu tới nơi
- Đảm bảo đúng thứ tự
- Nếu mất gói sẽ gửi lại
- Kiểm soát tốc độ truyền

Thích hợp cho:

- Web
- HTTPS
- Tải file
- Email
- SSH

---

## 4. TCP 3-Way Handshake

Trước khi gửi dữ liệu TCP phải tạo kết nối.


CLIENT SERVER

│
├──── SYN ───────────────►
│ "Tôi muốn kết nối"

│
◄──── SYN + ACK ──────────
"OK"

│
├──── ACK ───────────────►
"Bắt đầu truyền"

========= Truyền dữ liệu =========


Ba bước:

1. SYN
   - Client xin kết nối.

2. SYN-ACK
   - Server đồng ý.

3. ACK
   - Client xác nhận.

Sau đó mới truyền dữ liệu.

Kết thúc kết nối thường dùng gói FIN.

---

## 5. UDP là gì?

UDP (User Datagram Protocol) là giao thức truyền dữ liệu **không đảm bảo**.

Đặc điểm:

- Không cần tạo kết nối
- Không Handshake
- Không gửi lại khi mất gói
- Không đảm bảo đúng thứ tự
- Rất nhanh
- Độ trễ thấp

Thích hợp cho:

- Game Online
- Video Call
- Livestream
- DNS

---

## 6. So sánh TCP và UDP

| Tiêu chí | TCP | UDP |
|-----------|-----|-----|
| Kết nối | Có | Không |
| Handshake | Có | Không |
| Đảm bảo dữ liệu | Có | Không |
| Đúng thứ tự | Có | Không |
| Gửi lại khi mất | Có | Không |
| Tốc độ | Chậm hơn | Nhanh hơn |
| Overhead | Cao | Thấp |

TCP:

- Chắc chắn dữ liệu tới nơi.
- Phù hợp tải file, web, email.

UDP:

- Ưu tiên tốc độ.
- Chấp nhận mất vài gói.
- Phù hợp game, video call.

---

## 7. Tại sao Video Call dùng UDP?

Nếu đang gọi video:

Mất 1 khung hình.

TCP sẽ:

- Dừng lại.
- Xin gửi lại khung hình.
- Chờ nhận.
- Video bị giật.

UDP sẽ:

- Bỏ luôn khung hình bị mất.
- Tiếp tục gửi khung hình mới.

=> Hình ảnh mượt hơn.

Trong gọi video:

Đúng thời điểm quan trọng hơn đúng tuyệt đối.

---

# Mẹo nhớ

- IP = Đúng máy.
- Port = Đúng ứng dụng.
- TCP = Tin cậy, có Handshake.
- UDP = Nhanh, không Handshake.
- TCP dùng cho Web, File, Email.
- UDP dùng cho Game, Video Call, Livestream, DNS.
- TCP Handshake: SYN → SYN-ACK → ACK.