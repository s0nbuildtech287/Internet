# Bài 4 - Thiết bị mạng cơ bản

## Mục tiêu

Sau bài này sẽ hiểu:

- NIC là gì.
- Hub là gì.
- Switch là gì.
- Router là gì.
- Modem là gì.
- Access Point là gì.
- Phân biệt Hub, Switch và Router.
- Hiểu "Router WiFi" ở nhà thực chất là nhiều thiết bị tích hợp.
- Biết Switch làm việc với địa chỉ MAC, Router làm việc với địa chỉ IP.

---

## Kiến thức cần có

- Bài 1: Khái niệm mạng
- Bài 2: PAN, LAN, MAN, WAN
- Bài 3: Topology

---

# Tổng quan

Muốn các thiết bị giao tiếp được với nhau cần có thiết bị mạng.

Ví dụ:

```
Laptop
      │
      │
   Switch
      │
   Router
      │
    Modem
      │
  Internet
```

Mỗi thiết bị có một nhiệm vụ khác nhau.

---

# 1. NIC (Network Interface Card)

NIC là card mạng.

Không có NIC thì thiết bị không thể kết nối mạng.

## Chức năng

- Gửi dữ liệu
- Nhận dữ liệu
- Kết nối Ethernet hoặc WiFi

## Đặc điểm

- Mỗi NIC có một địa chỉ MAC duy nhất.
- Có thể là card LAN hoặc card WiFi.

Ví dụ:

```
Laptop

↓

Card WiFi

↓

Router
```

Hoặc

```
PC

↓

Card LAN

↓

Switch
```

---

## Ví dụ thực tế

- Cổng RJ45 phía sau máy tính.
- Card WiFi trong laptop.
- Chip WiFi trong điện thoại.

---

# 2. Hub

Hub là thiết bị kết nối nhiều máy tính.

Tuy nhiên Hub rất "ngây thơ".

Nó nhận dữ liệu từ một cổng rồi phát ra tất cả các cổng còn lại.

```
      PC1

       │

PC2 --- Hub --- PC3

       │

      PC4
```

Nếu PC1 gửi dữ liệu cho PC3

Hub sẽ gửi tới:

- PC2
- PC3
- PC4

Tất cả đều nhận.

---

## Ưu điểm

- Giá rẻ.
- Dễ sử dụng.

---

## Nhược điểm

- Tốn băng thông.
- Dễ xảy ra Collision.
- Bảo mật kém.
- Hiệu năng thấp.

---

## Hiện nay

Hub gần như không còn sử dụng.

---

# 3. Switch

Switch là phiên bản thông minh của Hub.

Switch học địa chỉ MAC của từng thiết bị.

Khi có dữ liệu

↓

Switch chỉ gửi đúng máy nhận.

```
      PC1

       │

PC2 -- Switch -- PC3

       │

      PC4
```

Nếu

```
PC1

↓

PC3
```

Switch chỉ gửi tới:

```
PC3
```

PC2 và PC4 sẽ không nhận.

---

## Switch hoạt động như thế nào?

Switch xây dựng bảng MAC.

Ví dụ

| MAC | Port |
|------|------|
| AA:11 | Port 1 |
| BB:22 | Port 2 |
| CC:33 | Port 3 |

Khi nhận dữ liệu

↓

Đọc MAC đích

↓

Tra bảng

↓

Gửi đúng cổng.

---

## Ưu điểm

- Nhanh.
- Ít Collision.
- Bảo mật tốt hơn Hub.
- Hiệu năng cao.

---

## Nhược điểm

- Giá cao hơn Hub.
- Chỉ hoạt động trong LAN.

---

# Hub vs Switch

| Hub | Switch |
|------|---------|
| Gửi mọi cổng | Gửi đúng cổng |
| Không biết MAC | Biết MAC |
| Chậm | Nhanh |
| Collision cao | Collision thấp |

---

# 4. Router

Router dùng để kết nối các mạng với nhau.

Ví dụ

```
Laptop

↓

Switch

↓

Router

↓

Internet
```

Router không quan tâm MAC.

Router quan tâm

```
IP Address
```

---

## Nhiệm vụ

- Định tuyến.
- Chọn đường đi.
- Kết nối LAN với Internet.

---

## Router hoạt động

Ví dụ

```
192.168.1.100

↓

Google.com
```

Router sẽ

↓

Đọc IP

↓

Tra bảng định tuyến

↓

Chuyển dữ liệu sang ISP.

---

## Router còn có

- NAT
- DHCP
- Firewall

---

# Switch vs Router

| Switch | Router |
|----------|---------|
| Dựa vào MAC | Dựa vào IP |
| Trong LAN | Giữa nhiều mạng |
| Không ra Internet | Có thể ra Internet |

---

# 5. Modem

Modem là thiết bị chuyển đổi tín hiệu.

Tên đầy đủ

```
MOdulator

DEModulator
```

---

## Nhiệm vụ

Chuyển đổi tín hiệu giữa

```
Nhà mạng

↓

Router
```

Ví dụ

```
ISP

↓

Cáp quang

↓

Modem

↓

Router
```

Không có Modem

↓

Không thể kết nối Internet.

---

# 6. Access Point (AP)

Access Point phát WiFi.

```
Internet

↓

Router

↓

Access Point

↓

Laptop

↓

Điện thoại
```

---

## Nhiệm vụ

- Phát SSID.
- Cho thiết bị WiFi kết nối.

Ví dụ

```
Tên WiFi

MyHome_5G
```

Đó là SSID.

---

# Router WiFi ở nhà thực chất là gì?

Thiết bị nhà mạng lắp thường tích hợp nhiều chức năng.

```
+-----------------------------+

Modem

Router

Switch

Access Point

+-----------------------------+
```

Nó vừa

- Nhận Internet
- Định tuyến
- Có cổng LAN
- Phát WiFi

Nên mọi người thường gọi chung là

```
Router WiFi
```

---

# Thiết bị hoạt động ở tầng nào?

| Thiết bị | Địa chỉ sử dụng | Tầng OSI |
|-----------|-----------------|----------|
| Hub | Không đọc địa chỉ | Layer 1 |
| Switch | MAC | Layer 2 |
| Router | IP | Layer 3 |

Có thể nhớ:

```
Hub

↓

Switch

↓

Router
```

Thiết bị càng xuống dưới càng "thông minh".

---

# So sánh nhanh

| Thiết bị | Chức năng |
|-----------|-----------|
| NIC | Kết nối mạng |
| Hub | Phát mọi cổng |
| Switch | Gửi đúng MAC |
| Router | Kết nối nhiều mạng |
| Modem | Chuyển đổi tín hiệu |
| AP | Phát WiFi |

---

# Sơ đồ tổng thể

```
Laptop

↓

NIC

↓

Switch

↓

Router

↓

Modem

↓

ISP

↓

Internet
```

---

# Thực hành

## Bài 1

Quan sát Router nhà bạn.

Tìm:

- Bao nhiêu cổng LAN?
- Có phát WiFi không?
- Tên SSID là gì?

---

## Bài 2

Giải thích

PC1 gửi dữ liệu tới PC3.

Hub làm gì?

Switch làm gì?

---

## Bài 3

Cho sơ đồ

```
Laptop

↓

Router

↓

Internet
```

Thiết bị nào sử dụng:

- MAC
- IP

---

# Project thực hành

## Project 1

Hiển thị địa chỉ MAC của máy.

NodeJS

```js
const os = require("os");

console.log(os.networkInterfaces());
```

---

## Project 2

Lấy IP của máy.

Hiển thị

- IPv4
- IPv6
- MAC

---

## Project 3

Mô phỏng Hub

```
Client A

↓

Hub

↓

Client B

↓

Client C

↓

Client D
```

Mọi Client đều nhận dữ liệu.

---

## Project 4

Mô phỏng Switch

```
Client A

↓

Switch

↓

Client C
```

Chỉ Client C nhận.

---

## Project 5

Mô phỏng Router

```
LAN A

↓

Router

↓

LAN B
```

Router đọc IP và chuyển tiếp dữ liệu.

---

# Sau bài này sẽ hiểu

- NIC là gì.
- Hub là gì.
- Switch là gì.
- Router là gì.
- Modem là gì.
- Access Point là gì.
- Phân biệt MAC và IP.
- Phân biệt Hub, Switch và Router.
- Vì sao Router WiFi ở nhà thực chất là thiết bị tích hợp nhiều chức năng.

---

# Bài tiếp theo

Mô hình OSI 7 tầng

- Layer 1: Physical
- Layer 2: Data Link
- Layer 3: Network
- Layer 4: Transport
- Layer 5: Session
- Layer 6: Presentation
- Layer 7: Application

Sau bài này sẽ hiểu dữ liệu đi qua từng tầng của mạng như thế nào.