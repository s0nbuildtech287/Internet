import http.server
import socket
import threading
import json
import time
import urllib.request
import os
import subprocess
import re
import uuid

PORT = 8080
DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pages")

# Global state for the TCP socket simulation
tcp_server = None
tcp_server_thread = None
tcp_server_running = False
tcp_server_port = None
tcp_clients = {}  # client_address -> socket
tcp_client_logs = []
client_socket_instance = None  # The client socket we control via web page
client_socket_thread = None

# Global state for Traceroute simulation
traceroute_running = False
traceroute_hops = []
traceroute_target = ""
traceroute_process = None
traceroute_thread = None

lock = threading.Lock()

def add_log(event_type, message, details=""):
    """Add a structured log for the TCP Playground"""
    with lock:
        tcp_client_logs.append({
            "timestamp": time.strftime("%H:%M:%S"),
            "type": event_type,  # 'info', 'handshake', 'data_sent', 'data_recv', 'error', 'success'
            "message": message,
            "details": details
        })

class NetworkUtility:
    @staticmethod
    def get_local_ips():
        """Get list of active local network IPs and interface names"""
        ips = []
        try:
            # Fallback method: Connect to a dummy socket to find active interface IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            primary_ip = s.getsockname()[0]
            s.close()
            ips.append({"name": "Primary Interface", "ip": primary_ip})
        except Exception:
            primary_ip = "127.0.0.1"

        try:
            # Get host name
            hostname = socket.gethostname()
            # Resolve all IPs associated with hostname
            addr_infos = socket.getaddrinfo(hostname, None)
            for info in addr_infos:
                ip = info[4][0]
                # Filter out IPv6 and duplicates
                if ":" not in ip and ip != "127.0.0.1":
                    exists = any(item["ip"] == ip for item in ips)
                    if not exists:
                        ips.append({"name": f"Adapter ({hostname})", "ip": ip})
        except Exception as e:
            pass
            
        if not ips:
            ips.append({"name": "Loopback", "ip": "127.0.0.1"})
        return ips

    @staticmethod
    def get_mac_address():
        """Get host MAC address formatted as XX:XX:XX:XX:XX:XX"""
        try:
            node = uuid.getnode()
            mac = ':'.join(['{:02x}'.format((node >> ele) & 0xff) for ele in range(0, 8*6, 8)][::-1])
            return mac.upper()
        except Exception:
            return "00:00:00:00:00:00"

    @staticmethod
    def get_default_gateway():
        """Get actual active default gateway IP using OS ipconfig or route command"""
        try:
            if os.name == 'nt':
                out = subprocess.check_output("ipconfig", shell=True, text=True, errors='ignore')
                gateways = re.findall(r'Default Gateway[\s\.]*:\s*([0-9\.]+)', out)
                for gw in gateways:
                    if gw.strip() and gw != "0.0.0.0":
                        return gw
            else:
                out = subprocess.check_output("route -n", shell=True, text=True, errors='ignore')
                for line in out.split('\n'):
                    if line.startswith("0.0.0.0"):
                        parts = line.split()
                        if len(parts) > 1:
                            return parts[1]
        except Exception:
            pass
        return "192.168.1.1" # default fallback

    @staticmethod
    def get_local_ipv6():
        """Get local IPv6 address"""
        try:
            hostname = socket.gethostname()
            addr_infos = socket.getaddrinfo(hostname, None, socket.AF_INET6)
            for info in addr_infos:
                ip = info[4][0]
                if ip != "::1" and not ip.startswith("fe80"):
                    return ip
        except Exception:
            pass
        return "Không hoạt động / Không hỗ trợ"

    @staticmethod
    def get_public_ip_info():
        """Fetch public IP and Geo-IP details using a free API"""
        url = "http://ip-api.com/json/"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=3) as response:
                data = json.loads(response.read().decode('utf-8'))
                if data.get("status") == "success":
                    return {
                        "ip": data.get("query"),
                        "isp": data.get("isp"),
                        "city": data.get("city"),
                        "country": data.get("country"),
                        "org": data.get("org")
                    }
        except Exception:
            # Fallback to ipify if ip-api fails
            try:
                with urllib.request.urlopen("https://api.ipify.org?format=json", timeout=2) as response:
                    ip_data = json.loads(response.read().decode('utf-8'))
                    return {
                        "ip": ip_data.get("ip"),
                        "isp": "Unknown ISP",
                        "city": "Unknown",
                        "country": "Unknown",
                        "org": "Unknown"
                    }
            except Exception:
                pass
        return {
            "ip": "No Internet Connection",
            "isp": "N/A",
            "city": "N/A",
            "country": "N/A",
            "org": "N/A"
        }

    @staticmethod
    def tcp_ping(host, port=80, timeout=1.5):
        """Measure RTT by establishing a standard TCP connection"""
        start = time.perf_counter()
        try:
            # Resolve DNS
            ip = socket.gethostbyname(host)
            # Try to connect
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(timeout)
            s.connect((ip, port))
            s.close()
            rtt = (time.perf_counter() - start) * 1000
            return {"status": "Online", "ip": ip, "rtt": round(rtt, 1)}
        except socket.timeout:
            return {"status": "Timeout", "ip": "Unknown", "rtt": -1}
        except Exception as e:
            return {"status": "Offline", "ip": "Unknown", "rtt": -1}

    @staticmethod
    def scan_subnet(base_ip):
        """Scan a base IP subnet (e.g. 192.168.1.0/24) for active hosts"""
        # Split base IP
        parts = base_ip.split('.')
        if len(parts) != 4:
            return []
        subnet_prefix = f"{parts[0]}.{parts[1]}.{parts[2]}."
        
        active_devices = []
        threads = []
        
        def check_host(ip):
            # Fast ping using OS subprocess (1 ping, short timeout)
            # Windows: ping -n 1 -w 150 ip
            # Linux/Mac: ping -c 1 -W 1 ip
            is_win = os.name == 'nt'
            cmd = ["ping", "-n", "1", "-w", "150", ip] if is_win else ["ping", "-c", "1", "-W", "1", ip]
            
            try:
                # We suppress output
                res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                if res.returncode == 0:
                    # Device responded to ping. Let's try to get hostname or service
                    name = "Unknown Device"
                    try:
                        name = socket.gethostbyaddr(ip)[0]
                    except Exception:
                        pass
                    active_devices.append({"ip": ip, "status": "Active", "name": name})
                    return
            except Exception:
                pass
                
            # If ping failed, try common ports (TCP connect) to see if socket is open
            for port in [80, 135, 443, 445]:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(0.08)
                    s.connect((ip, port))
                    s.close()
                    active_devices.append({"ip": ip, "status": "Active", "name": f"Device (Port {port} Open)"})
                    break
                except Exception:
                    pass

        # Scan IPs 1 to 254 in parallel threads
        for i in range(1, 255):
            ip = f"{subnet_prefix}{i}"
            t = threading.Thread(target=check_host, args=(ip,))
            threads.append(t)
            t.start()
            
        for t in threads:
            t.join()
            
        return sorted(active_devices, key=lambda x: [int(num) for num in x["ip"].split('.')])

    @staticmethod
    def scan_wifi_networks():
        """Scan surrounding WiFi network SSIDs using Windows netsh command"""
        if os.name != 'nt':
            return {"status": "error", "message": "Tính năng này chỉ hỗ trợ trên Windows"}
        try:
            # Trigger a new wireless scan to update the Windows WLAN cache
            subprocess.run(["netsh", "wlan", "scan"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            time.sleep(1.2) # Allow card a brief moment to scan
            
            # Run netsh wlan show networks mode=bssid
            result = subprocess.run(
                ["netsh", "wlan", "show", "networks", "mode=bssid"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                errors='ignore'
            )
            output = result.stdout
            
            networks = []
            current_net = {}
            
            # Parse netsh output lines
            for line in output.split('\n'):
                line = line.strip()
                if line.startswith("SSID"):
                    if current_net:
                        networks.append(current_net)
                    parts = line.split(':', 1)
                    ssid_name = parts[1].strip() if len(parts) > 1 else "Unknown"
                    current_net = {"ssid": ssid_name, "bssids": []}
                elif current_net:
                    if line.startswith("Authentication"):
                        current_net["auth"] = line.split(':', 1)[1].strip()
                    elif line.startswith("BSSID"):
                        bssid = line.split(':', 1)[1].strip()
                        current_net["bssids"].append({"bssid": bssid})
                    elif line.startswith("Signal") and current_net["bssids"]:
                        current_net["bssids"][-1]["signal"] = line.split(':', 1)[1].strip()
                    elif line.startswith("Channel") and current_net["bssids"]:
                        current_net["bssids"][-1]["channel"] = line.split(':', 1)[1].strip()
                        
            if current_net:
                networks.append(current_net)
                
            formatted_nets = []
            for net in networks:
                ssid = net.get("ssid", "").strip()
                if not ssid:
                    ssid = "Hidden SSID"
                auth = net.get("auth", "Unknown")
                for b in net.get("bssids", []):
                    formatted_nets.append({
                        "ssid": ssid,
                        "bssid": b.get("bssid"),
                        "signal": b.get("signal", "0%"),
                        "channel": b.get("channel", "Unknown"),
                        "auth": auth
                     })
            return {"status": "success", "networks": sorted(formatted_nets, key=lambda x: int(x["signal"].replace('%','')) if '%' in x["signal"] else 0, reverse=True)}
        except Exception as e:
            return {"status": "error", "message": str(e)}



# --- TCP Playground Backend Server ---
def run_tcp_server(port):
    global tcp_server, tcp_server_running, tcp_clients
    try:
        tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcp_server.bind(('0.0.0.0', port))
        tcp_server.listen(5)
        tcp_server_running = True
        add_log("success", f"TCP Server khởi động thành công", f"Lắng nghe cổng {port} trên tất cả card mạng (0.0.0.0)")
        
        while tcp_server_running:
            try:
                tcp_server.settimeout(1.0)
                client_sock, client_addr = tcp_server.accept()
                client_ip, client_port = client_addr
                add_log("handshake", f"Server nhận yêu cầu kết nối từ {client_ip}:{client_port}", 
                        "Nhận gói tin SYN. Đang thực hiện gửi SYN-ACK và nhận ACK...")
                
                # Keep track of connection
                tcp_clients[client_addr] = client_sock
                
                # Start handler thread
                t = threading.Thread(target=handle_tcp_client, args=(client_sock, client_addr))
                t.daemon = True
                t.start()
            except socket.timeout:
                continue
            except Exception as e:
                if tcp_server_running:
                    add_log("error", "Lỗi chấp nhận kết nối tại Server", str(e))
                break
    except Exception as e:
        add_log("error", f"Không thể mở Server tại cổng {port}", str(e))
        tcp_server_running = False

def handle_tcp_client(client_sock, client_addr):
    global tcp_clients
    client_ip, client_port = client_addr
    add_log("success", f"Kết nối TCP thiết lập hoàn tất: {client_ip}:{client_port}", "Trạng thái Socket: ESTABLISHED")
    
    while tcp_server_running:
        try:
            client_sock.settimeout(1.0)
            data = client_sock.recv(1024)
            if not data:
                # Connection closed by client
                add_log("info", f"Client {client_ip}:{client_port} đã đóng kết nối (FIN)", "Nhận EOF từ socket")
                break
            
            msg = data.decode('utf-8', errors='ignore')
            add_log("data_recv", f"Server nhận dữ liệu từ {client_ip}:{client_port}", f"Nội dung: \"{msg}\"")
            
            # Send Auto-reply like in the lesson
            reply = f"Hello Client! Server nhận được: {msg}"
            client_sock.sendall(reply.encode('utf-8'))
            add_log("data_sent", f"Server phản hồi lại cho {client_ip}:{client_port}", f"Nội dung: \"{reply}\"")
            
        except socket.timeout:
            continue
        except Exception as e:
            add_log("info", f"Ngắt kết nối với {client_ip}:{client_port}", str(e))
            break
            
    try:
        client_sock.close()
    except:
        pass
    if client_addr in tcp_clients:
        del tcp_clients[client_addr]


def run_tcp_client_connector(host, port):
    global client_socket_instance
    try:
        add_log("handshake", f"Client đang khởi tạo Socket...", "socket(AF_INET, SOCK_STREAM)")
        client_socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket_instance.settimeout(5.0)
        
        add_log("handshake", f"Client bắt đầu kết nối tới {host}:{port}", "Gửi gói tin SYN để bắt tay 3 bước...")
        client_socket_instance.connect((host, port))
        add_log("success", f"Client kết nối THÀNH CÔNG tới {host}:{port}", "Nhận SYN-ACK và gửi ACK. Trạng thái: ESTABLISHED")
        
        while client_socket_instance:
            try:
                # Wait for server messages
                client_socket_instance.settimeout(1.0)
                data = client_socket_instance.recv(1024)
                if not data:
                    add_log("info", "Client nhận tín hiệu đóng kết nối từ Server", "Nhận 0 bytes (EOF)")
                    break
                msg = data.decode('utf-8', errors='ignore')
                add_log("data_recv", "Client nhận dữ liệu phản hồi từ Server", f"Nội dung: \"{msg}\"")
            except socket.timeout:
                continue
            except Exception as e:
                add_log("info", "Luồng nhận dữ liệu Client đã dừng", str(e))
                break
    except Exception as e:
        add_log("error", f"Client kết nối THẤT BẠI tới {host}:{port}", str(e))
    finally:
        close_client_socket()

def close_client_socket():
    global client_socket_instance
    if client_socket_instance:
        try:
            add_log("info", "Client đóng Socket kết nối", "Gửi gói tin FIN để đóng phiên")
            client_socket_instance.close()
        except:
            pass
        client_socket_instance = None


def run_traceroute_thread(target):
    global traceroute_hops, traceroute_running, traceroute_process, traceroute_target
    traceroute_hops = []
    traceroute_target = target
    traceroute_running = True
    
    is_win = os.name == 'nt'
    # Windows: tracert -d -h 15 target (max 15 hops, no DNS resolution for speed)
    # Unix: traceroute -n -m 15 target
    cmd = ["tracert", "-d", "-h", "15", target] if is_win else ["traceroute", "-n", "-m", "15", target]
    
    try:
        # Use Popen to read line-by-line in real-time
        traceroute_process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            errors='ignore'
        )
        
        for line in iter(traceroute_process.stdout.readline, ''):
            if not traceroute_running:
                break
            line_str = line.strip()
            if not line_str:
                continue
                
            # Parse hop information
            # Match number at start (hop index)
            match = re.match(r'^\s*(\d+)\s+(.+)$', line_str)
            if match:
                hop_num = int(match.group(1))
                hop_data = match.group(2)
                
                # Check for IP address
                ip_match = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', hop_data)
                ip = ip_match.group(1) if ip_match else "Request timed out."
                
                # Extract latencies (e.g. 5 ms)
                rtts = re.findall(r'(\d+)\s*ms', hop_data)
                avg_rtt = "--"
                if rtts:
                    avg_rtt = f"{round(sum(int(r) for r in rtts) / len(rtts))} ms"
                elif "*" in hop_data:
                    avg_rtt = "*"
                    
                traceroute_hops.append({
                    "hop": hop_num,
                    "ip": ip,
                    "rtt": avg_rtt,
                    "raw": line_str
                })
        
        traceroute_process.stdout.close()
        traceroute_process.wait()
    except Exception as e:
        traceroute_hops.append({
            "hop": "ERR",
            "ip": "Error occurred",
            "rtt": "--",
            "raw": str(e)
        })
    finally:
        traceroute_running = False
        traceroute_process = None


# --- Web Server Handler ---
class APIServerHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        # Prevent caching for all files and APIs to ensure hot reloads work instantly
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def do_GET(self):
        # Handle Web Page root redirects
        if self.path == "/" or self.path == "":
            self.path = "/index.html"
            return super().do_GET()
            
        # REST APIs
        if self.path == "/api/network":
            self.send_json_response(self.handle_api_network())
        elif self.path == "/api/ping-all":
            self.send_json_response(self.handle_api_ping_all())
        elif self.path.startswith("/api/local-scan"):
            self.send_json_response(self.handle_api_local_scan())
        elif self.path == "/api/wifi-scan":
            self.send_json_response(self.handle_api_wifi_scan())
        elif self.path == "/api/socket/status":
            self.send_json_response(self.handle_api_socket_status())
        elif self.path == "/api/socket/logs":
            self.send_json_response(self.handle_api_socket_logs())
        elif self.path == "/api/traceroute/status":
            self.send_json_response(self.handle_api_traceroute_status())
        else:
            # Fallback to serving static files from directory
            super().do_GET()

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length) if content_length > 0 else b""
        
        try:
            params = json.loads(post_data.decode('utf-8')) if post_data else {}
        except Exception:
            params = {}

        if self.path == "/api/socket/start":
            self.send_json_response(self.handle_api_socket_start(params))
        elif self.path == "/api/socket/stop":
            self.send_json_response(self.handle_api_socket_stop())
        elif self.path == "/api/socket/connect-client":
            self.send_json_response(self.handle_api_socket_connect_client(params))
        elif self.path == "/api/socket/send-client-message":
            self.send_json_response(self.handle_api_socket_send_client_message(params))
        elif self.path == "/api/socket/disconnect-client":
            self.send_json_response(self.handle_api_socket_disconnect_client())
        elif self.path == "/api/socket/clear-logs":
            self.send_json_response(self.handle_api_socket_clear_logs())
        elif self.path == "/api/dns-lookup":
            self.send_json_response(self.handle_api_dns_lookup(params))
        elif self.path == "/api/traceroute/start":
            self.send_json_response(self.handle_api_traceroute_start(params))
        elif self.path == "/api/traceroute/stop":
            self.send_json_response(self.handle_api_traceroute_stop())
        else:
            self.send_error(404, "API endpoint not found")

    def send_json_response(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    # API Handlers
    def handle_api_network(self):
        local_ips = NetworkUtility.get_local_ips()
        public_info = NetworkUtility.get_public_ip_info()
        return {
            "local_ips": local_ips,
            "public_info": public_info,
            "hostname": socket.gethostname(),
            "mac_address": NetworkUtility.get_mac_address(),
            "default_gateway": NetworkUtility.get_default_gateway(),
            "local_ipv6": NetworkUtility.get_local_ipv6()
        }

    def handle_api_ping_all(self):
        servers = [
            {"name": "Google DNS", "host": "8.8.8.8", "port": 53},
            {"name": "Cloudflare DNS", "host": "1.1.1.1", "port": 53},
            {"name": "Google Vietnam", "host": "google.com.vn", "port": 80},
            {"name": "GitHub (USA)", "host": "github.com", "port": 443},
            {"name": "Facebook", "host": "facebook.com", "port": 443},
            {"name": "YouTube", "host": "youtube.com", "port": 443},
            {"name": "Wikipedia", "host": "wikipedia.org", "port": 443}
        ]
        
        results = []
        threads = []

        def ping_worker(srv):
            ping_res = NetworkUtility.tcp_ping(srv["host"], srv["port"])
            results.append({
                "name": srv["name"],
                "host": srv["host"],
                "port": srv["port"],
                "ip": ping_res["ip"],
                "rtt": ping_res["rtt"],
                "status": ping_res["status"]
            })

        for srv in servers:
            t = threading.Thread(target=ping_worker, args=(srv,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        return results

    def handle_api_local_scan(self):
        # Find active local IP to scan
        ips = NetworkUtility.get_local_ips()
        base_ip = "192.168.1.1" # default fallback
        
        # Look for a 192.168.X.X or 10.X.X.X address
        for ip_info in ips:
            ip = ip_info["ip"]
            if ip != "127.0.0.1":
                base_ip = ip
                break
                
        devices = NetworkUtility.scan_subnet(base_ip)
        return {
            "scanned_subnet": re.sub(r'\.\d+$', '.0/24', base_ip),
            "devices": devices
        }

    def handle_api_wifi_scan(self):
        return NetworkUtility.scan_wifi_networks()


    def handle_api_socket_status(self):
        global tcp_server_running, tcp_server_port, tcp_clients, client_socket_instance
        return {
            "server_running": tcp_server_running,
            "server_port": tcp_server_port,
            "connected_clients": [f"{addr[0]}:{addr[1]}" for addr in tcp_clients.keys()],
            "client_connected": client_socket_instance is not None
        }

    def handle_api_socket_logs(self):
        global tcp_client_logs
        with lock:
            logs = list(tcp_client_logs)
        return logs

    def handle_api_socket_start(self, params):
        global tcp_server_thread, tcp_server_running, tcp_server_port
        port = int(params.get("port", 3000))
        
        if tcp_server_running:
            return {"status": "error", "message": f"Server đang chạy trên cổng {tcp_server_port}"}
            
        tcp_server_port = port
        tcp_server_thread = threading.Thread(target=run_tcp_server, args=(port,))
        tcp_server_thread.daemon = True
        tcp_server_thread.start()
        
        return {"status": "success", "message": f"Yêu cầu khởi chạy Server trên cổng {port} đã được gửi"}

    def handle_api_socket_stop(self):
        global tcp_server, tcp_server_running, tcp_clients
        if not tcp_server_running:
            return {"status": "error", "message": "Server chưa chạy"}
            
        tcp_server_running = False
        
        # Close all client connections
        for client_sock in list(tcp_clients.values()):
            try:
                client_sock.close()
            except:
                pass
        tcp_clients.clear()
        
        # Close server socket
        if tcp_server:
            try:
                tcp_server.close()
            except:
                pass
        
        add_log("info", "TCP Server đã được dừng bởi người dùng", "Giải phóng cổng kết nối")
        return {"status": "success", "message": "Server đã dừng"}

    def handle_api_socket_connect_client(self, params):
        global client_socket_instance, client_socket_thread
        host = params.get("host", "127.0.0.1")
        port = int(params.get("port", 3000))
        
        if client_socket_instance:
            return {"status": "error", "message": "Client đã kết nối rồi"}
            
        client_socket_thread = threading.Thread(target=run_tcp_client_connector, args=(host, port))
        client_socket_thread.daemon = True
        client_socket_thread.start()
        
        return {"status": "success", "message": "Đang thiết lập kết nối Client..."}

    def handle_api_socket_send_client_message(self, params):
        global client_socket_instance
        message = params.get("message", "Hello Server")
        
        if not client_socket_instance:
            return {"status": "error", "message": "Client chưa kết nối tới server"}
            
        try:
            client_socket_instance.sendall(message.encode('utf-8'))
            add_log("data_sent", "Client gửi dữ liệu đi", f"Nội dung: \"{message}\"")
            return {"status": "success", "message": "Đã gửi tin nhắn"}
        except Exception as e:
            add_log("error", "Lỗi gửi tin nhắn từ Client", str(e))
            return {"status": "error", "message": f"Không thể gửi dữ liệu: {e}"}

    def handle_api_socket_disconnect_client(self):
        global client_socket_instance
        if not client_socket_instance:
            return {"status": "error", "message": "Client chưa kết nối"}
            
        close_client_socket()
        return {"status": "success", "message": "Đang đóng kết nối Client..."}

    def handle_api_socket_clear_logs(self):
        global tcp_client_logs
        with lock:
            tcp_client_logs.clear()
        return {"status": "success", "message": "Đã xóa lịch sử log"}

    def handle_api_dns_lookup(self, params):
        domain = params.get("domain", "").strip()
        if not domain:
            return {"status": "error", "message": "Vui lòng nhập tên miền"}
        try:
            ipv4_list = []
            ipv6_list = []
            try:
                addr_infos = socket.getaddrinfo(domain, None, socket.AF_INET)
                ipv4_list = list(set([info[4][0] for info in addr_infos]))
            except Exception:
                pass
            try:
                addr_infos = socket.getaddrinfo(domain, None, socket.AF_INET6)
                ipv6_list = list(set([info[4][0] for info in addr_infos]))
            except Exception:
                pass
                
            if not ipv4_list and not ipv6_list:
                return {"status": "error", "message": f"Không thể phân giải tên miền: {domain}"}
                
            return {
                "status": "success",
                "domain": domain,
                "ipv4": ipv4_list,
                "ipv6": ipv6_list
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def handle_api_traceroute_start(self, params):
        global traceroute_running, traceroute_thread, traceroute_target
        target = params.get("target", "").strip()
        if not target:
            return {"status": "error", "message": "Vui lòng nhập địa chỉ IP hoặc tên miền"}
            
        # Clean target name (simple security sanitization)
        target = re.sub(r'[^a-zA-Z0-9\.\-]', '', target)
        if not target:
            return {"status": "error", "message": "Địa chỉ không hợp lệ"}
            
        if traceroute_running:
            return {"status": "error", "message": "Tiến trình Traceroute khác đang chạy"}
            
        traceroute_thread = threading.Thread(target=run_traceroute_thread, args=(target,))
        traceroute_thread.daemon = True
        traceroute_thread.start()
        
        return {"status": "success", "message": f"Bắt đầu traceroute tới {target}..."}

    def handle_api_traceroute_status(self):
        global traceroute_running, traceroute_hops, traceroute_target
        return {
            "running": traceroute_running,
            "target": traceroute_target,
            "hops": list(traceroute_hops)
        }

    def handle_api_traceroute_stop(self):
        global traceroute_running, traceroute_process
        if not traceroute_running:
            return {"status": "error", "message": "Không có tiến trình traceroute nào đang chạy"}
            
        traceroute_running = False
        if traceroute_process:
            try:
                traceroute_process.terminate()
            except:
                pass
        return {"status": "success", "message": "Đã dừng tiến trình traceroute"}


if __name__ == "__main__":
    # Create the pages directory if it doesn't exist
    os.makedirs(DIRECTORY, exist_ok=True)
    
    server_address = ('', PORT)
    httpd = http.server.HTTPServer(server_address, APIServerHandler)
    print(f"===========================================================")
    print(f"  NETWORKING LAB WEB SERVER IS RUNNING")
    print(f"  Access the dashboard: http://localhost:{PORT}")
    print(f"  Serving files from: {DIRECTORY}")
    print(f"===========================================================")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping web server...")
        # Clean up
        if tcp_server_running:
            tcp_server_running = False
            try: tcp_server.close() 
            except: pass
        httpd.server_close()
        print("Web server stopped.")
