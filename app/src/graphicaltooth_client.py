import bluetooth
import io
from PIL import Image
import tkinter as tk
from tkinter import Label

def bluetooth_client(server_mac):
    """Connect to the server and display streamed images."""
    client_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    client_socket.connect((server_mac, 3))  # Replace 3 with the appropriate channel

    print("Connected to the server.")

    # Set up a simple Tkinter GUI for image display
    root = tk.Tk()
    root.title("Bluetooth Screen Stream")
    label = Label(root)
    label.pack()

    try:
        while True:
            # Receive image data
            data_length = int.from_bytes(client_socket.recv(4), "big")  # First 4 bytes = length
            image_data = client_socket.recv(data_length)

            # Display image
            image = Image.open(io.BytesIO(image_data))
            tk_image = tk.PhotoImage(image)
            label.config(image=tk_image)
            label.image = tk_image
            root.update_idletasks()
            root.update()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    # Replace with the server's Bluetooth MAC address
    server_mac_address = "XX:XX:XX:XX:XX:XX"
    bluetooth_client(server_mac_address)
