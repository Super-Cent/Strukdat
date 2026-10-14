"""
M3: Laporan Terurut - Insertion Sort, Merge Sort, Binary Search, & Linear Search
Proyek 2EZ4U APP - Struktur Data & Analisa Algoritma (EC234303)

CATATAN: Tidak menggunakan instant function (dict, set, sorted, .sort(),
heapq, bisect, collections.*, literal {}, comprehension dict/set).
"""


def insertion_sort(larik, kunci):
    """Urutkan larik (list of Pesanan) menurut atribut `kunci`, menaik (ascending), IN-PLACE. O(n^2)."""
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


def merge_sort(larik, kunci):
    """Urutkan larik (list of Pesanan) menurut atribut `kunci` dengan Merge Sort. O(n log n)."""
    if len(larik) <= 1:
        return larik

    mid = len(larik) // 2
    kiri = merge_sort(larik[:mid], kunci)
    kanan = merge_sort(larik[mid:], kunci)

    hasil = []
    i = j = 0

    while i < len(kiri) and j < len(kanan):
        if getattr(kiri[i], kunci) <= getattr(kanan[j], kunci):
            hasil.append(kiri[i])
            i += 1
        else:
            hasil.append(kanan[j])
            j += 1

    while i < len(kiri):
        hasil.append(kiri[i])
        i += 1

    while j < len(kanan):
        hasil.append(kanan[j])
        j += 1

    return hasil


def binary_search_oid(larik_terurut, target_oid):
    """
    Cari index elemen berdasarkan `oid` di larik yang SUDAH TERURUT menaik berdasarkan `oid`.
    Kompleksitas: O(log n).
    """
    lo = 0
    hi = len(larik_terurut) - 1

    while lo <= hi:
        mid = (lo + hi) // 2
        oid_mid = getattr(larik_terurut[mid], 'oid')

        if oid_mid == target_oid:
            return mid
        elif oid_mid < target_oid:
            lo = mid + 1
        else:
            hi = mid - 1

    return -1


def linear_search_oid(larik, target_oid):
    """
    Cari index elemen berdasarkan `oid` menggunakan Linear Search (bisa untuk larik acak/belum terurut).
    Kompleksitas: O(n).
    """
    i = 0
    n = len(larik)
    while i < n:
        if getattr(larik[i], 'oid') == target_oid:
            return i
        i += 1
    return -1


def ambil_subset(struktur, filter_resto=None, filter_status=None, maks_baris=None):
    """Filter data M1 ke dalam list Python biasa sebelum di-sort."""
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


def buat_laporan(struktur, kunci, filter_resto=None, filter_status=None, maks_baris=1000, metode_sort="insertion"):
    """Gabungkan filter subset + pengurutan (insertion / merge)."""
    subset = ambil_subset(struktur, filter_resto, filter_status, maks_baris)
    if metode_sort == "merge":
        return merge_sort(subset, kunci)
    else:
        insertion_sort(subset, kunci)
        return subset


def cari_di_laporan_oid(laporan, target_oid, metode_search="binary"):
    """Pencarian spesifik berdasarkan oid pada laporan (binary / linear)."""
    if metode_search == "binary":
        return binary_search_oid(laporan, target_oid)
    else:
        return linear_search_oid(laporan, target_oid)


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

    print("=== Uji Buat Laporan Terurut oid (Merge Sort 1000 baris) ===")
    t0 = time.perf_counter()
    laporan_oid = buat_laporan(arr, kunci="oid", maks_baris=1000, metode_sort="merge")
    t1 = time.perf_counter()
    print("Merge Sort (oid) selesai dalam {:.2f} ms".format((t1 - t0) * 1000))

    print("\n=== Uji Pencarian oid = 'O-000001' ===")
    t0 = time.perf_counter()
    idx = cari_di_laporan_oid(laporan_oid, "O-000001", metode_search="binary")
    t1 = time.perf_counter()
    print("Binary Search: Index {} (waktu: {:.4f} ms)".format(idx, (t1 - t0) * 1000))