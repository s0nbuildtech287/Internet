# Bài 8: Tầng Data Link - MAC, Frame, Switch & ARP

## 1. Tầng Data Link làm gì?

Tầng **Data Link (Layer 2)** chịu trách nhiệm truyền dữ liệu giữa các thiết bị trong **cùng một mạng LAN**.

### Chức năng chính

- Định danh thiết bị bằng **địa chỉ MAC**.
- Đóng gói dữ liệu thành **Frame**.
- Kiểm tra lỗi bằng **FCS (Frame Check Sequence)**.
- Chuyển dữ liệu trong mạng nội bộ thông qua **Switch**.

> **Lưu ý:** Data Link chỉ hoạt động trong LAN, không định tuyến ra Internet.

---

# 2. Địa chỉ MAC là gì?

MAC (Media Access Control) là địa chỉ phần cứng của card mạng (NIC).

Ví dụ:

```
00:1A:2B:3C:4D:5E
```

- Dài **48 bit (6 byte)**.
- Gần như duy nhất trên toàn thế giới.
- Được nhà sản xuất gán cho card mạng.

### Cấu trúc

```
00:1A:2B : 3C:4D:5E
└── OUI ─┘ └── NIC ─┘
```

- **OUI:** Mã nhà sản xuất.
- **NIC:** Số seri của card mạng.

### Địa chỉ Broadcast

```
FF:FF:FF:FF:FF:FF
```

Frame gửi tới địa chỉ này sẽ được tất cả thiết bị trong LAN nhận.

---

# 3. MAC và IP khác nhau thế nào?

| MAC | IP |
|------|----|
| Địa chỉ phần cứng | Địa chỉ logic |
| Ít thay đổi | Có thể thay đổi |
| Dùng trong LAN | Dùng giữa các mạng |
| Switch sử dụng | Router sử dụng |

Ví dụ:

- MAC giống **số khung xe**.
- IP giống **địa chỉ nhà**.

---

# 4. Cấu trúc Ethernet Frame

```
+-----------+-----------+--------+-------------+------+
| MAC Đích  | MAC Nguồn | Type   |  Payload    | FCS  |
+-----------+-----------+--------+-------------+------+
```

### Các thành phần

### MAC Destination

Thiết bị nhận.

### MAC Source

Thiết bị gửi.

### Type

Cho biết dữ liệu bên trong là gì.

Ví dụ:

- IPv4
- ARP
- IPv6

### Payload

Chứa Packet từ tầng Network.

### FCS

Mã kiểm tra lỗi.

Nếu FCS sai → Frame bị loại bỏ.

---

# 5. Switch hoạt động như thế nào?

Switch hoạt động ở **Layer 2**.

Nó xây dựng **MAC Address Table**.

Ví dụ:

| MAC | Port |
|------|------|
| AA | 1 |
| BB | 2 |
| CC | 3 |

---

## Switch học MAC (MAC Learning)

Khi nhận Frame:

```
PC1 (MAC AA)
      │
      ▼
 Switch
```

Switch ghi:

```
AA → Port 1
```

Lần sau sẽ nhớ luôn.

---

## Switch chuyển Frame

### Trường hợp 1

Đã biết MAC đích.

```
AA ---> Switch ---> BB
```

Switch gửi đúng cổng.

---

### Trường hợp 2

Chưa biết MAC.

Switch sẽ **Flood**.

```
AA ---> Switch

        │
        ├── PC2
        ├── PC3
        └── PC4
```

Máy đúng sẽ trả lời.

Switch ghi nhớ MAC.

Lần sau không Flood nữa.

---

### Trường hợp 3

MAC Broadcast

```
FF:FF:FF:FF:FF:FF
```

Switch gửi ra tất cả các cổng.

---

# 6. ARP là gì?

ARP (Address Resolution Protocol) dùng để:

> **Tìm địa chỉ MAC khi chỉ biết địa chỉ IP.**

Ví dụ:

PC1 muốn gửi cho:

```
192.168.1.5
```

Nhưng chưa biết MAC.

---

## Bước 1

PC1 Broadcast:

```
Ai có IP 192.168.1.5?
```

Địa chỉ đích:

```
FF:FF:FF:FF:FF:FF
```

---

## Bước 2

Máy có IP đó trả lời:

```
MAC của tôi là

BB:BB:BB:BB:BB:BB
```

Đây là ARP Reply.

---

## Bước 3

PC1 lưu vào ARP Cache.

```
192.168.1.5

↓

BB:BB:BB:BB:BB:BB
```

Lần sau không cần hỏi nữa.

---

# 7. ARP Cache

Là bảng lưu:

```
IP

↓

MAC
```

Có thể xem bằng:

Windows

```cmd
arp -a
```

---

# 8. Quá trình gửi dữ liệu trong LAN

Ví dụ:

PC1 gửi dữ liệu cho PC2.

### Bước 1

Đã biết IP.

Chưa biết MAC.

↓

ARP Request.

---

### Bước 2

Nhận được MAC.

---

### Bước 3

Đóng Frame.

```
+---------+---------+---------+
| MAC PC2 | MAC PC1 | Packet  |
+---------+---------+---------+
```

---

### Bước 4

Frame tới Switch.

Switch tra bảng MAC.

↓

Biết PC2 ở Port số 3.

↓

Chỉ gửi ra Port 3.

---

### Bước 5

PC2 nhận Frame.

↓

Kiểm tra FCS.

↓

Bóc Frame.

↓

Lấy Packet.

↓

Chuyển lên tầng Network.

---

# 9. Nếu gửi ra Internet thì sao?

Nếu IP đích không cùng mạng LAN.

PC1 **không gửi trực tiếp**.

Nó gửi Frame tới:

**Default Gateway (Router).**

Router sẽ định tuyến sang mạng khác.

---

# 10. Các lệnh nên biết

### Windows

Xem MAC

```cmd
ipconfig /all
```

Xem ARP

```cmd
arp -a
```

---

### Linux

```bash
ip link
```

hoặc

```bash
ifconfig
```

---

# Tóm tắt

- Data Link (Layer 2) truyền dữ liệu trong LAN.
- Dùng địa chỉ MAC.
- Đóng dữ liệu thành Frame.
- Switch dựa vào MAC để chuyển Frame.
- ARP dùng để tìm MAC từ IP.
- ARP Cache lưu các cặp IP ↔ MAC.
- FCS dùng để kiểm tra lỗi.
- Muốn ra Internet phải gửi tới Router.

---

# Mẹo ghi nhớ

```
MAC
↓
Switch
↓
Frame
↓
ARP
↓
LAN
```

**Một câu nhớ:**

> **Switch đọc MAC để chuyển Frame trong LAN; ARP giúp tìm MAC khi chỉ biết IP.**