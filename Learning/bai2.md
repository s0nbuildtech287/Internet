````md
# Bài 2 - Phân loại mạng (PAN, LAN, MAN, WAN)

## Mục tiêu

Sau bài này sẽ hiểu:

- Phân biệt PAN, LAN, MAN, WAN.
- Hiểu phạm vi hoạt động của từng loại mạng.
- Biết công nghệ thường sử dụng trong mỗi loại.
- Hiểu Internet là một mạng WAN.
- Có thể xác định loại mạng trong các tình huống thực tế.

---

## Kiến thức cần có

- Đã học Bài 1
- Khái niệm:
  - Node
  - Giao thức
  - Đường truyền
  - Client - Server

---

# Tổng quan

Các mạng được phân loại theo phạm vi địa lý.

```

```
PAN
↓

LAN
↓

MAN
↓

WAN
```

```

```
Nhỏ ---------------------------------------------> Lớn
```

---

# 1. PAN (Personal Area Network)

Mạng cá nhân.

## Phạm vi

Khoảng 1 - 10 mét.

## Công nghệ

- Bluetooth
- NFC
- Zigbee
- USB

## Ví dụ

- Tai nghe Bluetooth
- Đồng hồ thông minh
- Chuột không dây
- Bàn phím Bluetooth

```

```
Điện thoại
     │
Bluetooth
     │
Tai nghe
```

## Đặc điểm

- Tiêu thụ điện thấp
- Khoảng cách ngắn
- Ít thiết bị

---

# 2. LAN (Local Area Network)

Mạng cục bộ.

## Phạm vi

- Nhà
- Văn phòng
- Công ty
- Phòng máy

## Công nghệ

- Ethernet
- WiFi

## Thiết bị

- Router
- Switch
- Access Point

```

```
            Router
               │
        ┌──────┴──────┐
       PC           Laptop
        │
      Printer
```

## Ví dụ

- WiFi nhà
- Công ty
- Quán net

## Đặc điểm

- Tốc độ cao
- Độ trễ thấp
- Dễ quản lý

---

# 3. MAN (Metropolitan Area Network)

Mạng đô thị.

## Phạm vi

Một thành phố.

## Công nghệ

- Metro Ethernet
- Cáp quang

## Ví dụ

- Ngân hàng nhiều chi nhánh
- Đại học nhiều cơ sở
- Mạng truyền hình cáp

```

```
Chi nhánh A
      │
      │
Cáp quang
      │
Chi nhánh B
```

---

# 4. WAN (Wide Area Network)

Mạng diện rộng.

## Phạm vi

- Quốc gia
- Châu lục
- Toàn cầu

## Công nghệ

- MPLS
- Leased Line
- Cáp quang biển
- Vệ tinh

## Ví dụ

- Internet
- Google
- Facebook
- Microsoft

```

```
Việt Nam
     │
Internet
     │
Server Google (USA)
```

---

# So sánh

| Loại | Phạm vi | Ví dụ |
|-------|----------|--------|
| PAN | 1-10m | Bluetooth |
| LAN | Tòa nhà | WiFi |
| MAN | Thành phố | Metro Ethernet |
| WAN | Toàn cầu | Internet |

---

# Quan hệ giữa các loại mạng

```

```
PAN

↓

LAN

↓

MAN

↓

WAN
```

Một mạng nhỏ có thể nằm bên trong mạng lớn hơn.

Ví dụ

```
Tai nghe Bluetooth

↓

Điện thoại

↓

WiFi nhà

↓

Internet

↓

Server YouTube
```

Tương ứng

```
PAN

↓

LAN

↓

WAN
```

---

# Thực hành

## Bài 1

Cho biết loại mạng:

- Tai nghe Bluetooth
- WiFi quán café
- Internet
- Mạng ngân hàng trong Hà Nội

Đáp án

```
Bluetooth → PAN

WiFi → LAN

Internet → WAN

Ngân hàng → MAN
```

---

## Bài 2

Sắp xếp

```
PAN

LAN

MAN

WAN
```

Theo phạm vi từ nhỏ đến lớn.

---

## Bài 3

Quan sát mạng của bạn.

Ví dụ

```
Laptop

↓

WiFi

↓

Router

↓

Internet

↓

Google
```

Hãy xác định đoạn nào là:

- PAN
- LAN
- WAN

---

# Project thực hành

## Mục tiêu

Hiểu rõ PAN, LAN, WAN bằng chương trình thực tế.

---

## Bài 1

Lấy IP máy tính.

NodeJS

```
const os = require("os");

console.log(os.networkInterfaces());
```

Hiểu được:

- IP LAN
- MAC Address

---

## Bài 2

Ping một Website.

Ví dụ

```
ping google.com
```

Quan sát:

- Time
- TTL
- Địa chỉ IP

---

## Bài 3

Viết chương trình DNS Lookup.

Ví dụ

```
node dns.js google.com
```

Kết quả

```
Domain:
google.com

IPv4:
142.xxx.xxx.xxx

IPv6:
....
```

Kiến thức áp dụng

- WAN
- DNS
- Internet

---

## Bài 4

Viết chương trình hiển thị thông tin mạng.

Hiển thị

- Hostname
- IPv4
- IPv6
- MAC
- Gateway

---

# Sau bài này sẽ hiểu

- PAN là gì.
- LAN là gì.
- MAN là gì.
- WAN là gì.
- Internet thuộc loại mạng nào.
- Mạng nhỏ có thể nằm trong mạng lớn hơn.
- Cách xác định loại mạng trong thực tế.

---

# Bài tiếp theo

Topology (Cấu trúc mạng)

- Star
- Bus
- Ring
- Mesh
- Tree

Sau bài này sẽ bắt đầu mô phỏng các mô hình mạng bằng code.
````
