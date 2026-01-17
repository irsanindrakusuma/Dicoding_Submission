# Proyek Analisis Data: E-Commerce Brasil

## Deskripsi

Proyek ini menganalisis dataset E-Commerce publik Brasil untuk menjawab dua pertanyaan bisnis utama:

1. Bagaimana pola waktu pengiriman mempengaruhi kepuasan pelanggan?
2. Bagaimana distribusi keterlambatan pengiriman di setiap wilayah?

Analisis menggunakan teknik geospatial analysis untuk memvisualisasikan sebaran geografis keterlambatan pengiriman.

## Struktur Direktori

```
submission/
├── dashboard/
│   ├── dashboard.py
│   ├── orders_reviews.csv
│   └── geo_orders.csv
├── data/
│   ├── customers_dataset.csv
│   ├── geolocation_dataset.csv
│   ├── order_items_dataset.csv
│   ├── order_payments_dataset.csv
│   ├── order_reviews_dataset.csv
│   ├── orders_dataset.csv
│   ├── products_dataset.csv
│   ├── product_category_name_translation.csv
│   └── sellers_dataset.csv
├── notebook.ipynb
├── README.md
├── requirements.txt
├── pyproject.toml
└── url.txt
```

## Setup Environment

### Menggunakan UV

```bash
cd submission
uv sync
```

### Menggunakan pip

```bash
cd submission
pip install -r requirements.txt
```

## Menjalankan Proyek

### 1. Menjalankan Notebook

```bash
uv run jupyter notebook notebook.ipynb
```

Jalankan semua cell untuk menghasilkan data dashboard di folder `dashboard/`.

### 2. Menjalankan Dashboard

```bash
uv run streamlit run dashboard/dashboard.py
```

Akses di browser: http://localhost:8501

## Fitur Dashboard

- Filter interaktif berdasarkan skor review dan waktu pengiriman
- Ringkasan metrik: total order, rata-rata pengiriman, rata-rata skor, korelasi
- Tab 1: Boxplot hubungan waktu pengiriman dan kepuasan
- Tab 2: Bar chart dan scatter plot distribusi geografis keterlambatan

## Hasil Analisis

### Pertanyaan 1

Terdapat korelasi negatif (-0.334) antara waktu pengiriman dan skor review. Pengiriman cepat berkorelasi dengan kepuasan tinggi.

### Pertanyaan 2

Keterlambatan tersebar merata di seluruh wilayah Brasil, mengindikasikan masalah sistemik pada logistik.

## Author

Irsan Indra Kusuma

- Email: i.i.kusuma@student.rug.nl
- ID Dicoding: Irsan Indra Kusuma
