# Bài 9: Địa chỉ IPv4

## 1. IPv4 là gì?

IPv4 (Internet Protocol Version 4) là địa chỉ logic dùng để định danh một thiết bị trên mạng.

Ví dụ:

```
192.168.1.25
```

IPv4 gồm:

- 32 bit
- 4 Octet
- Mỗi Octet = 8 bit
- Giá trị từ **0 → 255**

Ví dụ:

```
192 . 168 . 1 . 25
 │      │     │    │
Octet Octet Octet Octet
```

Tổng số địa chỉ:

```
2^32 ≈ 4,3 tỷ địa chỉ
```

---

# 2. Vì sao mỗi Octet chỉ từ 0 đến 255?

Một Octet có 8 bit.

```
11111111
```

Giá trị lớn nhất:

```
2^8 = 256 giá trị

0 → 255
```

Do đó:

```
192.168.1.255 ✔

192.168.1.300 ✘
```

---

# 3. Network và Host

Một địa chỉ IP luôn được chia thành hai phần:

- Network (Mạng)
- Host (Thiết bị)

Ví dụ:

```
192.168.1.25/24
```

```
192.168.1 | 25
──────────┬────
 Network  │ Host
```

Ý nghĩa:

- **Network** → Thiết bị thuộc mạng nào.
- **Host** → Thiết bị nào trong mạng đó.

Có thể hiểu như:

```
Tên đường

↓

Số nhà
```

---

# 4. Subnet Mask

Subnet Mask dùng để xác định đâu là Network và đâu là Host.

Ví dụ:

```
255.255.255.0
```

Có nghĩa:

- 24 bit đầu là Network
- 8 bit cuối là Host

Hay viết ngắn:

```
/24
```

Ví dụ:

```
192.168.1.25/24
```

---

# 5. Hai máy nói chuyện với nhau khi nào?

Nếu:

```
Network giống nhau
```

↓

Hai máy có thể giao tiếp trực tiếp.

Nếu:

```
Network khác nhau
```

↓

Phải đi qua Router.

---

# 6. Class của IPv4 (Lịch sử)

Ngày xưa IPv4 chia thành các lớp.

| Class | Octet đầu | Dải IP | Mục đích |
|--------|-----------|---------|----------|
| A | 1 - 126 | 1.x.x.x | Mạng lớn |
| B | 128 - 191 | 128.x.x.x | Mạng vừa |
| C | 192 - 223 | 192.x.x.x | LAN nhỏ |
| D | 224 - 239 | Multicast | Gửi nhóm |
| E | 240 - 255 | Reserved | Thử nghiệm |

Hiện nay Class gần như không còn dùng.

Đã thay bằng CIDR.

---

# 7. Public IP và Private IP

## Public IP

- Có thể truy cập từ Internet.
- Do ISP cấp.
- Không được trùng nhau.

Ví dụ:

```
8.8.8.8
```

---

## Private IP

Chỉ dùng trong mạng nội bộ.

Không xuất hiện trực tiếp trên Internet.

Ba dải Private cần nhớ:

```
10.0.0.0
↓

10.255.255.255
```

```
172.16.0.0
↓

172.31.255.255
```

```
192.168.0.0
↓

192.168.255.255
```

Ví dụ:

```
192.168.1.10
```

Đây là IP Private.

---

# 8. Public và Private khác nhau

| Public | Private |
|---------|----------|
| Toàn cầu | Nội bộ |
| Không trùng | Có thể trùng |
| ISP cấp | Router cấp |
| Truy cập Internet trực tiếp | Qua NAT |

---

# 9. Địa chỉ đặc biệt

## Loopback

```
127.0.0.1
```

Hay còn gọi là:

```
localhost
```

Dùng để kiểm tra chính máy mình.

Ví dụ:

```cmd
ping 127.0.0.1
```

Gói tin không đi ra mạng.

---

## Network Address

Ví dụ:

```
192.168.1.0
```

Đây là địa chỉ mạng.

Không gán cho máy.

---

## Broadcast

Ví dụ:

```
192.168.1.255
```

Gửi tới tất cả thiết bị trong mạng.

---

## 0.0.0.0

Có nghĩa:

- Chưa xác định địa chỉ.
- Hoặc "mọi địa chỉ" tùy ngữ cảnh.

---

## APIPA

```
169.254.x.x
```

Xuất hiện khi:

Máy không xin được IP từ DHCP.

Windows sẽ tự cấp IP.

---

# 10. Vì sao IPv4 sắp hết?

IPv4 chỉ có:

```
≈ 4,3 tỷ địa chỉ
```

Trong khi:

- Điện thoại
- Laptop
- Camera
- Smart TV
- IoT
- Server

đều cần IP.

Do đó địa chỉ IPv4 dần cạn kiệt.

---

# 11. Hai giải pháp

## NAT

Nhiều máy dùng chung một Public IP.

Ví dụ:

```
PC1

PC2

PC3

↓

Router

↓

1 Public IP
```

Đây là cách hầu hết mạng gia đình đang hoạt động.

---

## IPv6

IPv6 dùng:

```
128 bit
```

Số lượng địa chỉ gần như vô hạn.

Là giải pháp lâu dài.

---

# 12. Kiểm tra IP trên máy

### Windows

```cmd
ipconfig
```

Hoặc

```cmd
ipconfig /all
```

---

### Linux

```bash
ip addr
```

hoặc

```bash
ifconfig
```

---

# Tóm tắt

- IPv4 là địa chỉ logic của tầng Network.
- Gồm 32 bit (4 Octet).
- Mỗi Octet từ 0 → 255.
- Được chia thành Network và Host.
- Cùng Network → giao tiếp trực tiếp.
- Khác Network → phải qua Router.
- Có Public IP và Private IP.
- Ba dải Private cần nhớ:
  - 10.x.x.x
  - 172.16–31.x.x
  - 192.168.x.x
- 127.0.0.1 là Loopback.
- IPv4 đang cạn kiệt nên cần NAT và IPv6.

---

# Mẹo ghi nhớ

```
IPv4

↓

32 bit

↓

4 Octet

↓

Network + Host

↓

Public / Private

↓

Router định tuyến
```

**Một câu nhớ:**

> **MAC dùng trong LAN, IP dùng giữa các mạng; IPv4 gồm 32 bit chia thành Network và Host để Router định tuyến dữ liệu.**