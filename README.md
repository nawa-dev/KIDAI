# KIDAI | KidBright AI Studio 🤖

เว็บแอปพลิเคชันสำหรับเชื่อมต่อ AI / Computer Vision กับบอร์ด KidBright32 ผ่าน Web Serial API โดยตรงบนเบราว์เซอร์

![KIDAI Logo](logonotext.png)

## ✨ ฟีเจอร์หลัก (Features)
- 👤 **โหมดจดจำใบหน้า (Face Recognition):** เทรนและจำแนกใบหน้าหรือวัตถุด้วย TensorFlow.js, MobileNet และ KNN Classifier
- ✋ **โหมดนับนิ้วมือ (Finger Counting):** ตรวจจับมือและนับจำนวนนิ้วแบบ Real-time ด้วย Google MediaPipe Hands
- 🔌 **Web Serial API:** เชื่อมต่อและส่งผลการทำนายไปยังบอร์ด KidBright32 ผ่านพอร์ต USB Serial โดยตรง ไม่ต้องลงโปรแกรมเสริม
- 📦 **KidBright Plugin:** ดาวน์โหลดและติดตั้งปลั๊กอิน `ai_serial.zip` สำหรับรับข้อมูลบนโปรแกรม KidBright IDE ได้ทันที

## 🚀 การใช้งาน (How to Use)
1. เปิดไฟล์ `index.html` บนเบราว์เซอร์ที่รองรับ Web Serial API (เช่น Google Chrome หรือ Microsoft Edge)
2. เชื่อมต่อบอร์ด KidBright32 เข้ากับคอมพิวเตอร์ผ่านสาย USB
3. กดปุ่ม **เชื่อมต่อ KidBright (Connect Serial)** แล้วเลือกพอร์ต COM ของบอร์ด
4. เลือกโหมด AI ที่ต้องการ (จดจำใบหน้า หรือ นับนิ้วมือ) และเริ่มต้นใช้งาน

## 📁 โครงสร้างไฟล์
- `index.html` - หน้าเว็บหลักของ KIDAI Studio
- `logonotext.png` - โลโก้ของ KIDAI
- `ai_serial.zip` - ไฟล์ปลั๊กอินสำหรับนำไปติดตั้งใน KidBright IDE
- `ai_serial_sender.py` - สคริปต์ Python สำหรับทดสอบส่งข้อมูล Serial จำลอง
