
# UrChats - Encrypted Chat Application  
**Your words, your keys, your world.**  
**Developed by [Bell](https://github.com/Bell-O)**

---

## 📋 Table of Contents
1. [Overview](#overview)
2. [System Requirements](#system-requirements)
3. [Installation](#installation)
4. [Supabase Database Setup](#supabase-database-setup)
5. [Usage](#usage)
6. [Key Features](#key-features)
7. [Troubleshooting](#troubleshooting)
8. [Security](#security)
9. [Support](#support)
10. [Important Notes](#important-notes)

---

## 1. 📖 Overview

**UrChats.hee** is an end-to-end encrypted chat application focused on user privacy and data security. It uses advanced encryption technologies and securely stores messages locally.

**Key Features**:

- End-to-end encryption using NaCl Cryptography
- Local encrypted message storage with FlightCode V2
- Real-time message updates
- Emergency Data Wipe system (`191`)
- Automatic key rotation

---

## 2. 💻 System Requirements

**Required Software**:

- Python 3.8 or newer
- pip (Python package manager)
- [Supabase](https://supabase.com) account (Free)
- Internet connection

**Supported Operating Systems**:

- Windows 10/11
- macOS 10.15+
- Linux (Ubuntu, Debian, CentOS, etc.)

---

## 3. 🔧 Installation

### Method 1: Automatic Installation

```bash
cd path/to/UrChats
pip install -r scripts/requirements.txt
python scripts/main.py
```

### Method 2: Manual Installation

```bash
pip install supabase
pip install pynacl
pip install argon2-cffi
pip install cryptography
pip install python-dotenv
pip install colorama
pip install pyfiglet
```

**Verify Installation**:

```bash
python -c "import supabase, nacl, colorama; print('Installation successful!')"
```

---

## 4. 🗄️ Supabase Database Setup

### Step 1: Create a Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Create a new account or log in
3. Click **New Project**
4. Enter project name and password
5. Select your nearest region
6. Click **Create new project**

### Step 2: Get API Keys

- Go to **Settings > API**
- Copy **Project URL** and **anon public key**

### Step 3: Automatic Database Setup

```bash
python scripts/main.py
```

When prompted:

- Supabase URL: `[Enter Project URL]`
- Supabase Key: `[Enter anon public key]`

### Step 4: Manual Database Setup (if needed)

```bash
python scripts/setup_database.py
# or
python scripts/simple_setup.py
```

**Manual SQL Setup**:

- Go to **Supabase Dashboard**
- Open **SQL Editor**
- Run `scripts/manual_setup.sql`

### Step 5: Test Connection

```bash
python scripts/test_connection.py
```

---

## 5. 🚀 Usage

### Getting Started

```bash
python scripts/main.py
```

**Create New User Account**:

- Enter username
- Enter password
- Confirm password

**Log in with Existing Account**:

- Enter password

### Main Menu

1. List users
2. Start chat
3. Rotate key
4. Logout
5. Credits & Support
6. `191` Emergency Data Wipe

### Chat Usage

1. Select **Start chat**
2. Select a user to chat with
3. Type your message and press Enter

**Chat Commands**:

- `quit` - Exit chat
- `clear` - Clear screen and refresh
- `refresh` - Manually refresh messages
- `help` - Show available commands

---

## 6. ✨ Key Features

### Security

- End-to-end encryption with NaCl
- Local encrypted message storage with FlightCode V2
- Automatic key rotation
- Emergency Data Wipe (`191`)

### Real-time Messaging

- Automatic message updates every 3 seconds
- Instant display of new messages

### Data Storage

- Messages stored locally in encrypted format
- User data encrypted with password

---

## 7. 🔧 Troubleshooting

### Database Connection Issues

```text
"Failed to connect to database"
```

**Solution**:

1. Check internet connection
2. Verify Supabase URL and Key in `.env`
3. Test connection:

```bash
python scripts/test_connection.py
```

4. Reinitialize database:

```bash
python scripts/setup_database.py
```

### Missing Database Tables

```text
"Table doesn't exist" or "relation does not exist"
```

**Solution**:

```bash
python scripts/simple_setup.py
```

or use manual SQL setup

### Encryption/Decryption Errors

```text
"Decryption error" or "Invalid message"
```

**Solution**:

1. Verify password
2. Rotate key
3. If still unresolved, delete user data and create a new account

### Python Dependency Issues

```text
"ModuleNotFoundError" or "ImportError"
```

**Solution**:

```bash
pip install -r scripts/requirements.txt
python -m pip install --upgrade pip
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scriptsctivate     # Windows
pip install -r scripts/requirements.txt
```

### Thai Text Display Issues

```bash
export PYTHONIOENCODING=utf-8  # Linux/Mac
set PYTHONIOENCODING=utf-8     # Windows
```

---

## 8. 🔒 Security

### Encryption

- NaCl (libsodium) for E2EE
- Curve25519 for key exchange
- XSalsa20 for message encryption
- Poly1305 for message authentication

### Data Storage

- User data encrypted with FlightCode V2
- Messages stored locally in encrypted format
- Private keys never transmitted over the network
- Passwords never stored as plain text

### Security Recommendations

- Use strong passwords
- Never share your password
- Rotate keys periodically
- Use `191` when needed
- Regularly back up important data

### Emergency Data Wipe (`191`)

1. Select `191` from the main menu
2. Type `DELETE` to confirm
3. Enter your username to reconfirm
4. Data will be permanently deleted

---

## 9. 💬 Support

**Developer Info**:

- Name: Bell  
- GitHub: [github.com/Bell-O](https://github.com/Bell-O)  
- Support: [ko-fi.com/bell_o](https://ko-fi.com/bell_o)

**Reporting Issues**:

1. Check this `README.md`
2. Try solutions in Section 7
3. Contact via GitHub Issues

**Support the Project**:

- [https://ko-fi.com/bell_o](https://ko-fi.com/bell_o)
- Share the project
- Report issues and provide feedback

---

## 📝 Important Notes

- This project is developed for educational and personal use
- The developer is not responsible for data loss
- Regularly back up important data
- Use strong and memorable passwords
- Do not share personal information

---

## 🎉 Thank you for using UrChats!  
**Your words, your keys, your world.**

---

**Version:** 1.0  
**Last updated:** 2024  
**Copyright:** [Bell](https://github.com/Bell-O)


# UrChats.hee - แอปพลิเคชันแชทเข้ารหัส  
**Your words, your keys, your world.**  
**สร้างโดย [Bell](https://github.com/Bell-O)**

---

## 📋 สารบัญ
1. [ข้อมูลทั่วไป](#ข้อมูลทั่วไป)
2. [ความต้องการของระบบ](#ความต้องการของระบบ)
3. [การติดตั้ง](#การติดตั้ง)
4. [การตั้งค่าฐานข้อมูล Supabase](#การตั้งค่าฐานข้อมูล-supabase)
5. [การใช้งาน](#การใช้งาน)
6. [คุณสมบัติหลัก](#คุณสมบัติหลัก)
7. [การแก้ไขปัญหา](#การแก้ไขปัญหา)
8. [ความปลอดภัย](#ความปลอดภัย)
9. [การสนับสนุน](#การสนับสนุน)
10. [หมายเหตุสำคัญ](#หมายเหตุสำคัญ)

---

## 1. 📖 ข้อมูลทั่วไป

**UrChats** เป็นแอปพลิเคชันแชทที่เข้ารหัสแบบ End-to-End ที่ให้ความสำคัญกับความเป็นส่วนตัวและความปลอดภัยของข้อมูล โดยใช้เทคโนโลยีการเข้ารหัสขั้นสูงและจัดเก็บข้อความในเครื่องแบบเข้ารหัส

**คุณสมบัติหลัก**:

- การเข้ารหัสแบบ End-to-End ด้วย NaCl Cryptography
- การจัดเก็บข้อความในเครื่องแบบเข้ารหัสด้วย FlightCode V2
- การอัปเดตข้อความแบบเรียลไทม์
- ระบบลบข้อมูลฉุกเฉิน (รหัส `191`)
- การหมุนเวียนกุญแจเข้ารหัสอัตโนมัติ

---

## 2. 💻 ความต้องการของระบบ

**ซอฟต์แวร์ที่จำเป็น**:

- Python 3.8 หรือใหม่กว่า
- pip (Python package manager)
- บัญชี [Supabase](https://supabase.com) (ฟรี)
- การเชื่อมต่ออินเทอร์เน็ต

**ระบบปฏิบัติการที่รองรับ**:

- Windows 10/11
- macOS 10.15+
- Linux (Ubuntu, Debian, CentOS, etc.)

---

## 3. 🔧 การติดตั้ง

### วิธีที่ 1: การติดตั้งแบบอัตโนมัติ

```bash
cd path/to/UrChats
pip install -r scripts/requirements.txt
python scripts/main.py
```

### วิธีที่ 2: การติดตั้งแบบแยกขั้นตอน

```bash
pip install supabase
pip install pynacl
pip install argon2-cffi
pip install cryptography
pip install python-dotenv
pip install colorama
pip install pyfiglet
```

**ตรวจสอบการติดตั้ง**:

```bash
python -c "import supabase, nacl, colorama; print('Installation successful!')"
```

---

## 4. 🗄️ การตั้งค่าฐานข้อมูล Supabase

### ขั้นตอนที่ 1: สร้างโปรเจกต์ Supabase

1. ไปที่ [supabase.com](https://supabase.com)
2. สร้างบัญชีใหม่หรือเข้าสู่ระบบ
3. คลิก **New Project**
4. ตั้งชื่อโปรเจกต์และรหัสผ่าน
5. เลือก Region
6. คลิก **Create new project**

### ขั้นตอนที่ 2: รับ API Keys

- ไปที่ **Settings > API**
- คัดลอก **Project URL** และ **anon public key**

### ขั้นตอนที่ 3: ตั้งค่าฐานข้อมูลอัตโนมัติ

```bash
python scripts/main.py
```

เมื่อถูกถาม:

- Supabase URL: `[ใส่ Project URL]`
- Supabase Key: `[ใส่ anon public key]`

### ขั้นตอนที่ 4: ตั้งค่าฐานข้อมูลแบบแยก (ถ้าจำเป็น)

```bash
python scripts/setup_database.py
# หรือ
python scripts/simple_setup.py
```

**ใช้ SQL แมนนวล**:

- ไปที่ **Supabase Dashboard**
- เปิด **SQL Editor**
- รัน `scripts/manual_setup.sql`

### ขั้นตอนที่ 5: ทดสอบการเชื่อมต่อ

```bash
python scripts/test_connection.py
```

---

## 5. 🚀 การใช้งาน

### การเริ่มต้นใช้งาน

```bash
python scripts/main.py
```

**สร้างบัญชีผู้ใช้ใหม่**:

- ใส่ชื่อผู้ใช้
- ใส่รหัสผ่าน
- ยืนยันรหัสผ่าน

**เข้าสู่ระบบด้วยบัญชีที่มีอยู่**:

- ใส่รหัสผ่าน

### เมนูหลัก

1. List users
2. Start chat
3. Rotate key
4. Logout
5. Credits & Support
6. `191` Emergency Data Wipe

### การแชท

1. เลือก **Start chat**
2. เลือกผู้ใช้ที่ต้องการแชท
3. พิมพ์ข้อความและกด Enter

**คำสั่งในแชท**:

- `quit` - ออกจากแชท
- `clear` - ล้างหน้าจอและรีเฟรช
- `refresh` - อัปเดตข้อความแบบแมนนวล
- `help` - แสดงคำสั่งทั้งหมด

---

## 6. ✨ คุณสมบัติหลัก

### ความปลอดภัย

- การเข้ารหัส End-to-End ด้วย NaCl
- การจัดเก็บข้อความในเครื่องแบบเข้ารหัสด้วย FlightCode V2
- การหมุนเวียนกุญแจเข้ารหัสอัตโนมัติ
- ระบบลบข้อมูลฉุกเฉิน (รหัส `191`)

### การทำงานแบบเรียลไทม์

- อัปเดตข้อความอัตโนมัติทุก 3 วินาที
- แสดงข้อความใหม่ทันที

### การจัดเก็บข้อมูล

- ข้อความจัดเก็บในเครื่องแบบเข้ารหัส
- ข้อมูลผู้ใช้เข้ารหัสด้วยรหัสผ่าน

---

## 7. 🔧 การแก้ไขปัญหา

### ปัญหาการเชื่อมต่อฐานข้อมูล

```text
"Failed to connect to database"
```

**วิธีแก้**:

1. ตรวจสอบอินเทอร์เน็ต
2. ตรวจสอบ Supabase URL และ Key ใน `.env`
3. ทดสอบ:

```bash
python scripts/test_connection.py
```

4. ตั้งค่าฐานข้อมูลใหม่:

```bash
python scripts/setup_database.py
```

### ปัญหาตารางฐานข้อมูล

```text
"Table doesn't exist" หรือ "relation does not exist"
```

**วิธีแก้**:

```bash
python scripts/simple_setup.py
```

หรือใช้ SQL แมนนวล

### ปัญหาการเข้ารหัส/ถอดรหัส

```text
"Decryption error" หรือ "Invalid message"
```

**วิธีแก้**:

1. ตรวจสอบรหัสผ่าน
2. Rotate key ใหม่
3. หากยังมีปัญหา ให้ลบข้อมูลและสร้างบัญชีใหม่

### ปัญหา Python Dependencies

```text
"ModuleNotFoundError" หรือ "ImportError"
```

**วิธีแก้**:

```bash
pip install -r scripts/requirements.txt
python -m pip install --upgrade pip
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scriptsctivate     # Windows
pip install -r scripts/requirements.txt
```

### ปัญหาการแสดงผลภาษาไทย

```bash
export PYTHONIOENCODING=utf-8  # Linux/Mac
set PYTHONIOENCODING=utf-8     # Windows
```

---

## 8. 🔒 ความปลอดภัย

### การเข้ารหัส

- ใช้ NaCl (libsodium) สำหรับ E2EE
- ใช้ Curve25519 สำหรับ key exchange
- ใช้ XSalsa20 สำหรับการเข้ารหัสข้อความ
- ใช้ Poly1305 สำหรับ message authentication

### การจัดเก็บข้อมูล

- ข้อมูลผู้ใช้เข้ารหัสด้วย FlightCode V2
- ข้อความจัดเก็บในเครื่องแบบเข้ารหัส
- กุญแจส่วนตัวไม่เคยส่งผ่านเครือข่าย
- รหัสผ่านไม่จัดเก็บเป็น plain text

### คำแนะนำความปลอดภัย

- ใช้รหัสผ่านแข็งแกร่ง
- อย่าแชร์รหัสผ่าน
- หมุนเวียนกุญแจบ่อยๆ
- ใช้ `191` เมื่อจำเป็น
- สำรองข้อมูลสำคัญ

### ระบบลบข้อมูลฉุกเฉิน (รหัส `191`)

1. เลือก `191` จากเมนูหลัก
2. พิมพ์ `DELETE`
3. พิมพ์ชื่อผู้ใช้
4. ข้อมูลจะถูกลบถาวร

---

## 9. 💬 การสนับสนุน

**ข้อมูลผู้พัฒนา**:

- ชื่อ: Bell  
- GitHub: [github.com/Bell-O](https://github.com/Bell-O)  
- การสนับสนุน: [ko-fi.com/bell_o](https://ko-fi.com/bell_o)

**การรายงานปัญหา**:

1. ตรวจสอบ `README.md`
2. ลองวิธีแก้ในข้อ 7
3. ติดต่อผ่าน GitHub Issues

**การสนับสนุนโปรเจกต์**:

- [https://ko-fi.com/bell_o](https://ko-fi.com/bell_o)
- แชร์โปรเจกต์
- รายงานปัญหา/ข้อเสนอแนะ

---

## 📝 หมายเหตุสำคัญ

- โปรเจกต์นี้พัฒนาเพื่อการศึกษาและใช้งานส่วนตัว
- ผู้พัฒนาไม่รับผิดชอบต่อการสูญหายของข้อมูล
- กรุณาสำรองข้อมูลสำคัญเป็นประจำ
- ใช้รหัสผ่านที่แข็งแกร่ง
- อย่าแชร์ข้อมูลส่วนตัวกับผู้อื่น

---

## 🎉 ขอบคุณที่ใช้ UrChats!  
**Your words, your keys, your world.**

---

**เวอร์ชัน:** 1.0  
**อัปเดตล่าสุด:** 2024  
**ลิขสิทธิ์:** [Bell](https://github.com/Bell-O)
