from kivy.app import App
from kivy.uix.button import Button
from plyer import camera
import socket
import struct
import os
import threading
import time

SERVER_IP = '172.20.10.11'  # Replace with your server IP
PORT = 4444

class CameraSenderApp(App):
    def build(self):
        self.btn = Button(text="Start Sending Camera Frames")
        self.btn.bind(on_press=self.start_sending)
        return self.btn

    def start_sending(self, instance):
        threading.Thread(target=self.capture_and_send_loop, daemon=True).start()
        self.btn.text = "Running..."

    def capture_and_send_loop(self):
        while True:
            try:
                filename = "image.jpg"
                camera.take_picture(filename, self.send_image)
                time.sleep(2)  # Capture every 2 seconds
            except Exception as e:
                print(f"[!] Capture failed: {e}")

    def send_image(self, path):
        try:
            with open(path, 'rb') as f:
                data = f.read()
            size = len(data)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((SERVER_IP, PORT))
            sock.sendall(struct.pack("Q", size) + data)
            sock.close()
            print(f"[+] Sent image of size {size} bytes")
        except Exception as e:
            print(f"[!] Sending failed: {e}")

if __name__ == '__main__':
    CameraSenderApp().run()
