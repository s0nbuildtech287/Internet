# Bài 1 - TCP Chat Server

## Mục tiêu

Sau bài này sẽ hiểu:

- TCP là gì.
- Socket là gì.
- Client và Server giao tiếp như thế nào.
- IP Address.
- Port.
- Quá trình một Client kết nối tới Server.

---

## Kiến thức cần có

- Node.js cơ bản
- JavaScript cơ bản
- Kiến thức Bài 1 của khóa Mạng máy tính:
  - Mạng máy tính
  - Node
  - Đường truyền
  - Giao thức
  - Client - Server

---

# Mô hình

```
          TCP

+-----------+                  +-----------+
|  Client A |----------------->|           |
+-----------+                  |           |
                               |  Server   |
+-----------+                  |           |
|  Client B |----------------->|           |
+-----------+                  +-----------+
```

Server lắng nghe trên một Port.

Nhiều Client có thể kết nối cùng lúc.

---

# Kiến thức sẽ học

## 1. TCP

TCP (Transmission Control Protocol)

Đặc điểm:

- Có kết nối (Connection-oriented)
- Đảm bảo dữ liệu đến nơi
- Không mất thứ tự
- Có cơ chế kiểm tra lỗi

Ví dụ:

```
Xin chào
↓

Packet 1
Packet 2
Packet 3

↓

Server nhận đúng thứ tự

Packet 1
Packet 2
Packet 3
```

---

## 2. Socket

Socket là điểm giao tiếp giữa hai máy.

Có thể hiểu:

```
Client Socket
      │
======TCP======
      │
Server Socket
```

---

## 3. IP Address

Ví dụ:

```
192.168.1.10
```

IP dùng để xác định máy nào đang giao tiếp.

---

## 4. Port

Một máy có thể chạy nhiều dịch vụ.

Ví dụ

```
80      HTTP
443     HTTPS
3306    MySQL
5432    PostgreSQL
3000    NodeJS
```

Một kết nối TCP luôn là

```
IP + Port
```

Ví dụ

```
192.168.1.10:3000
```

---

# Luồng hoạt động

```
Client mở chương trình

↓

Kết nối Server

↓

TCP Handshake

↓

Server chấp nhận kết nối

↓

Client gửi dữ liệu

↓

Server nhận dữ liệu

↓

Server phản hồi

↓

Client nhận phản hồi

↓

Đóng kết nối
```

---

# Thực hành

## Bước 1

Tạo project

```
mkdir tcp-chat

cd tcp-chat

npm init -y
```

---

## Bước 2

Tạo

```
server.js

client.js
```

---

## Bước 3

Viết TCP Server

Yêu cầu:

- Listen Port 3000
- In ra khi có Client kết nối
- Nhận dữ liệu
- Trả về "Hello Client"

---

## Bước 4

Viết TCP Client

Yêu cầu:

- Kết nối localhost:3000
- Gửi

```
Hello Server
```

- In dữ liệu Server trả về

---

# Kiểm tra

Server

```
Client Connected

Hello Server
```

Client

```
Hello Client
```

---

# Mở rộng

Sau khi hoàn thành:

- Nhiều Client kết nối cùng lúc
- Đặt nickname
- Broadcast tới tất cả Client
- Hiển thị thời gian gửi
- Thêm lệnh

```
/list
/help
/exit
```

---

# Liên hệ kiến thức mạng

| Kiến thức mạng | Ứng dụng trong project |
|----------------|------------------------|
| Node | Client và Server |
| Giao thức | TCP |
| Đường truyền | WiFi/LAN |
| Client - Server | Mô hình Chat |
| IP | localhost / 127.0.0.1 |
| Port | 3000 |

---

# Sau bài này sẽ hiểu

- TCP hoạt động như thế nào.
- Socket là gì.
- Một Client kết nối Server ra sao.
- Server lắng nghe bằng Port như thế nào.
- Vì sao HTTP, WebSocket đều được xây dựng trên TCP.

---

# Bài tiếp theo

HTTP Server từ số 0.

Không sử dụng Express.

Mục tiêu:

```
Browser

↓

HTTP Request

↓

Node TCP Server

↓

Parse HTTP

↓

HTTP Response

↓

Browser hiển thị trang web
```