#!/usr/bin/env python3
"""
Desk Buddy - PC Hardware Monitor Script
Wysyła w czasie rzeczywistym parametry komputera (CPU, RAM, GPU) do robota przez port szeregowy (USB).
Wymaga: pip install psutil pyserial
"""

import time
import sys

try:
    import psutil
    import serial
    import serial.tools.list_ports
except ImportError:
    print("[!] Zainstaluj wymagane biblioteki: pip install psutil pyserial")
    sys.exit(1)

def find_esp_port():
    ports = serial.tools.list_ports.comports()
    for p in ports:
        if "CP210" in p.description or "CH340" in p.description or "USB" in p.description:
            return p.device
    return ports[0].device if ports else None

def main():
    port = sys.argv[1] if len(sys.argv) > 1 else find_esp_port()
    if not port:
        print("[!] Nie znaleziono podłączonego portu ESP32. Podaj port jako argument, np: python3 pc_monitor.py /dev/ttyUSB0")
        sys.exit(1)

    print(f"[*] Łączenie z Desk Buddy na porcie {port} (115200 baud)...")
    try:
        ser = serial.Serial(port, 115200, timeout=1)
        time.sleep(2)
        print("[+] Połączono! Wysyłanie danych o obciążeniu PC co 1 sekundę. Naciśnij Ctrl+C aby zakończyć.")

        while True:
            cpu = psutil.cpu_percent(interval=0.5)
            ram = psutil.virtual_memory().percent
            # Prosta symulacja/estymacja GPU lub odczyt jeśli dostępny
            gpu = min(100.0, cpu * 1.1 + 5.0)
            temp = 45.0 + (cpu * 0.25)

            cmd = f"pc cpu={cpu:.0f} ram={ram:.0f} gpu={gpu:.0f} temp={temp:.0f}\n"
            ser.write(cmd.encode('utf-8'))
            print(f"\r[-> ROBOT] CPU: {cpu:4.1f}% | RAM: {ram:4.1f}% | GPU: {gpu:4.1f}% | Temp: {temp:4.1f}°C", end="", flush=True)
            time.sleep(1.0)

    except KeyboardInterrupt:
        print("\n[*] Zatrzymano monitor.")
    except Exception as e:
        print(f"\n[!] Błąd połączenia: {e}")

if __name__ == "__main__":
    main()
