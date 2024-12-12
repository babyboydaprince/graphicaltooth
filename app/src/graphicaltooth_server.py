import bluetooth
import pyscreenshot as ImageGrab
import io
import time

def capture_screen():
    """Capture the screen and return it as a compressed JPEG byte stream."""
    screen = ImageGrab.grab()  # Capture the full screen
    buffer = io.BytesIO()
    screen.save(buffer, format="JPEG", quality=50)  # Save as JPEG with compression
    return buffer.getvalue()

def bluetooth_server():
    server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    server_socket.bind(("", bluetooth.PORT_ANY))
    server_socket.listen(1)

    print("Waiting for Bluetooth connection...")
    client_socket, client_address = server_socket.accept()
    print(f"Connection established with {client_address}")

    try:
        while True:
            # Capture screen and send
            screen_data = capture_screen()
            client_socket.sendall(len(screen_data).to_bytes(4, "big"))  # Send data length
            client_socket.sendall(screen_data)  # Send screen data

            time.sleep(0.5)  # Delay for smoother streaming
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()
        server_socket.close()

if __name__ == "__main__":
    bluetooth_server()
