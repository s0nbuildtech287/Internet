# Bài 5 - Mô hình OSI 7 tầng

## Mục tiêu

Sau bài này sẽ hiểu:

- Vì sao cần mô hình OSI.
- Chức năng của 7 tầng trong mô hình OSI.
- Thiết bị và giao thức hoạt động ở từng tầng.
- Luồng dữ liệu đi qua các tầng.
- Phân biệt OSI và TCP/IP.
- Ghi nhớ địa chỉ MAC, IP, Port tương ứng với từng tầng.

---

## Kiến thức cần có

- Bài 1: Khái niệm mạng
- Bài 2: Phân loại mạng
- Bài 3: Topology
- Bài 4: Thiết bị mạng

---

# Giới thiệu

Khi truyền dữ liệu qua mạng, nếu tất cả công việc đều được xử lý trong một khối duy nhất thì hệ thống sẽ rất khó phát triển, bảo trì và sửa lỗi.

Để giải quyết vấn đề đó, người ta chia toàn bộ quá trình truyền dữ liệu thành nhiều tầng (Layer). Mỗi tầng đảm nhận một nhiệm vụ riêng và giao tiếp với tầng kế tiếp.

Đó chính là mô hình **OSI (Open Systems Interconnection)**.

---

# Vì sao cần chia tầng?

## Chia để trị

Mỗi tầng chỉ thực hiện một nhiệm vụ.

Ví dụ:

- Tầng 1 truyền tín hiệu.
- Tầng 2 truyền dữ liệu trong LAN.
- Tầng 3 định tuyến.
- Tầng 4 đảm bảo dữ liệu đến đúng ứng dụng.

---

## Độc lập

Ví dụ:

Đổi

```
WiFi

↓

Ethernet
```

không cần sửa trình duyệt.

---

## Chuẩn hóa

Thiết bị của Cisco, Juniper, TP-Link...

↓

vẫn giao tiếp được với nhau.

---

## Dễ sửa lỗi

Ví dụ

Không ping được

↓

Kiểm tra Layer 3.

Không có tín hiệu

↓

Kiểm tra Layer 1.

---

# Tổng quan 7 tầng

```
+------------------------------------+
| Layer 7 | Application              |
+------------------------------------+
| Layer 6 | Presentation             |
+------------------------------------+
| Layer 5 | Session                  |
+------------------------------------+
| Layer 4 | Transport                |
+------------------------------------+
| Layer 3 | Network                  |
+------------------------------------+
| Layer 2 | Data Link                |
+------------------------------------+
| Layer 1 | Physical                 |
+------------------------------------+
```

Dữ liệu đi

```
Máy gửi

↓

Layer 7

↓

Layer 6

↓

...

↓

Layer 1

↓

Đường truyền

↓

Layer 1

↓

...

↓

Layer 7

↓

Máy nhận
```

---

# Layer 1 - Physical

Là tầng thấp nhất.

Nhiệm vụ:

Truyền các bit 0 và 1.

Quan tâm:

- Cáp mạng
- Sóng WiFi
- Điện áp
- Tín hiệu

Thiết bị:

- Hub
- Repeater
- Cáp mạng

Đơn vị dữ liệu:

```
Bit
```

Ví dụ:

```
0001010110010110
```

---

# Layer 2 - Data Link

Đóng gói dữ liệu thành Frame.

Làm việc trong cùng một mạng LAN.

Sử dụng

```
MAC Address
```

Thiết bị:

- Switch
- NIC

Ví dụ:

```
MAC

AA:BB:CC:DD:EE:FF
```

Đơn vị dữ liệu:

```
Frame
```

---

# Layer 3 - Network

Kết nối các mạng khác nhau.

Định tuyến.

Sử dụng

```
IP Address
```

Ví dụ

```
192.168.1.100

↓

8.8.8.8
```

Thiết bị:

```
Router
```

Đơn vị dữ liệu

```
Packet
```

---

# Layer 4 - Transport

Đảm bảo dữ liệu đến đúng ứng dụng.

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

Đơn vị dữ liệu

```
Segment
```

---

# Layer 5 - Session

Quản lý phiên làm việc.

Ví dụ

```
Đăng nhập

↓

Giữ phiên

↓

Đăng xuất
```

Hoặc

```
Cuộc gọi Zoom
```

↓

Giữ kết nối.

---

# Layer 6 - Presentation

Chuyển đổi dữ liệu.

Bao gồm

- Mã hóa
- Giải mã
- Nén
- Giải nén
- Chuyển đổi định dạng

Ví dụ

```
HTTPS

↓

TLS
```

Hoặc

```
JPEG

PNG

UTF-8
```

---

# Layer 7 - Application

Là tầng gần người dùng nhất.

Không phải trình duyệt.

Mà là

```
HTTP

HTTPS

DNS

SMTP

FTP
```

Ví dụ

```
Chrome

↓

HTTP

↓

Internet
```

---

# Mẹo nhớ

Từ Layer 1 đến Layer 7

```
Please

Do

Not

Throw

Sausage

Pizza

Away
```

Hoặc

```
Physical

Data Link

Network

Transport

Session

Presentation

Application
```

---

# Thiết bị theo từng tầng

| Layer | Thiết bị |
|---------|----------|
| 1 | Hub |
| 2 | Switch |
| 3 | Router |

---

# Địa chỉ theo từng tầng

| Layer | Địa chỉ |
|---------|----------|
| 2 | MAC |
| 3 | IP |
| 4 | Port |

---

# Đơn vị dữ liệu (PDU)

| Layer | PDU |
|---------|------|
| 7 | Data |
| 6 | Data |
| 5 | Data |
| 4 | Segment |
| 3 | Packet |
| 2 | Frame |
| 1 | Bit |

Có thể nhớ:

```
Segment

↓

Packet

↓

Frame

↓

Bit
```

---

# Luồng dữ liệu

Ví dụ

Người dùng truy cập

```
https://google.com
```

Quá trình:

```
Application

↓

Presentation

↓

Session

↓

Transport

↓

Network

↓

Data Link

↓

Physical

↓

Internet

↓

Physical

↓

...

↓

Application
```

Máy gửi

↓

Đóng gói dữ liệu.

Máy nhận

↓

Bóc từng lớp dữ liệu.

---

# Encapsulation

Máy gửi

```
Data

↓

Segment

↓

Packet

↓

Frame

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

Frame

↓

Packet

↓

Segment

↓

Data
```

Mỗi tầng bỏ Header của mình.

---

# So sánh nhanh

| Layer | Chức năng |
|---------|-----------|
| 7 | Giao tiếp ứng dụng |
| 6 | Mã hóa, nén |
| 5 | Quản lý phiên |
| 4 | TCP, UDP, Port |
| 3 | IP, Routing |
| 2 | MAC, Switch |
| 1 | Cáp, Sóng |

---

# Ví dụ thực tế

```
Chrome

↓

HTTP

↓

TCP

↓

IP

↓

Ethernet

↓

Cáp mạng

↓

Router

↓

Internet

↓

Google Server
```

Đây chính là dữ liệu đi qua các tầng.

---

# Thực hành

## Bài 1

Viết lại 7 tầng theo thứ tự.

---

## Bài 2

Ghép đúng:

- MAC
- IP
- Port
- HTTP

với tầng tương ứng.

---

## Bài 3

Cho biết:

Switch hoạt động tầng nào?

Router hoạt động tầng nào?

Hub hoạt động tầng nào?

---

# Project thực hành

## Project 1

Hiển thị thông tin mạng.

NodeJS

```js
const os = require("os");

console.log(os.networkInterfaces());
```

Quan sát:

- IPv4
- IPv6
- MAC

---

## Project 2

HTTP Server

Tự xây dựng bằng module `http`.

Qua project sẽ hiểu:

- Layer 7
- Layer 4
- Layer 3

---

## Project 3

TCP Chat

Hiểu

- TCP
- Port
- Session

---

## Project 4

Ping Website

```bash
ping google.com
```

Quan sát:

- IP
- TTL
- Thời gian phản hồi

---

## Project 5

DNS Lookup

```js
const dns = require("dns");

dns.lookup("google.com", console.log);
```

Hiểu

- Layer 7
- Layer 3

---

# Hiểu lầm thường gặp

❌ Layer 7 là trình duyệt.

✅ Sai.

Layer 7 là giao thức như:

- HTTP
- HTTPS
- DNS
- SMTP

Chrome chỉ sử dụng các giao thức đó.

---

❌ Internet chạy đúng theo OSI.

✅ Sai.

OSI chỉ là mô hình tham chiếu.

Internet thực tế sử dụng mô hình TCP/IP.

---

❌ Layer 1 là tầng cao nhất.

✅ Sai.

Layer 1 ở gần phần cứng nhất.

Layer 7 ở gần người dùng nhất.

---

# Mẹo ghi nhớ

- Hub → Layer 1
- Switch → Layer 2
- Router → Layer 3

- MAC → Layer 2
- IP → Layer 3
- Port → Layer 4

- Segment → Packet → Frame → Bit

---

# Sau bài này sẽ hiểu

- Vì sao cần mô hình OSI.
- Chức năng của từng tầng.
- Dữ liệu đi qua 7 tầng như thế nào.
- Thiết bị hoạt động ở tầng nào.
- MAC, IP, Port thuộc tầng nào.
- Khái niệm Encapsulation và De-encapsulation.

---

# Bài tiếp theo

## Mô hình TCP/IP

Nội dung:

- Vì sao Internet không dùng OSI.
- So sánh OSI và TCP/IP.
- 4 tầng của TCP/IP.
- Ánh xạ giữa OSI và TCP/IP.
- Vai trò của TCP/IP trong Internet hiện đại.