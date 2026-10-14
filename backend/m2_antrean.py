import time


class AntreanMelingkar:

    def __init__(self, capacity=8):
        if capacity < 1:
            capacity = 1
        self.capacity = capacity
        self.data = [None] * self.capacity
        self.head = 0    # index elemen paling depan (keluar duluan)
        self.tail = 0    # index slot kosong berikutnya untuk enqueue
        self.count = 0   # jumlah elemen yang sedang ada di antrean

    def _resize(self, new_capacity):
        new_data = [None] * new_capacity
        i = 0
        idx = self.head
        while i < self.count:
            new_data[i] = self.data[idx]
            idx = (idx + 1) % self.capacity
            i += 1
        self.data = new_data
        self.capacity = new_capacity
        self.head = 0
        self.tail = self.count

    def enqueue(self, v):
        if self.count == self.capacity:
            self._resize(self.capacity * 2)
        self.data[self.tail] = v
        self.tail = (self.tail + 1) % self.capacity
        self.count += 1

    def dequeue(self):
        if self.count == 0:
            raise IndexError("antrean kosong, tidak ada yang bisa di-dequeue")
        v = self.data[self.head]
        self.data[self.head] = None  # bersihkan slot biar tidak "nyangkut"
        self.head = (self.head + 1) % self.capacity
        self.count -= 1
        return v

    def peek(self):
        if self.count == 0:
            raise IndexError("antrean kosong")
        return self.data[self.head]

    def is_empty(self):
        return self.count == 0

    def __len__(self):
        return self.count


class Stack:

    def __init__(self, capacity=8):
        if capacity < 1:
            capacity = 1
        self.capacity = capacity
        self.data = [None] * self.capacity
        self.size = 0

    def _resize(self, new_capacity):
        new_data = [None] * new_capacity
        i = 0
        while i < self.size:
            new_data[i] = self.data[i]
            i += 1
        self.data = new_data
        self.capacity = new_capacity

    def push(self, v):
        if self.size == self.capacity:
            self._resize(self.capacity * 2)
        self.data[self.size] = v
        self.size += 1

    def pop(self):
        if self.size == 0:
            raise IndexError("stack kosong, tidak ada yang bisa di-pop")
        self.size -= 1
        v = self.data[self.size]
        self.data[self.size] = None
        return v

    def peek(self):
        if self.size == 0:
            raise IndexError("stack kosong")
        return self.data[self.size - 1]

    def is_empty(self):
        return self.size == 0

    def __len__(self):
        return self.size


class AksiHistori:

    def __init__(self, tipe, index, pesanan):
        self.tipe = tipe
        self.index = index
        self.pesanan = pesanan

    def __repr__(self):
        return "AksiHistori({}, index={}, {})".format(self.tipe, self.index, self.pesanan)


class ManajerUndo:

    def __init__(self, struktur):
        self.struktur = struktur
        self.histori = Stack()

    def tambah_reguler(self, pesanan):
        self.struktur.append(pesanan)
        idx = len(self.struktur) - 1
        self.histori.push(AksiHistori("TAMBAH_REGULER", idx, pesanan))

    def tambah_prioritas(self, pesanan):
        idx = len(self.struktur) // 2
        self.struktur.insert_priority(pesanan)
        self.histori.push(AksiHistori("TAMBAH_PRIORITAS", idx, pesanan))

    def tambah_vip(self, pesanan):
        self.struktur.insert_vip(pesanan)
        self.histori.push(AksiHistori("TAMBAH_VIP", 0, pesanan))

    def hapus(self, index):
        pesanan = self.struktur.hapus(index)
        self.histori.push(AksiHistori("HAPUS", index, pesanan))
        return pesanan

    def bisa_undo(self):
        return not self.histori.is_empty()

    def undo(self):

        if self.histori.is_empty():
            raise IndexError("tidak ada aksi untuk di-undo")

        aksi = self.histori.pop()

        if aksi.tipe == "TAMBAH_REGULER" or aksi.tipe == "TAMBAH_PRIORITAS" or aksi.tipe == "TAMBAH_VIP":
            self.struktur.hapus(aksi.index)
        elif aksi.tipe == "HAPUS":
            self.struktur.sisip_di(aksi.index, aksi.pesanan)

        return aksi


class ManajerPesananGabungan:
    def __init__(self, arr, ll):
        self.arr = arr
        self.ll = ll
        self.histori = Stack()

    def tambah_reguler(self, pesanan):
        t0 = time.perf_counter()
        self.arr.append(pesanan)
        t1 = time.perf_counter()
        self.ll.append(pesanan)
        t2 = time.perf_counter()

        idx = len(self.arr) - 1
        self.histori.push(AksiHistori("TAMBAH_REGULER", idx, pesanan))
        return idx, (t1 - t0) * 1000, (t2 - t1) * 1000

    def tambah_prioritas(self, pesanan):
        idx = len(self.arr) // 2

        t0 = time.perf_counter()
        self.arr.insert_priority(pesanan)
        t1 = time.perf_counter()
        self.ll.insert_priority(pesanan)
        t2 = time.perf_counter()

        self.histori.push(AksiHistori("TAMBAH_PRIORITAS", idx, pesanan))
        return idx, (t1 - t0) * 1000, (t2 - t1) * 1000

    def tambah_vip(self, pesanan):
        t0 = time.perf_counter()
        self.arr.insert_vip(pesanan)
        t1 = time.perf_counter()
        self.ll.insert_vip(pesanan)
        t2 = time.perf_counter()

        self.histori.push(AksiHistori("TAMBAH_VIP", 0, pesanan))
        return 0, (t1 - t0) * 1000, (t2 - t1) * 1000

    def hapus(self, idx):
        t0 = time.perf_counter()
        pesanan = self.arr.hapus(idx)
        t1 = time.perf_counter()
        self.ll.hapus(idx)
        t2 = time.perf_counter()

        self.histori.push(AksiHistori("HAPUS", idx, pesanan))
        return pesanan, (t1 - t0) * 1000, (t2 - t1) * 1000

    def bisa_undo(self):
        return not self.histori.is_empty()

    def undo(self):
        """
        Balikkan aksi terakhir di KEDUA struktur sekaligus, supaya
        Array dan LinkList tetap sinkron setelah di-undo.
        """
        if self.histori.is_empty():
            raise IndexError("tidak ada aksi untuk di-undo")

        aksi = self.histori.pop()

        if aksi.tipe == "TAMBAH_REGULER" or aksi.tipe == "TAMBAH_PRIORITAS" or aksi.tipe == "TAMBAH_VIP":
            self.arr.hapus(aksi.index)
            self.ll.hapus(aksi.index)
        elif aksi.tipe == "HAPUS":
            self.arr.sisip_di(aksi.index, aksi.pesanan)
            self.ll.sisip_di(aksi.index, aksi.pesanan)

        return aksi


def _isi_ke_list(struktur):
    """Helper hanya untuk keperluan print di test (tanpa comprehension)."""
    hasil = []
    i = 0
    while i < len(struktur):
        hasil.append(struktur.get(i))
        i += 1
    return hasil


if __name__ == "__main__":
    print("=== Test AntreanMelingkar (circular queue) ===")
    antrean = AntreanMelingkar(capacity=3)  # kapasitas kecil biar wrap-around kelihatan

    antrean.enqueue("O-1")
    antrean.enqueue("O-2")
    antrean.enqueue("O-3")
    print("Setelah enqueue O-1, O-2, O-3 | isi (head->tail):", end=" ")
    print(antrean.data, "| head=", antrean.head, "tail=", antrean.tail, "count=", antrean.count)

    print("dequeue():", antrean.dequeue())  # keluarkan O-1, slot index-0 kosong lagi
    print("dequeue():", antrean.dequeue())  # keluarkan O-2

    # enqueue lagi -> harus WRAP AROUND, pakai slot kosong di awal buffer
    antrean.enqueue("O-4")
    antrean.enqueue("O-5")
    print("Setelah dequeue 2x lalu enqueue O-4, O-5 (wrap-around):")
    print("isi buffer mentah:", antrean.data, "| head=", antrean.head,
          "tail=", antrean.tail, "count=", antrean.count)
    print("Urutan FIFO yang benar harus O-3, O-4, O-5:")
    print("dequeue():", antrean.dequeue())
    print("dequeue():", antrean.dequeue())
    print("dequeue():", antrean.dequeue())

    print()
    print("=== Test Stack ===")
    stack = Stack()
    stack.push("aksi-1")
    stack.push("aksi-2")
    stack.push("aksi-3")
    print("pop():", stack.pop())  # harus "aksi-3" (LIFO)
    print("pop():", stack.pop())  # harus "aksi-2"

    print()
    print("=== Test ManajerUndo (terhubung ke Array dari M1) ===")
    import sys
    import os
    sys.path.insert(0, os.path.dirname(__file__))
    from m1_pesanan import Array, Pesanan  # noqa: E402  (import setelah path diatur)

    arr = Array()
    manajer = ManajerUndo(arr)

    p1 = Pesanan("O-100", "Budi", "kafe-teknik", "nasi-goreng", 15000, 3, 0, None, "ANTRE")
    p2 = Pesanan("O-101", "Siti", "kedai-kopi", "kopi-susu", 10000, 2, 0, None, "ANTRE")
    p3 = Pesanan("O-102", "Rahmi", "kafe-teknik", "roti-bakar", 12000, 1, 0, None, "ANTRE")

    manajer.tambah_reguler(p1)
    manajer.tambah_prioritas(p2)
    manajer.tambah_vip(p3)
    print("Setelah 3x tambah ->", _isi_ke_list(arr))

    manajer.hapus(1)
    print("Setelah hapus(1)  ->", _isi_ke_list(arr))

    aksi_dibatalkan = manajer.undo()
    print("Undo terakhir ({}) ->".format(aksi_dibatalkan.tipe), _isi_ke_list(arr))

    aksi_dibatalkan = manajer.undo()
    print("Undo terakhir ({}) ->".format(aksi_dibatalkan.tipe), _isi_ke_list(arr))