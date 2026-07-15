# Bài 10: Định tuyến (Routing), Gateway & NAT

## 1. Routing (Định tuyến) là gì?

Routing là quá trình router chọn đường đi tốt nhất để đưa gói tin từ mạng nguồn đến mạng đích.

Mỗi router có một **Routing Table (bảng định tuyến)** để biết:

- Mạng đích ở đâu
- Phải gửi sang router nào tiếp theo (Next Hop)

Ví dụ:

┌────────────────────┬──────────────────┐
│ Mạng đích          │ Next Hop         │
├────────────────────┼──────────────────┤
│ 192.168.1.0/24     │ Kết nối trực tiếp │
│ 10.0.0.0/8         │ Router A          │
│ 0.0.0.0/0          │ Router ISP        │
└────────────────────┴──────────────────┘

**0.0.0.0/0** gọi là **Default Route** (đường mặc định).

Nếu không biết gửi đi đâu thì gửi theo tuyến này.

---

## 2. Router chuyển tiếp gói tin như thế nào?

Khi router nhận một Packet:

1. Đọc IP đích.
2. Tra Routing Table.
3. Chọn tuyến phù hợp nhất (Longest Prefix Match).
4. Gửi sang Next Hop.
5. Router tiếp theo làm tương tự.

Ví dụ:

Máy bạn
   ↓
Router nhà
   ↓
Router ISP
   ↓
Router khác
   ↓
Server

Không router nào cần biết toàn bộ Internet, chỉ cần biết bước tiếp theo.

---

## 3. Default Gateway là gì?

Default Gateway là địa chỉ IP của Router trong mạng LAN.

Ví dụ:

Máy bạn:

192.168.1.10

Gateway:

192.168.1.1

Nếu gửi tới:

192.168.1.20

→ cùng mạng

→ gửi trực tiếp.

Nếu gửi tới:

8.8.8.8

→ khác mạng

→ gửi cho Gateway.

Gateway sẽ tiếp tục định tuyến.

Thường Gateway là:

- 192.168.1.1
- 192.168.0.1
- 10.0.0.1

Có thể xem bằng:

Windows
