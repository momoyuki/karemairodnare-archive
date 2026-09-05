# karemairodnare-archive

Community mirror/frontend สำหรับ Karemairodnare public API พร้อมระบบ snapshot สำรอง

## เว็บไซต์

https://momoyuki.github.io/karemairodnare-archive/

หน้าเว็บใช้ API ต้นทางเป็นแหล่งข้อมูลหลัก:

`https://260816-karemairodnare.vercel.app/api/v1/records.json`

เมื่อเปิดหน้าเว็บ browser จะเรียก API ต้นทางโดยตรง จึงเห็นข้อมูลปัจจุบันโดยไม่ต้องรอ GitHub Actions backup หาก API ต้นทางเรียกไม่ได้ frontend จะลองใช้ `api/v1/records.json` จาก snapshot ใน repository แทนอัตโนมัติ

รองรับ full-text search, กรองจังหวัด/อำเภอ/หน่วยงาน, pagination และดูรายละเอียด record

## Architecture

```text
Browser
  |
  +--> upstream public API (primary)
  |      https://260816-karemairodnare.vercel.app/api/v1/records.json
  |
  +--> local snapshot (fallback)
         ./api/v1/records.json
```

GitHub Pages ใช้สำหรับ host frontend เท่านั้น จึงไม่จำเป็นต้องดาวน์โหลด dataset ใหม่ทุกครั้งที่ deploy

## Snapshot backup

`scripts/backup.py` และ workflow `Backup API` ยังเก็บไว้สำหรับ disaster recovery โดยสามารถสร้าง snapshot ของ public API ลงใน `api/v1/` ได้

สามารถรันเองได้จาก **Actions → Backup API → Run workflow** หรือ:

```bash
python scripts/backup.py
```

## Deploy

Workflow `Deploy mirror website` deploy frontend ไป GitHub Pages ทุกครั้งที่ branch `main` เปลี่ยนแปลง

## ข้อมูลและข้อจำกัด

โปรเจกต์นี้เป็น community frontend/mirror ไม่ใช่เว็บไซต์หรือผู้ดูแลข้อมูลต้นทาง ข้อมูลที่แสดงมาจากชุดข้อมูลสาธารณะของต้นทาง และไม่ควรถูกตีความว่าเป็นการยืนยันสถานะทางคดี ความผิด หรือคำพิพากษาของบุคคล ชื่อที่เหมือนกันอาจหมายถึงคนละบุคคล ควรตรวจสอบ `sources`, metadata และเอกสารอ้างอิงของแต่ละรายการก่อนนำข้อมูลไปใช้
