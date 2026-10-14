import csv

class Pesanan:
    def __init__(self, oid, pelanggan, resto, menu_makanan, harga, prioritas, t_masuk_detik, t_selesai_detik, status):
        self.oid = oid
        self.pelanggan = pelanggan
        self.resto = resto
        self.menu_makanan = menu_makanan
        self.harga = int(harga) if harga else 0
        self.prioritas = int(prioritas) if prioritas else 3
        self.t_masuk_detik = int(t_masuk_detik) if t_masuk_detik else 0
        self.t_selesai_detik = int(t_selesai_detik) if t_selesai_detik else 0
        self.status = status

    def __repr__(self):
        return f"Pesanan({self.oid}, {self.pelanggan}, {self.resto}, {self.menu_makanan}, Rp{self.harga}, P{self.prioritas}, {self.status})"


class Array:
    def __init__(self, kapasitas=10):
        self.kapasitas = kapasitas
        self.data = [None] * kapasitas
        self.size = 0

    def _resize(self, new_cap):
        baru = [None] * new_cap
        for i in range(self.size):
            baru[i] = self.data[i]
        self.data = baru
        self.kapasitas = new_cap

    def append(self, pesanan):
        if self.size == self.kapasitas:
            self._resize(self.kapasitas * 2)
        self.data[self.size] = pesanan
        self.size += 1
        return self.size - 1

    def insert(self, index, pesanan):
        if index < 0 or index > self.size:
            index = self.size
        if self.size == self.kapasitas:
            self._resize(self.kapasitas * 2)
        for i in range(self.size, index, -1):
            self.data[i] = self.data[i - 1]
        self.data[index] = pesanan
        self.size += 1
        return index

    def get(self, index):
        if index < 0 or index >= self.size:
            raise IndexError("Indeks Array di luar jangkauan")
        return self.data[index]

    def hapus(self, index):
        if index < 0 or index >= self.size:
            raise IndexError("Indeks Array di luar jangkauan")
        terhapus = self.data[index]
        for i in range(index, self.size - 1):
            self.data[i] = self.data[i + 1]
        self.data[self.size - 1] = None
        self.size -= 1
        return terhapus

    def tambah_reguler(self, pesanan):
        return self.append(pesanan)

    def tambah_vip(self, pesanan):
        return self.insert(0, pesanan)

    def tambah_prioritas(self, pesanan):
        # Cari posisi penyisipan setelah VIP/Prioritas
        idx = 0
        while idx < self.size and self.data[idx].prioritas <= 2:
            idx += 1
        return self.insert(idx, pesanan)

    def __len__(self):
        return self.size


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def append(self, pesanan):
        node_baru = Node(pesanan)
        if self.head is None:
            self.head = node_baru
            self.tail = node_baru
        else:
            self.tail.next = node_baru
            self.tail = node_baru
        self.size += 1
        return self.size - 1

    def insert(self, index, pesanan):
        if index <= 0 or self.head is None:
            node_baru = Node(pesanan)
            node_baru.next = self.head
            self.head = node_baru
            if self.tail is None:
                self.tail = node_baru
            self.size += 1
            return 0

        if index >= self.size:
            return self.append(pesanan)

        curr = self.head
        for _ in range(index - 1):
            curr = curr.next

        node_baru = Node(pesanan)
        node_baru.next = curr.next
        curr.next = node_baru
        self.size += 1
        return index

    def get(self, index):
        if index < 0 or index >= self.size:
            raise IndexError("Indeks LinkedList di luar jangkauan")
        curr = self.head
        for _ in range(index):
            curr = curr.next
        return curr.data

    def hapus(self, index):
        if index < 0 or index >= self.size or self.head is None:
            raise IndexError("Indeks LinkedList di luar jangkauan")

        if index == 0:
            terhapus = self.head.data
            self.head = self.head.next
            if self.head is None:
                self.tail = None
            self.size -= 1
            return terhapus

        curr = self.head
        for _ in range(index - 1):
            curr = curr.next

        terhapus = curr.next.data
        curr.next = curr.next.next
        if curr.next is None:
            self.tail = curr
        self.size -= 1
        return terhapus

    def tambah_reguler(self, pesanan):
        return self.append(pesanan)

    def tambah_vip(self, pesanan):
        return self.insert(0, pesanan)

    def tambah_prioritas(self, pesanan):
        if self.head is None:
            return self.append(pesanan)

        idx = 0
        curr = self.head
        while curr is not None and curr.data.prioritas <= 2:
            idx += 1
            curr = curr.next
        return self.insert(idx, pesanan)

    def __len__(self):
        return self.size


def load_pesanan_csv(path_csv):
    arr = Array()
    ll = LinkList()
    count = 0

    with open(path_csv, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            p = Pesanan(
                row.get('oid', ''),
                row.get('pelanggan', ''),
                row.get('resto', ''),
                row.get('menu', ''),
                row.get('harga', 0),
                row.get('prioritas', 3),
                row.get('t_masuk_detik', 0),
                row.get('t_selesai_detik', 0),
                row.get('status', 'ANTRE')
            )
            arr.append(p)
            ll.append(p)
            count += 1

    return arr, ll, count