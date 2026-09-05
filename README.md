# karemairodnare-archive

Backup/mirror ของชุดข้อมูลและ API จาก `https://260816-karemairodnare.vercel.app` พร้อมหน้าเว็บสำรองสำหรับค้นหาข้อมูลโดยไม่ต้องพึ่ง API ต้นทาง

## เว็บไซต์สำรอง

เมื่อเปิด GitHub Pages แล้ว เว็บไซต์จะอยู่ที่:

`https://momoyuki.github.io/karemairodnare-archive/`

หน้าเว็บอ่าน `api/v1/records.json` จาก snapshot ใน repository โดยตรง รองรับการค้นหาทุกข้อความ, กรองจังหวัด/อำเภอ/หน่วยงาน, pagination และดูรายละเอียด record

## ข้อมูลที่สำรอง

โครงสร้าง API ถูก mirror ไว้ใกล้เคียงต้นทาง เช่น:

- `/api/v1/records.json`
- `/api/v1/provinces.json`
- `/api/v1/provinces/{slug}.json`
- `/api/v1/districts.json`
- `/api/v1/districts/{slug}.json`
- `/api/v1/agencies.json`
- `/api/v1/agencies/{slug}.json`
- `/api/v1/meta.json`
- `/api/v1/index.json`
- `/api/v1/openapi.json`

## Automatic backup

GitHub Actions รัน `scripts/backup.py` ทุกวันเพื่อดึง snapshot ใหม่ แล้ว commit เฉพาะเมื่อข้อมูลเปลี่ยน พร้อม `backup-manifest.json` และ SHA-256 checksum สำหรับตรวจสอบไฟล์

สามารถรันเองได้จาก **Actions → Backup API → Run workflow** หรือในเครื่อง:

```bash
python scripts/backup.py
```

## Deploy website

Workflow `Deploy archive website` จะ deploy หน้าเว็บไป GitHub Pages เมื่อ branch `main` เปลี่ยนแปลง หาก repository ยังไม่เคยเปิด Pages ให้เข้า **Settings → Pages → Build and deployment → Source** แล้วเลือก **GitHub Actions** หนึ่งครั้ง

## ต้นทางและข้อจำกัด

- Website/API: `https://260816-karemairodnare.vercel.app/api`
- โปรเจกต์นี้เป็น archive/mirror สำรอง ไม่ใช่เว็บไซต์หรือผู้ดูแลข้อมูลต้นทาง
- ข้อมูลต้นทางมาจากแหล่งเผยแพร่สาธารณะและอาจมีข้อจำกัดด้านความถูกต้อง ควรตรวจ `sources` และ metadata ของข้อมูลก่อนนำไปอ้างอิง
