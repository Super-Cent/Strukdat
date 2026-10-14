"""
M3: Laporan Terurut - Insertion Sort + Binary Search
Proyek 2EZ4U APP - Struktur Data & Analisa Algoritma (EC234303)

Alur pengerjaan M3:
1. Implementasi insertion sort generik (berdasarkan field apa saja)
2. Implementasi binary search (hanya valid pada larik yang sudah terurut)
3. ambil_subset(): filter dulu dari struktur M1 (resto/status/batas baris)
   sebelum di-sort, karena insertion sort O(n^2) terlalu lambat untuk
   langsung diterapkan ke 200.000 baris sekaligus
4. buat_laporan(): gabungkan filter + insertion sort jadi satu alur
5. cari_di_laporan(): bungkus binary_search supaya gampang dipakai UI

CATATAN: tidak menggunakan instant function (dict, set, sorted, .sort(),
heapq, bisect, collections.*, literal {}, comprehension dict/set).
"""


def insertion_sort(larik, kunci):
    """
    Urutkan larik (list of Pesanan) menurut atribut bernama `kunci`
    (misal "harga" atau "t_masuk_detik"), menaik (ascending), IN-PLACE.

    Cara kerja: ambil elemen satu-satu dari kiri, geser elemen yang lebih
    besar ke kanan, sisipkan elemen itu di posisi yang tepat di bagian
    larik yang sudah terurut (mirip mengurutkan kartu remi di tangan).

    Kompleksitas: O(n^2) di rata-rata/terburuk - makanya HANYA dipakai
    untuk subset data (lihat ambil_subset), bukan 200.000 baris langsung.
    """
    i = 1
    while i < len(larik):
        current = larik[i]
        nilai_current = getattr(current, kunci)

        j = i - 1
        while j >= 0 and getattr(larik[j], kunci) > nilai_current:
            larik[j + 1] = larik[j]
            j -= 1
        larik[j + 1] = current

        i += 1
    return larik


def binary_search(larik_terurut, kunci, nilai_target):
    """
    Cari index elemen dengan atribut `kunci` == nilai_target di dalam
    larik yang SUDAH TERURUT menaik berdasarkan kunci yang sama.
    Mengembalikan index jika ketemu, atau -1 jika tidak ada.

    Cara kerja: bandingkan nilai_target dengan elemen TENGAH larik,
    lalu persempit pencarian ke separuh kiri/kanan, ulangi terus.

    Kompleksitas: O(log n) - PENTING: kalau larik belum terurut,
    hasilnya tidak bisa diandalkan (bisa salah/tidak ketemu padahal ada).
    """
    lo = 0
    hi = len(larik_terurut) - 1

    while lo <= hi:
        mid = (lo + hi) // 2
        nilai_mid = getattr(larik_terurut[mid], kunci)

        if nilai_mid == nilai_target:
            return mid
        elif nilai_mid < nilai_target:
            lo = mid + 1
        else:
            hi = mid - 1

    return -1


def ambil_subset(struktur, filter_resto=None, filter_status=None, maks_baris=None):
    """
    Telusuri struktur M1 (Array atau LinkList) satu per satu lewat get(i),
    salin pesanan yang cocok filter ke dalam list Python biasa (sebagai
    "working copy" laporan, bukan mengubah struktur M1 aslinya).

    filter_resto  : None = semua resto, atau nama resto persis (misal "kafe-teknik")
    filter_status : None = semua status, atau "DONE" / "CANCEL" / "ANTRE"
    maks_baris    : None = tidak dibatasi (HATI-HATI, insertion sort jadi
                    sangat lambat kalau subset masih puluhan ribu baris),
                    atau batasi jumlah baris yang diambil supaya tetap
                    responsif untuk demo (disarankan beberapa ratus - 2000)
    """
    hasil = []
    n = len(struktur)
    i = 0
    while i < n:
        p = struktur.get(i)

        cocok = True
        if filter_resto is not None and p.resto != filter_resto:
            cocok = False
        if filter_status is not None and p.status != filter_status:
            cocok = False

        if cocok:
            hasil.append(p)
            if maks_baris is not None and len(hasil) >= maks_baris:
                break
        i += 1

    return hasil


def buat_laporan(struktur, kunci, filter_resto=None, filter_status=None, maks_baris=1000):
    """
    Gabungan: ambil subset sesuai filter, lalu urutkan dengan insertion_sort
    berdasarkan `kunci`. Mengembalikan list Pesanan yang sudah terurut.
    """
    subset = ambil_subset(struktur, filter_resto, filter_status, maks_baris)
    insertion_sort(subset, kunci)
    return subset


def cari_di_laporan(laporan_terurut, kunci, nilai_target):
    """Bungkus binary_search supaya nama fungsinya jelas dipakai untuk apa."""
    return binary_search(laporan_terurut, kunci, nilai_target)


if __name__ == "__main__":
    import os
    import sys
    import time

    sys.path.insert(0, os.path.dirname(__file__))
    from m1_pesanan import load_pesanan_csv

    path_csv = os.path.join(os.path.dirname(__file__), "..", "data", "pesanan.csv")
    print("Load data penuh (200.000 baris) ke Array...")
    arr, ll, jumlah = load_pesanan_csv(path_csv)
    print("Selesai load {} baris.\n".format(jumlah))

    print("=== Buat laporan: resto=kafe-teknik, urutkan berdasarkan harga ===")
    t0 = time.perf_counter()
    laporan = buat_laporan(arr, kunci="harga", filter_resto="kafe-teknik", maks_baris=1000)
    t1 = time.perf_counter()
    print("Subset diambil & diurutkan: {} baris dalam {:.2f} ms".format(len(laporan), (t1 - t0) * 1000))

    print("\n10 pesanan termurah di kafe-teknik (dari subset 1000 baris):")
    i = 0
    while i < 10 and i < len(laporan):
        print(" -", laporan[i])
        i += 1

    print("\n=== Cari pesanan dengan harga 15000 di laporan ===")
    t0 = time.perf_counter()
    idx = cari_di_laporan(laporan, kunci="harga", nilai_target=15000)
    t1 = time.perf_counter()
    if idx == -1:
        print("Tidak ditemukan pesanan dengan harga 15000 (waktu cari: {:.4f} ms)".format((t1 - t0) * 1000))
    else:
        print("Ditemukan di index", idx, ":", laporan[idx], "(waktu cari: {:.4f} ms)".format((t1 - t0) * 1000))

    print("\n=== Perbandingan: insertion sort pada subset lebih besar (5000 baris, semua resto) ===")
    t0 = time.perf_counter()
    laporan_besar = buat_laporan(arr, kunci="t_masuk_detik", maks_baris=5000)
    t1 = time.perf_counter()
    print("5000 baris diurutkan dalam {:.2f} ms (lihat bedanya kalau maks_baris makin besar -> O(n^2))".format((t1 - t0) * 1000))
