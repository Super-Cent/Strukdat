import csv
import time


class Array:

    def __init__(self, capacity=4):
        if capacity < 1:
            capacity = 1
        self.capacity = capacity
        self.size = 0
        # petak memori awal, diisi None dulu sebagai slot kosong
        self.data = [None] * self.capacity

    def _resize(self, new_capacity):
        new_data = [None] * new_capacity
        i = 0
        while i < self.size:
            new_data[i] = self.data[i]
            i += 1
        self.data = new_data
        self.capacity = new_capacity

    def append(self, v):
        if self.size == self.capacity:
            self._resize(self.capacity * 2)
        self.data[self.size] = v
        self.size += 1

    def get(self, i):
        if i < 0 or i >= self.size:
            raise IndexError(
                "index {} di luar jangkauan (ukuran saat ini: {})".format(i, self.size)
            )
        return self.data[i]

    def _insert_at(self, idx, v):
        if self.size == self.capacity:
            self._resize(self.capacity * 2)
        j = self.size
        while j > idx:
            self.data[j] = self.data[j - 1]
            j -= 1
        self.data[idx] = v
        self.size += 1

    def insert_priority(self, v):
        idx = self.size // 2
        self._insert_at(idx, v)

    def insert_vip(self, v):
        self._insert_at(0, v)

    def sisip_di(self, idx, v):
        if idx < 0 or idx > self.size:
            raise IndexError(
                "index {} di luar jangkauan sisip (ukuran saat ini: {})".format(idx, self.size)
            )
        self._insert_at(idx, v)

    def hapus(self, i):
        if i < 0 or i >= self.size:
            raise IndexError(
                "index {} di luar jangkauan (ukuran saat ini: {})".format(i, self.size)
            )
        removed = self.data[i]
        j = i
        while j < self.size - 1:
            self.data[j] = self.data[j + 1]
            j += 1
        self.data[self.size - 1] = None  # bersihkan slot terakhir yang jadi duplikat
        self.size -= 1
        return removed

    def __len__(self):
        return self.size


class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class LinkList:

    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def append(self, v):
        node = Node(v)
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self.size += 1

    def get(self, i):
        if i < 0 or i >= self.size:
            raise IndexError(
                "index {} di luar jangkauan (ukuran saat ini: {})".format(i, self.size)
            )
        current = self.head
        langkah = 0
        while langkah < i:
            current = current.next
            langkah += 1
        return current.value

    def _insert_at(self, idx, v):
        node = Node(v)
        if idx == 0:
            node.next = self.head
            self.head = node
            if self.tail is None:  # list sebelumnya kosong
                self.tail = node
        else:
            prev = self.head
            langkah = 0
            while langkah < idx - 1:
                prev = prev.next
                langkah += 1
            node.next = prev.next
            prev.next = node
            if node.next is None:  # ternyata disisip di posisi paling akhir
                self.tail = node
        self.size += 1

    def insert_priority(self, v):
        """Tambah PRIORITAS: menyerobot ke tengah barisan. O(n) karena menelusuri."""
        idx = self.size // 2
        self._insert_at(idx, v)

    def insert_vip(self, v):
        self._insert_at(0, v)

    def sisip_di(self, idx, v):
        if idx < 0 or idx > self.size:
            raise IndexError(
                "index {} di luar jangkauan sisip (ukuran saat ini: {})".format(idx, self.size)
            )
        self._insert_at(idx, v)

    def hapus(self, i):
        if i < 0 or i >= self.size:
            raise IndexError(
                "index {} di luar jangkauan (ukuran saat ini: {})".format(i, self.size)
            )
        if i == 0:
            removed = self.head
            self.head = self.head.next
            if self.head is None:  # list jadi kosong setelah dihapus
                self.tail = None
        else:
            prev = self.head
            langkah = 0
            while langkah < i - 1:
                prev = prev.next
                langkah += 1
            removed = prev.next
            prev.next = removed.next
            if removed.next is None:  # yang dihapus adalah elemen terakhir
                self.tail = prev
        self.size -= 1
        return removed.value

    def __len__(self):
        return self.size


class Pesanan:

    __slots__ = (
        "oid", "pelanggan", "resto", "menu", "harga", "prioritas",
        "t_masuk_detik", "t_selesai_detik", "status",
    )

    def __init__(self, oid, pelanggan, resto, menu, harga, prioritas,
                 t_masuk_detik, t_selesai_detik, status):
        self.oid = oid
        self.pelanggan = pelanggan
        self.resto = resto
        self.menu = menu
        self.harga = harga
        self.prioritas = prioritas
        self.t_masuk_detik = t_masuk_detik
        self.t_selesai_detik = t_selesai_detik
        self.status = status

    def __repr__(self):
        return "Pesanan({}, {}, {}, prioritas={})".format(
            self.oid, self.pelanggan, self.menu, self.prioritas
        )


def load_pesanan_csv(path, limit=None):

    arr = Array(capacity=4)
    ll = LinkList()
    jumlah = 0

    with open(path, "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        next(reader)  # lewati baris header

        for baris in reader:
            if limit is not None and jumlah >= limit:
                break

            oid = baris[0]
            pelanggan = baris[1]
            resto = baris[2]
            menu = baris[3]
            harga = int(baris[4])
            prioritas = int(baris[5])
            t_masuk = int(baris[6])
            t_selesai = int(baris[7]) if baris[7] != "" else None
            status = baris[8]

            p = Pesanan(oid, pelanggan, resto, menu, harga, prioritas,
                        t_masuk, t_selesai, status)
            arr.append(p)
            ll.append(p)
            jumlah += 1

    return arr, ll, jumlah


def benchmark(arr, ll):
    hasil = []
    n = len(arr)
    idx_tengah = n // 2

    # --- Lihat pesanan ke-i (akses di tengah data) ---
    t0 = time.perf_counter(); arr.get(idx_tengah); t1 = time.perf_counter()
    hasil.append(("Lihat pesanan ke-i", "Array", (t1 - t0) * 1000))

    t0 = time.perf_counter(); ll.get(idx_tengah); t1 = time.perf_counter()
    hasil.append(("Lihat pesanan ke-i", "LinkList", (t1 - t0) * 1000))

    # --- Tambah REGULER (paling belakang) ---
    dummy_reg = Pesanan("O-BENCH-REG", "bench", "bench", "bench", 0, 3, 0, None, "ANTRE")
    t0 = time.perf_counter(); arr.append(dummy_reg); t1 = time.perf_counter()
    hasil.append(("Tambah REGULER", "Array", (t1 - t0) * 1000))

    t0 = time.perf_counter(); ll.append(dummy_reg); t1 = time.perf_counter()
    hasil.append(("Tambah REGULER", "LinkList", (t1 - t0) * 1000))

    # --- Tambah PRIORITAS (tengah) ---
    dummy_pri = Pesanan("O-BENCH-PRI", "bench", "bench", "bench", 0, 2, 0, None, "ANTRE")
    t0 = time.perf_counter(); arr.insert_priority(dummy_pri); t1 = time.perf_counter()
    hasil.append(("Tambah PRIORITAS", "Array", (t1 - t0) * 1000))

    t0 = time.perf_counter(); ll.insert_priority(dummy_pri); t1 = time.perf_counter()
    hasil.append(("Tambah PRIORITAS", "LinkList", (t1 - t0) * 1000))

    # --- Tambah VIP (depan) ---
    dummy_vip = Pesanan("O-BENCH-VIP", "bench", "bench", "bench", 0, 1, 0, None, "ANTRE")
    t0 = time.perf_counter(); arr.insert_vip(dummy_vip); t1 = time.perf_counter()
    hasil.append(("Tambah VIP", "Array", (t1 - t0) * 1000))

    t0 = time.perf_counter(); ll.insert_vip(dummy_vip); t1 = time.perf_counter()
    hasil.append(("Tambah VIP", "LinkList", (t1 - t0) * 1000))

    # --- Hapus pesanan ke-0 ---
    t0 = time.perf_counter(); arr.hapus(0); t1 = time.perf_counter()
    hasil.append(("Hapus pesanan ke-0", "Array", (t1 - t0) * 1000))

    t0 = time.perf_counter(); ll.hapus(0); t1 = time.perf_counter()
    hasil.append(("Hapus pesanan ke-0", "LinkList", (t1 - t0) * 1000))

    return hasil


def cetak_benchmark(hasil):
    print("{:<22} {:<10} {:>14}".format("Operasi", "Struktur", "Waktu (ms)"))
    print("-" * 48)
    i = 0
    while i < len(hasil):
        nama, struktur, waktu_ms = hasil[i]
        print("{:<22} {:<10} {:>14.4f}".format(nama, struktur, waktu_ms))
        i += 1


def _isi_ke_list(struktur):
    """Helper hanya untuk keperluan print di test (tanpa comprehension)."""
    hasil = []
    i = 0
    while i < len(struktur):
        hasil.append(struktur.get(i))
        i += 1
    return hasil


if __name__ == "__main__":
    # Sanity check kecil dengan data dummy sebelum nanti disambungkan
    # ke pesanan.csv (200.000 baris) dan UI Tkinter.
    print("=== Test Array ===")
    arr = Array(capacity=2)  # kapasitas kecil sengaja, biar resize kelihatan
    for oid in ["O-000001", "O-000002", "O-000003", "O-000004", "O-000005"]:
        arr.append(oid)
    print("Ukuran:", len(arr), "| Kapasitas internal:", arr.capacity)
    print("get(0):", arr.get(0))
    print("get(4):", arr.get(4))

    arr.insert_priority("O-PRIORITAS-1")
    print("Setelah insert_priority ->", _isi_ke_list(arr))

    arr.insert_vip("O-VIP-1")
    print("Setelah insert_vip      ->", _isi_ke_list(arr))

    dihapus = arr.hapus(0)
    print("hapus(0), yang terhapus:", dihapus)
    print("Setelah hapus(0)        ->", _isi_ke_list(arr))

    print()
    print("=== Test LinkList ===")
    ll = LinkList()
    for oid in ["O-000001", "O-000002", "O-000003", "O-000004", "O-000005"]:
        ll.append(oid)
    print("Ukuran:", len(ll))
    print("get(0):", ll.get(0))
    print("get(4):", ll.get(4))

    ll.insert_priority("O-PRIORITAS-1")
    print("Setelah insert_priority ->", _isi_ke_list(ll))

    ll.insert_vip("O-VIP-1")
    print("Setelah insert_vip      ->", _isi_ke_list(ll))

    dihapus = ll.hapus(0)
    print("hapus(0), yang terhapus:", dihapus)
    print("Setelah hapus(0)        ->", _isi_ke_list(ll))

    # ------------------------------------------------------------------
    # Step 7-8: load data CSV skala penuh (200.000 baris) & benchmark
    # ------------------------------------------------------------------
    print()
    print("=== Load data/pesanan.csv & Benchmark skala penuh ===")
    import os
    path_csv = os.path.join(os.path.dirname(__file__), "..", "data", "pesanan.csv")

    t0 = time.perf_counter()
    arr_full, ll_full, jumlah = load_pesanan_csv(path_csv)
    t1 = time.perf_counter()
    print("Berhasil load {} baris dalam {:.2f} ms".format(jumlah, (t1 - t0) * 1000))
    print()

    hasil_benchmark = benchmark(arr_full, ll_full)
    cetak_benchmark(hasil_benchmark)
