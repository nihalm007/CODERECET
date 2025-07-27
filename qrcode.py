import cv2
from pyzbar.pyzbar import decode
import numpy as np
import time

def scan_qr(picam2):
    print("📷 Looking for QR code... Show QR to camera.")
    start_time = time.time()
    timeout = 1000  # seconds

    while True:
        frame = picam2.capture_array()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        qr_codes = decode(gray)

        for qr in qr_codes:
            qr_data = qr.data.decode("utf-8")
            print("✅ QR Code Detected:", qr_data)
            return qr_data
            

        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    print("⚠️ QR code scan timed out.")
    return None
