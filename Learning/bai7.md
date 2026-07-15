# Bài 7 - Đóng gói dữ liệu (Encapsulation)

## Mục tiêu

Sau bài này sẽ hiểu:

- Encapsulation là gì.
- De-encapsulation là gì.
- Header và Trailer là gì.
- Vì sao dữ liệu đổi tên theo từng tầng.
- Hiểu PDU của từng tầng.
- Hiểu Overhead trong truyền dữ liệu.

---

## Kiến thức cần có

- Bài 5: Mô hình OSI
- Bài 6: Mô hình TCP/IP

---

# Giới thiệu

Khi bạn gửi một tin nhắn qua Internet, dữ liệu **không được gửi trực tiếp**.

Thay vào đó, mỗi tầng trong mô hình TCP/IP sẽ **bọc thêm thông tin của mình** vào dữ liệu trước khi chuyển xuống tầng dưới.

Quá trình này gọi là:

```
Encapsulation
(Đóng gói dữ liệu)
```

Ở phía máy nhận, dữ liệu sẽ được **mở từng lớp** theo thứ tự ngược lại.

Quá trình này gọi là:

```
De-encapsulation
(Mở gói dữ liệu)
```

---

# Encapsulation là gì?

Encapsulation là quá trình:

```
Application

↓

Transport

↓

Internet

↓

Network Access

↓

Đường truyền
```

Mỗi tầng sẽ:

- Thêm Header.
- Có thể thêm Trailer.
- Chuyển xuống tầng dưới.

---

# Ví dụ đơn giản

Giả sử bạn gửi tin nhắn chỉ có 2 chữ cái (chiếm 2 byte dữ liệu):

```
Hi
```

### Bước 1: Dữ liệu thô (DATA) ở tầng Application
Dữ liệu gốc là chuỗi mã UTF-8 của chữ "Hi" (Byte 1: `0x48`, Byte 2: `0x69`).
* Kích thước: **2 Byte**
* Tên gọi PDU: **Data**

### Bước 2: Thêm TCP Header ở tầng Transport (Layer 4)
Tầng Transport bọc dữ liệu trong một **TCP Header** 20 byte:
* **Port nguồn (Source Port)**: `54321` (2 byte) - Cổng ngẫu nhiên do hệ điều hành cấp cho ứng dụng của bạn.
* **Port đích (Destination Port)**: `80` (2 byte) - Cổng mặc định của dịch vụ Web HTTP.
* **Sequence Number**: `1000` (4 byte) - Số thứ tự gói tin để sắp xếp đúng vị trí ở máy nhận.
* **ACK Number**: `0` (4 byte) - Số xác nhận.
* **Window Size, Flags, Checksum**: (8 byte còn lại) để kiểm soát luồng và bảo mật.
* Tên gọi PDU lúc này: **Segment** (Kích thước: 2 + 20 = **22 Byte**)
* Gói tin có dạng:
```
[TCP Header: Src Port 54321, Dst Port 80, Seq 1000...] [ Dữ liệu: "Hi" ]
```

### Bước 3: Thêm IP Header ở tầng Internet (Layer 3)
Tầng Internet bọc Segment TCP bằng một **IP Header** 20 byte để dẫn đường trên mạng:
* **IP nguồn (Source IP)**: `192.168.1.10` (4 byte) - IP máy tính của bạn.
* **IP đích (Destination IP)**: `8.8.8.8` (4 byte) - IP máy chủ Google.
* **TTL (Time To Live)**: `64` (1 byte) - Số router tối đa mà gói tin có thể đi qua.
* **Protocol**: `6` (1 byte) - Giá trị chỉ định dữ liệu bên trong là TCP.
* Tên gọi PDU lúc này: **Packet** (Kích thước: 22 + 20 = **42 Byte**)
* Gói tin có dạng:
```
[IP Header: Src 192.168.1.10, Dst 8.8.8.8] [TCP Header...] [ Dữ liệu: "Hi" ]
```

### Bước 4: Thêm MAC Header và FCS Trailer ở tầng Network Access (Layer 2)
Tầng liên kết dữ liệu bọc Packet IP bằng **MAC Header** (14 byte) ở đầu và **FCS Trailer** (4 byte) ở cuối để truyền trong mạng LAN:
* **MAC đích (Destination MAC)**: `00:11:22:33:44:55` (6 byte) - Địa chỉ vật lý của Router cổng ra nhà bạn.
* **MAC nguồn (Source MAC)**: `AA:BB:CC:DD:EE:FF` (6 byte) - Địa chỉ vật lý của card mạng máy bạn.
* **EtherType**: `0x0800` (2 byte) - Chỉ thị dữ liệu lớp trên là IPv4.
* **FCS (Frame Check Sequence)**: (4 byte) - Mã kiểm tra lỗi CRC32 tính toán từ toàn bộ khung dữ liệu. Nếu máy nhận tính ra mã khác, khung tin bị hỏng sẽ bị loại bỏ lập tức.
* Tên gọi PDU lúc này: **Frame** (Kích thước: 42 + 14 + 4 = **60 Byte**)
* Gói tin có dạng:
```
[MAC Header: AA:BB.. -> 00:11..] [IP Header...] [TCP Header...] [ Dữ liệu: "Hi" ] [FCS Trailer (CRC32)]
```

### Bước 5: Chuyển thành xung tín hiệu ở tầng Physical (Layer 1)
Tầng Physical chuyển đổi toàn bộ 60 byte (480 bit nhị phân `0` và `1`) của Frame thành các tín hiệu điện hoặc sóng vô tuyến phát lên dây cáp/không trung.
* Tên gọi PDU lúc này: **Bit**

---

---

# Header là gì?

Header là phần thông tin nằm ở đầu dữ liệu.

Header chứa thông tin điều khiển.

Ví dụ

- IP nguồn
- IP đích
- Port
- MAC
- Sequence Number

---

# Trailer là gì?

Trailer nằm ở cuối dữ liệu.

Không phải tầng nào cũng có Trailer.

Ví dụ:

```
FCS

(Frame Check Sequence)
```

được dùng để kiểm tra lỗi ở tầng Data Link.

---

# Hành trình đóng gói

## Layer 4 - Application

```
Xin chào
```

↓

PDU

```
Data
```

---

## Layer 3 - Transport

Thêm TCP Header.

```
[TCP Header]

Xin chào
```

↓

PDU

```
Segment
```

---

## Layer 2 - Internet

Thêm IP Header.

```
[IP Header]

[TCP Header]

Xin chào
```

↓

PDU

```
Packet
```

---

## Layer 1 - Network Access

Thêm MAC Header.

Thêm Trailer.

```
[MAC]

[IP]

[TCP]

Xin chào

[FCS]
```

↓

PDU

```
Frame
```

---

## Physical

Frame được chuyển thành

```
010101101001001...
```

↓

PDU

```
Bit
```

---

# De-encapsulation

Ở máy nhận

Quá trình diễn ra ngược lại.

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

Mỗi tầng chỉ bóc Header của mình.

---

# Hành trình mở gói

Máy nhận

↓

Physical

```
010101001...
```

↓

Network Access

- Kiểm tra FCS.
- Đọc MAC.
- Bỏ Header.

↓

Internet

- Đọc IP.
- Kiểm tra IP đích.
- Bỏ Header.

↓

Transport

- Đọc Port.
- Đọc Sequence Number.
- Bỏ Header.

↓

Application

```
Xin chào
```

---

# PDU theo từng tầng

| Tầng | PDU |
|------|------|
| Application | Data |
| Transport | Segment (TCP) / Datagram (UDP) |
| Internet | Packet |
| Network Access | Frame |
| Physical | Bit |

Có thể nhớ:

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

---

# Header của từng tầng

## Transport Header

Chứa

- Source Port
- Destination Port
- Sequence Number
- ACK Number

Mục đích

- Đưa đúng ứng dụng.
- Đảm bảo dữ liệu đầy đủ.

---

## Internet Header

Chứa

- Source IP
- Destination IP
- TTL
- Protocol

Mục đích

- Định tuyến.

---

## Network Access Header

Chứa

- Source MAC
- Destination MAC

Trailer

```
FCS
```

Mục đích

- Truyền trong LAN.
- Kiểm tra lỗi.

---

# Vì sao phải thêm nhiều Header?

Mỗi tầng chỉ quan tâm nhiệm vụ của mình.

Ví dụ

Transport

↓

Không cần biết Router nào sẽ đi qua.

Internet

↓

Không cần biết dữ liệu là Video hay Email.

Network Access

↓

Chỉ cần biết MAC đích.

Đây chính là nguyên lý của mô hình phân tầng.

---

# Overhead là gì?

Mỗi khi gửi dữ liệu qua mạng, chúng ta không chỉ gửi nội dung chính (Payload) mà bắt buộc phải gửi kèm các thông tin điều khiển (Header và Trailer). Phần thông tin điều khiển này được gọi là **Overhead** (Chi phí vận chuyển/Hao phí băng thông).

### Phân tích chi tiết ví dụ gửi tin nhắn "Hi" (2 Byte):

| Tầng | Tên trường thông tin điều khiển | Kích thước |
|---|---|---|
| **Layer 4 (Transport)** | TCP Header | 20 Byte |
| **Layer 3 (Internet)** | IP Header | 20 Byte |
| **Layer 2 (Network Access)** | Ethernet Header (MAC) | 14 Byte |
| **Layer 2 (Network Access)** | FCS Trailer (CRC32) | 4 Byte |
| **TỔNG HAO PHÍ (OVERHEAD)** | **Tất cả Header + Trailer** | **58 Byte** |
| **DỮ LIỆU THỰC TẾ (PAYLOAD)** | **Chuỗi "Hi"** | **2 Byte** |
| **TỔNG KÍCH THƯỚC FRAME** | **Overhead + Payload** | **60 Byte** |

### Cách tính phần trăm Overhead:
$$\text{Tỷ lệ Overhead} = \frac{\text{Tổng kích thước Header \& Trailer}}{\text{Tổng kích thước gói tin}} \times 100\%$$

Áp dụng vào ví dụ trên:
$$\text{Tỷ lệ Overhead} = \frac{58\text{ Byte}}{60\text{ Byte}} \times 100\% \approx 96.67\%$$

> [!WARNING]
> Trong trường hợp này, **96.67% băng thông của bạn bị tốn cho việc vận chuyển điều khiển**, và chỉ có vỏn vẹn **3.33%** băng thông dành cho dữ liệu thực tế!

---

# Ví dụ thực tế về hiệu quả truyền tải

Nếu bạn gửi 1000 tin nhắn "Hi" riêng biệt, bạn sẽ phải truyền tổng cộng:
$$1000 \times 60\text{ Byte} = 60.000\text{ Byte}$$
Trong đó hao phí điều khiển chiếm tới **58.000 Byte**!

Nhưng nếu bạn gom toàn bộ thành 1 tin nhắn dài chứa 2000 ký tự (2000 Byte), bạn chỉ cần đóng gói 1 lần:
* Payload: `2000 Byte`
* Overhead: `58 Byte`
* Tổng kích thước gói tin: `2058 Byte`
* Tỷ lệ Overhead lúc này chỉ còn:
$$\frac{58}{2058} \times 100\% \approx 2.82\%$$

**KẾT LUẬN**:
* Gửi nhiều file nhỏ hoặc nhiều tin nhắn ngắn lặp đi lặp lại rất tốn băng thông và làm chậm mạng do Overhead cao.
* Gom dữ liệu lớn hoặc nén file trước khi gửi giúp giảm số lượng gói tin, giảm Overhead và tăng tốc độ truyền tải rõ rệt.

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

Physical

↓

Internet

↓

Physical

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

# Ví dụ thực tế

Bạn mở

```
https://google.com
```

Quá trình

```
Chrome

↓

HTTP Request

↓

TCP Header

↓

IP Header

↓

Ethernet Header

↓

Router

↓

Internet

↓

Google Server
```

Google Server

↓

Bóc Header

↓

Đọc HTTP Request.

---

# Thực hành

## Bài 1

Viết lại thứ tự PDU.

```
Data

↓

?

↓

?

↓

?

↓

?
```

Đáp án

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

## Bài 2

Header nào chứa

- IP
- MAC
- Port

---

## Bài 3

Giải thích

Vì sao gửi 1000 tin nhắn "Hi"

lại tốn băng thông hơn

gửi một đoạn văn dài có cùng số ký tự?

---

# Project thực hành

## Project 1

Quan sát HTTP Request bằng Wireshark.

Xem:

- Ethernet Header
- IP Header
- TCP Header
- HTTP Data

---

## Project 2

Tạo HTTP Server bằng Node.js.

```js
const http = require("http");

http.createServer((req, res) => {
  res.end("Hello");
}).listen(3000);
```

Sau đó dùng Wireshark bắt gói tin.

---

## Project 3

So sánh TCP và UDP.

Quan sát:

- TCP có Sequence Number.
- UDP không có.

---

## Project 4

Phân tích gói Ping.

```bash
ping google.com
```

Quan sát:

- Ethernet
- IP
- ICMP

---

# Hiểu lầm thường gặp

❌ Segment, Packet và Frame là ba dữ liệu khác nhau.

✅ Sai.

Đó là **cùng một dữ liệu**, chỉ khác tên theo từng tầng.

---

❌ Mỗi tầng đọc toàn bộ dữ liệu.

✅ Sai.

Mỗi tầng chỉ đọc **Header của mình**.

---

❌ Chỉ có Header.

✅ Sai.

Một số tầng còn có **Trailer**, ví dụ FCS ở tầng Network Access.

---

# Mẹo ghi nhớ

- Encapsulation = Đóng gói.
- De-encapsulation = Mở gói.
- Header ở đầu.
- Trailer ở cuối.
- Data → Segment → Packet → Frame → Bit.
- Transport → Port.
- Internet → IP.
- Network Access → MAC.

---

# Sau bài này sẽ hiểu

- Encapsulation hoạt động như thế nào.
- De-encapsulation hoạt động như thế nào.
- Ý nghĩa của Header và Trailer.
- PDU ở từng tầng.
- Overhead là gì.
- Hành trình của một gói tin từ máy gửi đến máy nhận.

---

# Bài tiếp theo

## Ethernet và Địa chỉ MAC

Nội dung:

- Ethernet là gì.
- Frame Ethernet.
- Địa chỉ MAC.
- MAC Broadcast.
- ARP hoạt động như thế nào.
- Switch học địa chỉ MAC.