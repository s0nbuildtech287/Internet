# Bài 6 - Mô hình TCP/IP

## Mục tiêu

Sau bài này sẽ hiểu:

- TCP/IP là gì.
- Vì sao Internet sử dụng TCP/IP thay vì OSI.
- Chức năng của 4 tầng TCP/IP.
- So sánh TCP/IP với OSI.
- Phân biệt TCP và IP.
- Biết các giao thức hoạt động ở từng tầng.

---

## Kiến thức cần có

- Bài 1: Khái niệm mạng
- Bài 2: Phân loại mạng
- Bài 3: Topology
- Bài 4: Thiết bị mạng
- Bài 5: Mô hình OSI

---

# Giới thiệu

Ở bài trước chúng ta đã học mô hình **OSI 7 tầng**.

Tuy nhiên:

> Internet thực tế **không chạy theo OSI**.

Internet sử dụng mô hình

```
TCP/IP
```

TCP/IP là bộ giao thức giúp hàng tỷ thiết bị trên toàn thế giới có thể giao tiếp với nhau.

Tên gọi TCP/IP được lấy từ hai giao thức quan trọng nhất:

- TCP (Transmission Control Protocol)
- IP (Internet Protocol)

---

# TCP/IP là gì?

TCP/IP là bộ giao thức nền tảng của Internet.

Mỗi khi:

- Truy cập Website
- Gửi Email
- Chat Messenger
- Chơi Game Online
- Gọi Video

↓

đều sử dụng TCP/IP.

---

# TCP làm gì?

TCP (Transmission Control Protocol)

Nhiệm vụ:

- Đảm bảo dữ liệu đến đầy đủ.
- Đúng thứ tự.
- Không bị mất.
- Không bị trùng.

Ví dụ

```
Gửi 100 gói tin

↓

TCP kiểm tra

↓

Nếu thiếu gói số 35

↓

Yêu cầu gửi lại.
```

---

# IP làm gì?

IP (Internet Protocol)

Nhiệm vụ:

- Gán địa chỉ IP.
- Định tuyến.
- Chọn đường đi.

Ví dụ

```
192.168.1.10

↓

8.8.8.8
```

Router sẽ dựa vào IP để chuyển tiếp dữ liệu.

---

# TCP/IP có 4 tầng

```
+----------------------------------+
| Layer 4 | Application            |
+----------------------------------+
| Layer 3 | Transport              |
+----------------------------------+
| Layer 2 | Internet               |
+----------------------------------+
| Layer 1 | Network Access         |
+----------------------------------+
```

Khác với OSI

```
OSI

↓

7 tầng

TCP/IP

↓

4 tầng
```

---

# Layer 1 - Network Access

Là tầng gần phần cứng nhất.

Gộp:

```
OSI Layer 1

+

OSI Layer 2
```

Quan tâm

- MAC
- Ethernet
- WiFi
- Cáp mạng

Giao thức

- Ethernet
- IEEE 802.11

Thiết bị

- NIC
- Switch

---

# Layer 2 - Internet

Tương ứng

```
OSI Layer 3
```

Quan tâm

- IP
- Routing
- ICMP

Ví dụ

```
ping google.com
```

sử dụng

```
ICMP
```

Thiết bị

```
Router
```

---

# Layer 3 - Transport

Tương ứng

```
OSI Layer 4
```

Quan tâm

- TCP
- UDP
- Port

Ví dụ

```
80

443

3306

5432
```

---

# TCP

Đặc điểm

- Có kết nối.
- Tin cậy.
- Có ACK.
- Có kiểm tra lỗi.
- Có gửi lại.

Ví dụ

```
HTTP

HTTPS

SSH

FTP
```

đều dùng TCP.

---

# UDP

Đặc điểm

- Không kết nối.
- Không gửi lại.
- Nhanh.

Ví dụ

- Livestream
- Video Call
- Game Online
- DNS

---

# Layer 4 - Application

Là tầng gần người dùng nhất.

Gộp

```
OSI Layer

5

6

7
```

Bao gồm

- HTTP
- HTTPS
- FTP
- SMTP
- DNS

Ví dụ

```
Chrome

↓

HTTP

↓

TCP

↓

IP

↓

Internet
```

---

# So sánh OSI và TCP/IP

```
OSI                     TCP/IP

Application

Presentation

Session

↓

Application

------------------------

Transport

↓

Transport

------------------------

Network

↓

Internet

------------------------

Data Link

Physical

↓

Network Access
```

---

# Bảng ánh xạ

| OSI | TCP/IP |
|------|---------|
| Application | Application |
| Presentation | Application |
| Session | Application |
| Transport | Transport |
| Network | Internet |
| Data Link | Network Access |
| Physical | Network Access |

---

# TCP/IP hay OSI?

| OSI | TCP/IP |
|------|---------|
| Mô hình lý thuyết | Mô hình thực tế |
| 7 tầng | 4 tầng |
| Dùng để học | Dùng để vận hành Internet |

Có thể nhớ:

```
OSI

↓

Học

TCP/IP

↓

Chạy thật
```

---

# Giao thức theo từng tầng

| TCP/IP | Giao thức |
|----------|-----------|
| Application | HTTP, HTTPS, DNS, FTP, SMTP |
| Transport | TCP, UDP |
| Internet | IP, ICMP |
| Network Access | Ethernet, WiFi |

---

# Ví dụ mở Website

Bạn truy cập

```
https://google.com
```

Quá trình

```
Chrome

↓

HTTP Request

↓

TCP

↓

IP

↓

Ethernet

↓

Router

↓

Internet

↓

Google Server
```

Google Server xử lý

↓

Trả dữ liệu về

↓

Theo chiều ngược lại.

---

# Luồng dữ liệu

```
Application

↓

Transport

↓

Internet

↓

Network Access

↓

Internet

↓

Network Access

↓

Internet

↓

Transport

↓

Application
```

---

# Encapsulation

Máy gửi

```
HTTP

↓

TCP Header

↓

IP Header

↓

Ethernet Header

↓

Bit
```

Mỗi tầng thêm Header riêng.

---

# De-encapsulation

Máy nhận

```
Bit

↓

Ethernet

↓

IP

↓

TCP

↓

HTTP
```

Mỗi tầng bỏ Header của mình.

---

# So sánh TCP và IP

| TCP | IP |
|------|----|
| Đảm bảo dữ liệu | Định tuyến |
| Có ACK | Không ACK |
| Có Port | Có IP |
| Tin cậy | Không đảm bảo |

---

# Thực hành

## Bài 1

Viết lại 4 tầng TCP/IP theo thứ tự.

---

## Bài 2

Ghép giao thức:

- HTTP
- TCP
- UDP
- IP
- Ethernet
- WiFi

với tầng tương ứng.

---

## Bài 3

So sánh:

OSI

↓

TCP/IP

khác nhau ở điểm nào?

---

# Project thực hành

## Project 1

HTTP Server

```js
const http = require("http");

http.createServer((req, res) => {
  res.end("Hello TCP/IP");
}).listen(3000);
```

Hiểu

- HTTP
- TCP
- IP

---

## Project 2

TCP Socket

```js
const net = require("net");
```

Tạo TCP Server.

---

## Project 3

UDP Socket

```js
const dgram = require("dgram");
```

So sánh TCP và UDP.

---

## Project 4

Ping Website

```bash
ping google.com
```

Quan sát

- IP
- TTL
- RTT

---

## Project 5

Traceroute

Windows

```bash
tracert google.com
```

Linux

```bash
traceroute google.com
```

Quan sát Router mà gói tin đi qua.

---

# Hiểu lầm thường gặp

❌ TCP/IP chỉ gồm TCP và IP.

✅ Sai.

TCP/IP là cả một bộ giao thức gồm:

- HTTP
- HTTPS
- DNS
- SMTP
- FTP
- TCP
- UDP
- ICMP
- IP

---

❌ TCP và IP làm cùng một việc.

✅ Sai.

TCP

↓

Đảm bảo dữ liệu.

IP

↓

Định tuyến.

---

❌ OSI và TCP/IP đối lập nhau.

✅ Sai.

OSI dùng để học.

TCP/IP dùng để vận hành.

Hai mô hình bổ sung cho nhau.

---

# Mẹo ghi nhớ

- TCP/IP có **4 tầng**.
- OSI có **7 tầng**.
- TCP = Tin cậy.
- UDP = Nhanh.
- IP = Địa chỉ + Định tuyến.
- Application = HTTP.
- Transport = TCP/UDP.
- Internet = IP.
- Network Access = Ethernet/WiFi.

---

# Sau bài này sẽ hiểu

- TCP/IP là gì.
- Vai trò của TCP và IP.
- 4 tầng của TCP/IP.
- Ánh xạ TCP/IP với OSI.
- Luồng dữ liệu khi truy cập Internet.
- Vì sao Internet sử dụng TCP/IP thay vì OSI.

---

# Bài tiếp theo

## Encapsulation (Đóng gói dữ liệu)

Nội dung:

- Header là gì.
- Encapsulation.
- De-encapsulation.
- Segment, Packet, Frame, Bit.
- Hành trình của một gói tin từ máy gửi đến máy nhận.