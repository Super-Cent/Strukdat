# 2EZ4U Food Delivery Engine

## Modul M1: Data Pesanan (Array vs Linked List)

### 1. Deskripsi Fitur
Modul M1 berfungsi sebagai penampung data utama transaksi yang dimuat dari data/pesanan.csv. Data disimpan secara paralel pada dua struktur data dasar: Dynamic Array dan Singly Linked List untuk membandingkan performa operasinya.

Aturan bisnis untuk penyisipan pesanan berdasarkan jenis prioritas:
* REGULER (Prioritas 3): Disisipkan di barisan paling belakang.
* PRIORITAS (Prioritas 2): Disisipkan menyerobot ke tengah (setelah kelompok VIP).
* VIP (Prioritas 1): Disisipkan langsung di urutan paling depan.

### 2. Kompleksitas & Perbandingan Performa Riil Perangkat

| Operasi / Menu | Dynamic Array | Linked List | Penjelasan Mekanisme Kerja |
| :--- | :---: | :---: | :--- |
| **LIHAT PESANAN** | O(1) ~ 0,00 ms | O(n) ~ 8,85 ms | Array mengakses indeks memori secara langsung, Linked List harus menelusuri simpul satu per satu. |
| **TAMBAH REGULER** | O(1) amortized ~ 0,02 ms | O(1) ~ 0,00 ms | Array menempel di ujung kapasitas cadangan; Linked List langsung disambungkan via pointer tail. |
| **TAMBAH PRIORITAS** | O(n) ~ 25,61 ms | O(n) ~ 0,01 ms | Array menggeser ribuan elemen memori; Linked List menelusuri rantai simpul lalu menyambung pointer. |
| **TAMBAH VIP** | O(n) ~ 24,04 ms | O(1) ~ 0,01 ms | Array menggeser seluruh isi elemen ke kanan; Linked List hanya memperbarui penunjuk head. |
| **HAPUS PESANAN** | O(n) ~ 18,97 ms | O(n) ~ 8,72 ms | Array menggeser sisa elemen ke kiri; Linked List melakukan penelusuran lalu memutus rantai simpul. |

---

## Modul M2: Stack (Kasir & Undo/Redo) & Queue (Antrean)

### 1. Deskripsi Fitur
* Stack Evaluator Kasir: Mengubah ekspresi struk belanja dari bentuk infix ke postfix (ke_postfix), lalu menghitung totalnya (hitung).
* Stack Undo & Redo Histori: Membatalkan (undo_last) atau mengerjakan ulang (redo_last) aksi transaksi M1 maupun Dequeue M2. Menggunakan dua tumpukan terpisah; setiap aksi baru akan otomatis mengosongkan tumpukan Redo.
* Queue Pemrosesan Pesanan: Menampung pesanan berstatus ANTRE. Dibandingkan dalam 2 versi:
  * Antrean Naif (Larik Biasa): Mengambil elemen depan dengan pop(0), memaksa seluruh sisa elemen digeser.
  * Antrean Melingkar (Circular Array): Menggunakan penunjuk front dan rear berputar berbasis modulo O(1) tanpa pergeseran memori.

### 2. Perbandingan Performa Queue Riil

| Aksi | Antrean Naif (Array Biasa) | Antrean Melingkar (Circular Array) | Selisih Performa & Keterangan |
| :--- | :---: | :---: | :--- |
| **ENQUEUE (Pesanan Baru)** | 30,23 ms | 33,93 ms | Sama-sama murah karena hanya menempel di ujung belakang antrean. |
| **DEQUEUE (1 Pesanan)** | 0,02 ms | 0,02 ms | Pergeseran elemen masih relatif ringan pada skala sampel kecil. |
| **DEQUEUE (100 Pesanan)** | 0,70 ms | **0,06 ms** | **Circular Array ~11.6x lebih cepat** karena hanya memajukan penunjuk front tanpa menggeser isi memori. |

---

## Modul M3: Laporan Terurut (Sorting) & Pencarian (Searching)

### 1. Penjelasan Algoritma & Struktur Data
* Insertion Sort O(N^2): Menggeser elemen mundur satu per satu sampai menemukan tempatnya (In-place & Stabil). Dibatasi maks 5.000 baris pada GUI untuk mencegah pembekuan aplikasi.
* Merge Sort O(N log N): Membelah array secara rekursif lalu menggabungkannya kembali (Divide & Conquer, Stabil). Sanggup mengurutkan seluruh data secara konsisten.
* Linear Search O(N): Memeriksa elemen satu per satu dari awal. Tidak menuntut data terurut.
* Binary Search O(log N): Membuang separuh sisa ruang pencarian di setiap langkah. Wajib dijalankan di atas data yang **sudah terurut** berdasarkan kunci oid.

---

### 2. Tabel Uji Perbandingan Elemen (N) vs Durasi Waktu Riil

#### Tabel A: Perbandingan Algoritma Sorting (Kunci: Harga)

| Jumlah Baris (N) | Insertion Sort (Waktu Riil) | Merge Sort (Waktu Riil) | Rasio / Pola Pertumbuhan |
| :---: | :---: | :---: | :--- |
| **10** | 0,03 ms | 0,03 ms | Performa identik pada data sangat kecil. |
| **1.000** | 28,33 ms | 1,99 ms | Merge Sort ~14.2x lebih cepat. |
| **5.000** | 806,72 ms | 10,69 ms | **Merge Sort ~75.4x lebih cepat** (Insertion Sort membengkak akibat O(N^2)). |
| **200.000** | DITOLAK SISTEM | 317,80 ms | Batas aman Insertion Sort terlampaui; Merge Sort menyelesaikan seluruh dataset. |

---

#### Tabel B: Perbandingan Algoritma Searching (Target: oid)

| Target Pencarian | Posisi Indeks Data | Linear Search (Waktu Riil) | Binary Search (Waktu Riil) | Analisis Efisiensi |
| :--- | :--- | :---: | :---: | :--- |
| **O-000001** | Indeks Paling Depan | 0,00 ms | 0,02 ms | Linear Search menemukan target di langkah pertama. |
| **O-002500** | Indeks Tengah | 0,36 ms | **0,02 ms** | Binary Search ~18x lebih cepat. |
| **O-004996** | Indeks Belakang (Maks) | 0,84 ms | **0,03 ms** | **Binary Search ~28x lebih cepat** (Linear Search harus menelusuri seluruh baris). |
| **O-999999** | Data Tidak Ada | 0,88 ms | 0,03 ms | Kasus terburuk Linear Search menyentuh seluruh elemen data. |

---
