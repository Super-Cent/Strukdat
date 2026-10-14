# 🍔 2EZ4U Food Delivery Engine

Aplikasi **2EZ4U Food Delivery Engine** adalah backend layanan antar makanan berbasis desktop GUI (Tkinter)[cite: 39]. Aplikasi ini mengelola data transaksi berskala besar (~200.000 data pesanan) dengan mengimplementasikan struktur data dan algoritma buatan sendiri (*from scratch*) tanpa bergantung pada fungsi bawaan (*built-in*) Python seperti `sort()`, `sorted()`, `dict`, `set`, `heapq`, atau `bisect`[cite: 39, 40].

---

## 🛠️ Modul M1: Data Pesanan (Array vs Linked List)

### 1. Deskripsi Fitur
Modul M1 berfungsi sebagai penampung data utama transaksi yang dimuat dari `data/pesanan.csv`[cite: 39, 43]. Data disimpan secara paralel pada dua struktur data dasar: **Dynamic Array** dan **Singly Linked List** untuk membandingkan performa operasinya[cite: 43, 44].

Aturan bisnis untuk penyisipan pesanan berdasarkan jenis prioritas[cite: 43]:
* **REGULER (Prioritas 3):** Disisipkan di barisan paling belakang[cite: 43, 44].
* **PRIORITAS (Prioritas 2):** Disisipkan menyerobot ke tengah (setelah kelompok VIP)[cite: 43, 44].
* **VIP (Prioritas 1):** Disisipkan langsung di urutan paling depan[cite: 43, 44].

### 2. Kompleksitas & Perbandingan Performa ($N = 200.000$ Baris)

| Operasi / Menu | Dynamic Array | Linked List | Penjelasan Mekanisme Kerja |
| :--- | :---: | :---: | :--- |
| **LIHAT PESANAN** | $O(1)$ ~ $0,02\text{ ms}$[cite: 43, 44] | $O(n)$ ~ $1,80\text{ ms}$[cite: 43, 44] | Array mengakses indeks memori secara langsung, Linked List harus menelusuri simpul dari *head*[cite: 43, 44]. |
| **TAMBAH REGULER** | $O(1)$ amortized ~ $0,02\text{ ms}$[cite: 43, 44] | $O(1)$ ~ $0,01\text{ ms}$[cite: 43, 44] | Array menempel di ujung kapasitas cadangan; Linked List menggunakan penunjuk *tail*[cite: 43, 44]. |
| **TAMBAH PRIORITAS** | $O(n)$ ~ $3,71\text{ ms}$[cite: 43, 44] | $O(n)$ ~ $2,19\text{ ms}$[cite: 43, 44] | Array menggeser $\sim 100.000$ elemen; Linked List menelusuri $\sim 100.000$ simpul lalu menyambung *pointer*[cite: 44]. |
| **TAMBAH VIP** | $O(n)$ ~ $6,82\text{ ms}$[cite: 43, 44] | $O(1)$ ~ $0,00\text{ ms}$[cite: 43, 44] | Array menggeser seluruh isi elemen ke kanan; Linked List hanya memperbarui penunjuk *head*[cite: 44]. |
| **HAPUS PESANAN** | $O(n)$ ~ $3,50\text{ ms}$[cite: 43, 44] | $O(n)$ ~ $2,10\text{ ms}$[cite: 43, 44] | Array menggeser sisa elemen ke kiri; Linked List melakukan penelusuran lalu memutus rantai simpul[cite: 43, 44]. |

---

## 🔄 Modul M2: Stack (Kasir & Undo/Redo) & Queue (Antrean)

### 1. Deskripsi Fitur
* **Stack Evaluator Kasir:** Mengubah ekspresi struk belanja dari bentuk *infix* ke *postfix* (`ke_postfix`), lalu menghitung totalnya (`hitung`)[cite: 45].
* **Stack Undo & Redo Histori:** Membatalkan (`undo_last`) atau mengerjakan ulang (`redo_last`) aksi transaksi M1 maupun Dequeue M2[cite: 45, 47]. Menggunakan dua tumpukan terpisah; setiap aksi baru akan otomatis mengosongkan tumpukan Redo[cite: 45, 47].
* **Queue Pemrosesan Pesanan:** Menampung pesanan berstatus `ANTRE`[cite: 45, 50]. Dibandingkan dalam 2 versi[cite: 45, 49]:
  * **Antrean Naif (Larik Biasa):** Mengambil elemen depan dengan `pop(0)`, memaksa seluruh sisa elemen digeser[cite: 49].
  * **Antrean Melingkar (Circular Array):** Menggunakan penunjuk `front` dan `rear` berputar berbasis modulo ($O(1)$) tanpa pergeseran memori[cite: 49].

### 2. Perbandingan Performa Queue ($N = 19.850$ Pesanan ANTRE)

| Aksi | Antrean Naif (Array Biasa) | Antrean Melingkar (Circular Array) | Selisih Performa & Keterangan |
| :--- | :---: | :---: | :--- |
| **ENQUEUE (1 pesanan)** | $0,08\text{ ms}$ (0 geseran)[cite: 50] | $0,03\text{ ms}$ (0 geseran)[cite: 50] | Sama-sama murah karena hanya menempel di ujung belakang[cite: 50]. |
| **DEQUEUE (100 pesanan)** | $93,27\text{ ms}$ ($1.979.950$ geseran)[cite: 50] | $0,03\text{ ms}$ (**0 geseran**)[cite: 50] | **Circular Array jauh lebih unggul** karena hanya memajukan penunjuk `front`[cite: 49, 50]. |

---

## 📊 Modul M3: Laporan Terurut (Sorting) & Pencarian (Searching)

### 1. Penjelasan Algoritma & Struktur Data
* **Insertion Sort ($O(N^2)$):** Menggeser elemen mundur satu per satu sampai menemukan tempatnya (In-place & Stabil). Dibatasi maks $5.000$ baris pada GUI untuk mencegah pembekuan aplikasi[cite: 58].
* **Merge Sort ($O(N \log N)$):** Membelah array secara rekursif lalu menggabungkannya kembali (Divide & Conquer, Stabil). Sanggup mengurutkan seluruh $200.000$ data.
* **Linear Search ($O(N)$):** Memeriksa elemen satu per satu dari awal. Tidak menuntut data terurut[cite: 53, 56].
* **Binary Search ($O(\log N)$):** Membuang separuh sisa ruang pencarian di setiap langkah[cite: 55, 56]. Wajib dijalankan di atas data yang **sudah terurut** berdasarkan kunci `oid`.

---

### 2. Tabel Uji Perbandingan Elemen ($N$) vs Jumlah Perbandingan

#### Tabel A: Perbandingan Algoritma Sorting (Kunci: Harga)

| Jumlah Baris ($N$) | Insertion Sort (Perbandingan) | Insertion Sort (Waktu) | Merge Sort (Perbandingan) | Merge Sort (Waktu) | Pola Pertumbuhan |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **10** | $24$[cite: 54] | $0,11\text{ ms}$[cite: 54] | $22$ | $0,05\text{ ms}$ | Performa setara pada data sangat kecil[cite: 54]. |
| **1.000** | $241.520$ | $42,10\text{ ms}$ | $8.712$ | $1,82\text{ ms}$ | Merge Sort $\approx 23\times$ lebih cepat. |
| **2.000** | $962.430$[cite: 57] | $163,26\text{ ms}$[cite: 57] | $19.240$[cite: 57] | $3,85\text{ ms}$ | Insertion naik $4\times$ ($N^2$)[cite: 57]. |
| **4.000** | $3.831.520$[cite: 57] | $660,36\text{ ms}$[cite: 57] | $42.355$[cite: 57] | $8,32\text{ ms}$[cite: 57] | Merge Sort naik $2\times$ ($N \log N$)[cite: 57]. |
| **5.000** | $6.012.300$ | $1.020,15\text{ ms}$ | $54.120$ | $10,80\text{ ms}$ | Batas maksimum penolakan Insertion Sort. |
| **200.000** | *DITOLAK SISTEM*[cite: 57] | *DITOLAK*[cite: 57] | $3.226.139$[cite: 57] | $317,80\text{ ms}$ | Hanya Merge Sort yang sanggup menangani[cite: 57]. |

---

#### Tabel B: Perbandingan Algoritma Searching (Target: `oid` pada $200.001$ Data)

| Target Pencarian | Position / Case | Linear Search (Perbandingan) | Linear Search (Waktu) | Binary Search (Perbandingan) | Binary Search (Waktu) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **`O-000001`** | Indeks Paling Depan | $1$ | $0,01\text{ ms}$ | $17$ | $0,03\text{ ms}$ |
| **`O-137442`** | Indeks Tengah | $137.442$ | $26,28\text{ ms}$[cite: 56] | $16$[cite: 57] | $0,05\text{ ms}$[cite: 57] |
| **`O-199999`** | Indeks Paling Belakang | $199.999$[cite: 57] | $24,52\text{ ms}$[cite: 57] | $17$[cite: 57] | $0,03\text{ ms}$[cite: 57] |
| **`O-999999`** | Data Tidak Ada | $200.001$ | $28,10\text{ ms}$ | $18$ | $0,04\text{ ms}$ |
