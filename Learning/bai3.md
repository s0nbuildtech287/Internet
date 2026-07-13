````md
# Bài 3 - Topology (Cấu trúc liên kết mạng)

## Mục tiêu

Sau bài này sẽ hiểu:

- Topology là gì.
- Phân biệt Physical Topology và Logical Topology.
- Hiểu 4 topology phổ biến:
  - Star
  - Bus
  - Ring
  - Mesh
- Biết ưu điểm, nhược điểm của từng topology.
- Hiểu vì sao mạng LAN hiện đại thường dùng Star và Internet có dạng Partial Mesh.

---

## Kiến thức cần có

- Đã học Bài 1 (Khái niệm mạng)
- Đã học Bài 2 (PAN, LAN, MAN, WAN)

---

# Topology là gì?

Topology là cách các thiết bị (Node) được kết nối với nhau trong một mạng.

Nói đơn giản:

```
Node kết nối với nhau như thế nào?
```

Topology quyết định:

- Tốc độ mạng
- Độ ổn định
- Khả năng mở rộng
- Chi phí triển khai
- Khả năng dự phòng

---

# Có 2 loại Topology

## 1. Physical Topology

Là cách đi dây ngoài thực tế.

Ví dụ:

```
Laptop

      │

Switch

      │

Server
```

Đó là hình dạng thật của mạng.

---

## 2. Logical Topology

Là cách dữ liệu thực sự truyền đi.

Ví dụ:

```
Laptop

↓

Switch

↓

Server
```

Có những mạng:

- Đi dây hình sao
- Nhưng dữ liệu chạy theo vòng

Đó là Physical Star nhưng Logical Ring.

---

# 1. Star Topology

Hình sao.

Mọi thiết bị đều kết nối về một thiết bị trung tâm.

Thường là:

- Switch
- Router

```
             PC1
              │
PC2 ───── Switch ───── PC3
              │
            Laptop
```

---

## Cách hoạt động

```
PC1 gửi dữ liệu

↓

Switch

↓

PC3
```

Mọi dữ liệu đều đi qua Switch.

---

## Ưu điểm

- Dễ quản lý
- Dễ mở rộng
- Một dây hỏng không ảnh hưởng thiết bị khác
- Tốc độ cao

---

## Nhược điểm

Nếu Switch hỏng

↓

Toàn bộ mạng ngừng hoạt động.

---

## Ví dụ

- WiFi gia đình
- Văn phòng
- Công ty
- Trường học

---

# 2. Bus Topology

Mọi thiết bị cùng kết nối vào một đường cáp chính.

```
PC1

 │

PC2

 │

PC3

 │

PC4

====================
     Cable
====================
```

---

## Cách hoạt động

Một máy gửi dữ liệu

↓

Tất cả máy đều nhận

↓

Máy đúng địa chỉ sẽ xử lý.

---

## Ưu điểm

- Ít dây
- Giá rẻ

---

## Nhược điểm

Nếu cáp chính đứt

↓

Toàn bộ mạng dừng hoạt động.

Nhiều máy gửi cùng lúc dễ xảy ra Collision.

---

## Hiện nay

Hầu như không còn sử dụng.

---

# 3. Ring Topology

Các thiết bị tạo thành một vòng tròn.

```
        PC1

     /       \

PC4           PC2

     \       /

        PC3
```

---

## Cách hoạt động

Dữ liệu đi theo một chiều.

```
PC1

↓

PC2

↓

PC3

↓

PC4

↓

PC1
```

---

## Ưu điểm

- Ít xảy ra va chạm
- Dữ liệu truyền có thứ tự

---

## Nhược điểm

Một thiết bị hỏng

↓

Có thể làm đứt cả vòng.

Khó mở rộng.

---

## Ví dụ

- Token Ring (IBM)
- Một số mạng công nghiệp

---

# 4. Mesh Topology

Mỗi thiết bị kết nối với nhiều thiết bị khác.

```
      A ------- B
      |\       /|
      | \     / |
      |  \   /  |
      |   \ /   |
      |   / \   |
      |  /   \  |
      | /     \ |
      |/       \|
      C ------- D
```

---

## Cách hoạt động

Nếu một đường hỏng

↓

Dữ liệu đi đường khác.

---

## Ưu điểm

- Rất ổn định
- Có nhiều đường dự phòng
- Khó bị gián đoạn

---

## Nhược điểm

- Tốn rất nhiều dây
- Chi phí cao
- Khó triển khai

---

## Ví dụ

- Internet
- Data Center
- Hệ thống Cloud

---

# Hybrid Topology

Thực tế không có mạng nào chỉ dùng một topology.

Ví dụ:

```
             Core Switch

          /      |      \

      Switch  Switch  Switch

      / | \    / | \    / | \

    PC PC PC PC PC PC PC PC PC
```

Đây là Tree Topology.

Mỗi tầng là một Star.

---

# So sánh

| Topology | Ưu điểm | Nhược điểm | Phổ biến |
|-----------|----------|------------|----------|
| Star | Dễ mở rộng | Switch hỏng là sập | ⭐⭐⭐⭐⭐ |
| Bus | Rẻ | Đứt cáp là sập | ⭐ |
| Ring | Ít Collision | Đứt vòng | ⭐ |
| Mesh | Bền nhất | Rất đắt | ⭐⭐⭐ |

---

# So sánh trực quan

```
STAR

      PC

      |

Switch

 / | \

PC PC Laptop
```

```
BUS

PC

 |

PC

 |

PC

================
```

```
RING

PC

/     \

PC     PC

\     /

PC
```

```
MESH

A------B

|\    /|

| \  / |

|  \/  |

|  /\  |

| /  \ |

|/    \|

C------D
```

---

# Thực hành

## Bài 1

Quan sát mạng nhà bạn.

```
Laptop

↓

WiFi

↓

Router

↓

Internet
```

Topology gì?

Đáp án:

```
Star
```

---

## Bài 2

Nếu Switch hỏng thì sao?

Đáp án:

```
Toàn bộ mạng Star ngừng hoạt động.
```

---

## Bài 3

Topology nào bền nhất?

Đáp án:

```
Mesh
```

---

## Bài 4

Topology nào tiết kiệm dây nhất?

Đáp án:

```
Bus
```

---

# Project thực hành

## Mục tiêu

Hiểu topology bằng cách mô phỏng bằng code.

---

## Project 1

Mô phỏng Star Topology.

```
Client A

↓

Server

↓

Client B
```

Code:

- TCP Server
- Nhiều TCP Client

Kiến thức:

- Star
- Client - Server
- Socket

---

## Project 2

Mô phỏng Ring.

```
A

↓

B

↓

C

↓

D

↓

A
```

Dữ liệu truyền lần lượt qua từng Node.

---

## Project 3

Mô phỏng Mesh.

```
A

↓

B

↓

C

↓

D
```

Nếu B lỗi

↓

A gửi sang C.

---

## Project 4

Mô phỏng Tree.

```
Core

↓

Switch

↓

Client
```

---

# Sau bài này sẽ hiểu

- Topology là gì.
- Physical và Logical Topology.
- Star hoạt động như thế nào.
- Bus hoạt động như thế nào.
- Ring hoạt động như thế nào.
- Mesh hoạt động như thế nào.
- Vì sao mạng LAN dùng Star.
- Vì sao Internet gần giống Mesh.

---

# Bài tiếp theo

Thiết bị mạng

- NIC
- Hub
- Switch
- Router
- Modem
- Access Point

Sau bài này sẽ bắt đầu code mô phỏng hoạt động của các thiết bị mạng bằng Node.js.
````
