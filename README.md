# 🧾 SealPay - Watermarking untuk Invoice Digital dengan QIM

**SealPay** adalah aplikasi yang menggunakan algoritma **Quantization Index Modulation (QIM)** untuk menyisipkan watermark pada invoice digital. Tujuannya adalah menjaga keaslian, mencegah pemalsuan, dan memberikan perlindungan hak cipta pada dokumen invoice.

---

## 📌 Fitur Unggulan

- 🔐 **Pembuatan Invoice** lengkap dengan watermark digital tersembunyi.
- 🕵️‍♀️ **Verifikasi Keaslian Invoice** dengan ekstraksi watermark.
- 🧾 **Riwayat Invoice** disimpan otomatis dan dapat ditelusuri.
- 📂 Manajemen dan penyimpanan data invoice dalam format JSON.

---

## 🧰 Teknologi Digunakan

- Python 3.x
- OpenCV
- PIL (Pillow)
- NumPy
- JSON

---

## 📁 Struktur Proyek

```
SealPay/
├── assets/
│   └── images/
│       └── watermark.png
│
├── pages/                  
│   ├── about.py
│   ├── create_invoice.py
│   ├── history.py
│   ├── home.py
│   └── verify_invoice.py
│
├── utils/                      
│   ├── history_manager.py       
│   ├── invoice_gen.py          
│   └── watermark.py            
│
├── invoice_history.json         
├── main.py                      
└── README.md
```

---

## 🚀 Cara Menjalankan Aplikasi

1. **Clone repository ini:**

```bash
git clone https://github.com/lyraaa18/QIM.git
cd QIM
```

2. **(Opsional) Buat virtual environment:**

```bash
python -m venv venv
source venv/bin/activate       
venv\Scripts\activate      
```

3. **Install dependensi:**

```bash
pip install -r requirements.txt
```

4. **Jalankan aplikasi:**

```bash
streamlit run main.py
```

---

## 📸 Alur Penggunaan

1. **Buka aplikasi** dan navigasi ke halaman **Create Invoice**.
2. **Isi detail invoice** dan watermark akan disisipkan otomatis.
3. **Download invoice** dengan watermark tersembunyi.
4. Gunakan halaman **Verify Invoice** untuk mengekstrak dan memverifikasi watermark.
5. Cek semua invoice sebelumnya di halaman **History**.

---

## 📜 Lisensi

Proyek ini dibuat untuk kebutuhan akademik. Bebas digunakan dengan mencantumkan atribusi kepada pengembang.

---

## 👩‍💻 Pengembang

- **Delvina salma Hidayah**  
  Mahasiswa Informasika, Universitas Siliwangi  
  [GitHub](https://github.com/lyraaa18)
- **Ikhwan Kurniawan Julianto**  
  Mahasiswa Informasika, Universitas Siliwangi  
  [GitHub](https://github.com/rhenaald)
- **Alya Shaumi**  
  Mahasiswa Informasika, Universitas Siliwangi  
  [GitHub](https://github.com/alin03s)
