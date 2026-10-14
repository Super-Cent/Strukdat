def insertion_sort(larik, kunci):

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
    subset = ambil_subset(struktur, filter_resto, filter_status, maks_baris)
    insertion_sort(subset, kunci)
    return subset


def cari_di_laporan(laporan_terurut, kunci, nilai_target):
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