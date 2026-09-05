# karemairodnare-archive

Backup/mirror ของชุดข้อมูลและ API จาก `https://260816-karemairodnare.vercel.app`

โปรเจกต์นี้มีเป้าหมายเพื่อเก็บ snapshot ของ API สาธารณะไว้สำรอง โดยคงโครงสร้าง path ใกล้เคียงต้นทาง เช่น:

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

## การทำงาน

GitHub Actions จะรัน `scripts/backup.py` เพื่อดึงไฟล์ JSON จากต้นทาง แล้ว commit เฉพาะเมื่อข้อมูลเปลี่ยน โดยมี checksum และ manifest สำหรับตรวจสอบย้อนหลัง

> ข้อมูลต้นทางมาจากแหล่งเผยแพร่สาธารณะและมีข้อจำกัดด้านความถูกต้อง โปรดอ่าน `_meta.notice` และเก็บ `sources` ไว้เมื่อเผยแพร่ต่อ

## รันเอง

```bash
python scripts/backup.py
```

ผลลัพธ์จะถูกเขียนลง `api/v1/` และ `backup-manifest.json`

## ต้นทาง

- Website/API: https://260816-karemairodnare.vercel.app/api

โปรเจกต์นี้เป็น archive/mirror สำรอง และไม่ใช่เจ้าของข้อมูลต้นทาง
