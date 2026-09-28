import subprocess
import platform
import ipaddress
import re


def validar_ip(ip):
    """Comprueba que la dirección IP ingresada sea válida."""
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def hacer_ping(ip):
    """
    Realiza un ping a una dirección IP.
    Devuelve el estado del dispositivo y la latencia.
    """

    sistema = platform.system().lower()

    if sistema == "windows":
        comando = ["ping", "-n", "1", "-w", "2000", ip]
    else:
        comando = ["ping", "-c", "1", "-W", "2", ip]

    try:
        resultado = subprocess.run(
            comando,
            capture_output=True,
            text=True,
            timeout=5
        )

        if resultado.returncode == 0:

            # Buscar latencia en la respuesta del ping
            coincidencia = re.search(
                r"(?:time|tiempo)[=<]?\s*(\d+(?:\.\d+)?)\s*ms",
                resultado.stdout,
                re.IGNORECASE
            )

            if coincidencia:
                latencia = f"{coincidencia.group(1)} ms"
            else:
                latencia = "No disponible"

            return "ONLINE", latencia

        return "OFFLINE", "-"

    except subprocess.TimeoutExpired:
        return "OFFLINE", "-"

    except Exception as error:
        return "ERROR", str(error)


def mostrar_encabezado():
    print("\n" + "=" * 40)
    print("          NETWORK MONITOR v1")
    print("=" * 40)


def main():

    mostrar_encabezado()

    ip = input("\nIngrese una dirección IP: ").strip()

    if not validar_ip(ip):
        print("\n[ERROR] La dirección IP ingresada no es válida.")
        return

    print(f"\nComprobando conectividad con {ip}...\n")

    estado, latencia = hacer_ping(ip)

    print("-" * 40)
    print(f"IP:        {ip}")
    print(f"Estado:    {estado}")
    print(f"Latencia:  {latencia}")
    print("-" * 40)

    if estado == "ONLINE":
        print("\nEl dispositivo responde correctamente.")
    elif estado == "OFFLINE":
        print("\nEl dispositivo no responde al ping.")
    else:
        print("\nSe produjo un error durante la comprobación.")


if __name__ == "__main__":
    main()