"""
KidBright AI Serial Bridge (Python Version)
===========================================
สคริปต์ Python ทางเลือกสำหรับรันโมเดล Teachable Machine (Keras / TensorFlow)
และส่งผลลัพธ์ผ่าน Serial ไปยัง KidBright

ความต้องการ:
  pip install opencv-python tensorflow pyserial
"""

import time
import sys
import serial
import cv2
import numpy as np

# 1. ตั้งค่าโมเดลและพอร์ต Serial
MODEL_PATH = "keras_model.h5"     # ไฟล์โมเดลที่ export มาจาก Teachable Machine
LABELS_PATH = "labels.txt"        # ไฟล์ labels.txt จาก Teachable Machine
SERIAL_PORT = "COM3"              # เปลี่ยนตามพอร์ตของบอร์ด KidBright
BAUD_RATE = 115200
THRESHOLD = 0.80                  # ความมั่นใจขั้นต่ำ 80%
SEND_INTERVAL = 0.5               # ส่งทุก 0.5 วินาที

def main():
    # โหลด Labels
    try:
        with open(LABELS_PATH, "r", encoding="utf-8") as f:
            class_names = [line.strip().split(" ", 1)[-1] for line in f.readlines()]
    except Exception as e:
        print(f"Error loading {LABELS_PATH}: {e}")
        class_names = []

    # โหลดโมเดล Keras
    try:
        import tensorflow as tf
        model = tf.keras.models.load_model(MODEL_PATH, compile=False)
        print("✅ โหลดโมเดลสำเร็จ!")
    except Exception as e:
        print(f"❌ โหลดโมเดลไม่สำเร็จ: {e}")
        return

    # เชื่อมต่อ Serial
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"✅ เชื่อมต่อ Serial {SERIAL_PORT} สำเร็จ!")
    except Exception as e:
        print(f"⚠️ ไม่สามารถเปิด Serial {SERIAL_PORT}: {e}")
        ser = None

    # เปิดกล้อง WebCam
    cap = cv2.VideoCapture(0)
    last_send_time = 0

    print("🚀 เริ่มต้นระบบตรวจจับ... กด 'q' เพื่อออก")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # ปรับขนาดภาพให้ตรงกับ Teachable Machine (224x224)
        image = cv2.resize(frame, (224, 224), interpolation=cv2.INTER_AREA)
        image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)
        image = (image / 127.5) - 1

        # ทำนายผล
        prediction = model.predict(image, verbose=0)
        index = np.argmax(prediction)
        confidence = prediction[0][index]
        class_name = class_names[index] if index < len(class_names) else f"Class_{index}"

        # แสดงผลบนหน้าจอวิดีโอ
        text = f"{class_name}: {confidence * 100:.1f}%"
        color = (0, 255, 0) if confidence >= THRESHOLD else (0, 0, 255)
        cv2.putText(frame, text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        cv2.imshow("KidBright AI Camera", frame)

        # ส่งค่าผ่าน Serial หากความมั่นใจถึงเกณฑ์
        current_time = time.time()
        if confidence >= THRESHOLD and (current_time - last_send_time >= SEND_INTERVAL):
            if ser and ser.is_open:
                ser.write(f"{class_name}\n".encode("utf-8"))
                print(f"📤 ส่งข้อมูล: {class_name} ({confidence*100:.1f}%)")
            last_send_time = current_time

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    if ser and ser.is_open:
        ser.close()

if __name__ == "__main__":
    main()
