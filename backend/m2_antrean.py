"""
M2: Stack & Queue
Proyek 2EZ4U APP - Struktur Data & Analisa Algoritma (EC234303)
"""

class Stack:
    def __init__(self):
        self.data = []

    def push(self, x):
        self.data.append(x)

    def pop(self):
        if self.is_empty():
            raise IndexError("Stack kosong")
        return self.data.pop()

    def peek(self):
        if self.is_empty():
            return None
        return self.data[-1]

    def is_empty(self):
        return len(self.data) == 0

    def clear(self):
        self.data = []

    def __len__(self):
        return len(self.data)


# ==========================================
# 1. POSTFIX & KASIR (STACK OPERATOR & ANGKA)
# ==========================================
def presedensi(op):
    if op in ('+', '-'):
        return 1
    if op in ('*', '/'):
        return 2
    return 0

def ke_postfix(ekspresi):
    tokens = ekspresi.split()
    output = []
    s = Stack()

    for token in tokens:
        if token.isdigit():
            output.append(token)
        elif token in ('+', '-', '*', '/'):
            while (not s.is_empty()) and presedensi(s.peek()) >= presedensi(token):
                output.append(s.pop())
            s.push(token)
        elif token == '(':
            s.push(token)
        elif token == ')':
            while (not s.is_empty()) and s.peek() != '(':
                output.append(s.pop())
            if not s.is_empty() and s.peek() == '(':
                s.pop()

    while not s.is_empty():
        output.append(s.pop())

    return " ".join(output)

def hitung(postfix_expr):
    tokens = postfix_expr.split()
    s = Stack()

    for token in tokens:
        if token.isdigit():
            s.push(int(token))
        elif token in ('+', '-', '*', '/'):
            b = s.pop()
            a = s.pop()
            if token == '+':
                res = a + b
            elif token == '-':
                res = a - b
            elif token == '*':
                res = a * b
            elif token == '/':
                res = a // b if b != 0 else 0
            s.push(res)

    return s.pop() if not s.is_empty() else 0


# ==========================================
# 2. QUEUE DEQUEUE NAIF VS MELINGKAR
# ==========================================
class AntreanNaif:
    def __init__(self):
        self.data = []

    def enqueue(self, x):
        self.data.append(x)

    def dequeue(self):
        """Metode dequeue tunggal O(n)."""
        if len(self.data) == 0:
            raise IndexError("Antrean kosong")
        return self.data.pop(0)

    def dequeue_banyak(self, k=1):
        """Dequeue k elemen sekaligus dan hitung total pergeseran memori."""
        if len(self.data) < k:
            k = len(self.data)
        if k == 0:
            return [], 0

        terkeluar = []
        total_digeser = 0

        for _ in range(k):
            item = self.data.pop(0)
            terkeluar.append(item)
            total_digeser += len(self.data)

        return terkeluar, total_digeser

    def __len__(self):
        return len(self.data)


class AntreanMelingkar:
    def __init__(self, kapasitas=200000):
        self.kapasitas = kapasitas
        self.data = [None] * kapasitas
        self.head = 0
        self.tail = 0
        self.size = 0

    def enqueue(self, x):
        if self.size == self.kapasitas:
            baru = [None] * (self.kapasitas * 2)
            for i in range(self.size):
                baru[i] = self.data[(self.head + i) % self.kapasitas]
            self.data = baru
            self.head = 0
            self.tail = self.size
            self.kapasitas *= 2

        self.data[self.tail] = x
        self.tail = (self.tail + 1) % self.kapasitas
        self.size += 1

    def dequeue(self):
        """Metode dequeue tunggal O(1)."""
        if self.size == 0:
            raise IndexError("Antrean kosong")
        item = self.data[self.head]
        self.data[self.head] = None
        self.head = (self.head + 1) % self.kapasitas
        self.size -= 1
        return item

    def dequeue_banyak(self, k=1):
        """Dequeue k elemen. Pergeseran elemen selalu 0."""
        if self.size < k:
            k = self.size
        if k == 0:
            return [], 0

        terkeluar = []
        for _ in range(k):
            item = self.data[self.head]
            self.data[self.head] = None
            self.head = (self.head + 1) % self.kapasitas
            self.size -= 1
            terkeluar.append(item)

        return terkeluar, 0

    def kembalikan_ke_depan(self, list_item):
        for item in reversed(list_item):
            self.head = (self.head - 1 + self.kapasitas) % self.kapasitas
            self.data[self.head] = item
            self.size += 1

    def __len__(self):
        return self.size


# ==========================================
# 3. MANAJER DENGAN UNDO & REDO
# ==========================================
class AksiHistori:
    def __init__(self, jenis, data, index=None):
        self.jenis = jenis
        self.data = data
        self.index = index

    def __repr__(self):
        return f"AksiHistori({self.jenis})"


class ManajerPesananGabungan:
    def __init__(self, arr, ll):
        self.arr = arr
        self.ll = ll
        self.stack_undo = Stack()
        self.stack_redo = Stack()

    def tambah_reguler(self, pesanan):
        idx = self.arr.tambah_reguler(pesanan)
        self.ll.tambah_reguler(pesanan)
        self.stack_undo.push(AksiHistori("TAMBAH_REGULER", pesanan, idx))
        self.stack_redo.clear()
        return idx

    def tambah_prioritas(self, pesanan):
        idx = self.arr.tambah_prioritas(pesanan)
        self.ll.tambah_prioritas(pesanan)
        self.stack_undo.push(AksiHistori("TAMBAH_PRIORITAS", pesanan, idx))
        self.stack_redo.clear()
        return idx

    def tambah_vip(self, pesanan):
        idx = self.arr.tambah_vip(pesanan)
        self.ll.tambah_vip(pesanan)
        self.stack_undo.push(AksiHistori("TAMBAH_VIP", pesanan, idx))
        self.stack_redo.clear()
        return idx

    def hapus(self, index):
        p_arr = self.arr.hapus(index)
        self.ll.hapus(index)
        self.stack_undo.push(AksiHistori("HAPUS", p_arr, index))
        self.stack_redo.clear()
        return p_arr

    def catat_dequeue(self, list_terkeluar):
        self.stack_undo.push(AksiHistori("DEQUEUE", list_terkeluar))
        self.stack_redo.clear()

    def undo_last(self, antrean_circular=None):
        if self.stack_undo.is_empty():
            raise IndexError("Tumpukan undo kosong, tidak ada aksi untuk dibatalkan")

        aksi = self.stack_undo.pop()

        if aksi.jenis == "DEQUEUE":
            if antrean_circular is not None:
                antrean_circular.kembalikan_ke_depan(aksi.data)
            pesan = f"{len(aksi.data)} pesanan dikembalikan ke DEPAN antrean circular"
        
        elif aksi.jenis.startswith("TAMBAH"):
            self.arr.hapus(aksi.index)
            self.ll.hapus(aksi.index)
            pesan = f"Penambahan pesanan '{getattr(aksi.data, 'oid', '-')}' dibatalkan (dihapus dari M1)"
        
        elif aksi.jenis == "HAPUS":
            self.arr.insert(aksi.index, aksi.data)
            self.ll.insert(aksi.index, aksi.data)
            pesan = f"Penghapusan pesanan '{getattr(aksi.data, 'oid', '-')}' dibatalkan (dikembalikan ke M1)"

        self.stack_redo.push(aksi)
        return pesan

    def redo_last(self, antrean_circular=None):
        if self.stack_redo.is_empty():
            raise IndexError("Tumpukan redo kosong, tidak ada aksi untuk diulang")

        aksi = self.stack_redo.pop()

        if aksi.jenis == "DEQUEUE":
            if antrean_circular is not None:
                antrean_circular.dequeue_banyak(len(aksi.data))
            pesan = f"{len(aksi.data)} pesanan keluar lagi dari antrean circular"

        elif aksi.jenis == "TAMBAH_REGULER":
            self.arr.tambah_reguler(aksi.data)
            self.ll.tambah_reguler(aksi.data)
            pesan = f"Mengerjakan ulang penambahan pesanan reguler '{getattr(aksi.data, 'oid', '-')}'"

        elif aksi.jenis == "TAMBAH_PRIORITAS":
            self.arr.tambah_prioritas(aksi.data)
            self.ll.tambah_prioritas(aksi.data)
            pesan = f"Mengerjakan ulang penambahan pesanan prioritas '{getattr(aksi.data, 'oid', '-')}'"

        elif aksi.jenis == "TAMBAH_VIP":
            self.arr.tambah_vip(aksi.data)
            self.ll.tambah_vip(aksi.data)
            pesan = f"Mengerjakan ulang penambahan pesanan VIP '{getattr(aksi.data, 'oid', '-')}'"

        elif aksi.jenis == "HAPUS":
            self.arr.hapus(aksi.index)
            self.ll.hapus(aksi.index)
            pesan = f"Mengerjakan ulang penghapusan pesanan pada indeks {aksi.index}"

        self.stack_undo.push(aksi)
        return pesan