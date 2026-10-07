# master_bsc

Sumber data KPI untuk **BSC Designer** (data source "HTTP / web script").
Data disimpan sebagai CSV, lalu diubah menjadi file JSON yang diambil BSC Designer langsung dari GitHub (raw).

## Format yang dibaca BSC Designer

BSC Designer memanggil satu URL per tanggal dan membaca field `value`:

```json
{"value": 4931164624, "name": "Revenue Jakarta"}
```

## Setting di BSC Designer

Di **KPI data source → Query properties** pada indikator:

| Field | Isi |
|---|---|
| Url template | `https://raw.githubusercontent.com/firzi15/master_bsc/main/api/revenue_jakarta/%%date%%.json` |
| Date format | `yyyy-MM` |

Klik **Test url**. Contoh untuk April 2026:
`https://raw.githubusercontent.com/firzi15/master_bsc/main/api/revenue_jakarta/2026-04.json`

Nama indikator ditulis langsung di URL (bukan `%%name%%`) agar tidak bermasalah dengan spasi.

Catatan: setelah data diubah, URL raw bisa butuh beberapa menit sebelum menampilkan angka terbaru (cache GitHub).

## Menambah / mengubah data

1. Edit atau tambah file di `data/`, misalnya `data/revenue_bandung.csv`:
   ```csv
   bulan,value
   2026-01,1234567890
   ```
   Angka boleh ditulis dengan titik ribuan (`4.931.164.624`).
2. Commit ke `main`. GitHub Actions menjalankan `build.py` dan memperbarui folder `api/` otomatis.
3. URL indikator baru: `https://raw.githubusercontent.com/firzi15/master_bsc/main/api/revenue_bandung/%%date%%.json`

Daftar semua indikator dan bulan yang tersedia: `api/index.json`.

Menjalankan secara lokal: `python build.py`
