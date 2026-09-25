class Array:
    """
    Array dengan kapasitas dinamis (mirip cara kerja list/vector di balik layar).
    Saat penuh, kapasitas digandakan (2x) dan seluruh isi disalin manual.
    """
 
    def __init__(self, capacity=4):
        if capacity < 1:
            capacity = 1
        self.capacity = capacity
        self.size = 0
        # petak memori awal, diisi None dulu sebagai slot kosong
        self.data = [None] * self.capacity
 
    def _resize(self, new_capacity):
        """Alokasi petak baru berukuran new_capacity, salin isi lama satu-satu."""
        new_data = [None] * new_capacity
        i = 0
        while i < self.size:
            new_data[i] = self.data[i]
            i += 1
        self.data = new_data
        self.capacity = new_capacity
 
    def append(self, v):
        """
        Tambah elemen di akhir array.
        Amortized O(1): mahal (O(n)) hanya saat resize, yang jarang terjadi.
        """
        if self.size == self.capacity:
            self._resize(self.capacity * 2)
        self.data[self.size] = v
        self.size += 1
 
    def get(self, i):
        """Lihat pesanan ke-i. O(1) karena alamat memori bisa dihitung langsung."""
        if i < 0 or i >= self.size:
            raise IndexError(
                "index {} di luar jangkauan (ukuran saat ini: {})".format(i, self.size)
            )
        return self.data[i]
 
    def _insert_at(self, idx, v):
        """
        Sisip elemen di posisi idx. O(n) karena elemen dari idx sampai akhir
        harus digeser satu langkah ke kanan dulu supaya ada slot kosong.
        """
        if self.size == self.capacity:
            self._resize(self.capacity * 2)
        j = self.size
        while j > idx:
            self.data[j] = self.data[j - 1]
            j -= 1
        self.data[idx] = v
        self.size += 1
 
    def insert_priority(self, v):
        """Tambah PRIORITAS: menyerobot ke tengah barisan. O(n) karena geser."""
        idx = self.size // 2
        self._insert_at(idx, v)
 
    def insert_vip(self, v):
        """Tambah VIP: langsung ke urutan pertama. O(n), paling mahal di Array
        karena SEMUA elemen yang sudah ada harus digeser ke kanan."""
        self._insert_at(0, v)
 
    def hapus(self, i):
        """
        Hapus pesanan ke-i.
        O(n) karena elemen setelah i harus digeser satu langkah ke kiri
        untuk menutup lubang bekas elemen yang dihapus.
        """
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
    """Satu simpul dalam linked list: menyimpan nilai dan alamat simpul berikutnya."""
 
    def __init__(self, value):
        self.value = value
        self.next = None
 
 
class LinkList:
    """
    Linked list dengan pointer head dan tail.
    Pointer tail disimpan supaya append tetap O(1) tanpa perlu menelusuri
    seluruh list untuk mencari elemen terakhir.
    """
 
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
 
    def append(self, v):
        """Tambah elemen di akhir list. O(1) karena tail sudah diketahui."""
        node = Node(v)
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self.size += 1
 
    def get(self, i):
        """
        Lihat pesanan ke-i.
        O(n) karena harus menelusuri dari head sebanyak i langkah
        (tidak ada alamat yang bisa dihitung langsung seperti pada array).
        """
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
        """
        Sisip elemen di posisi idx.
        O(1) kalau idx == 0 (langsung ubah head, tidak perlu menelusuri apa pun).
        O(n) untuk idx lain karena tetap harus menelusuri ke posisi idx-1 dulu.
        """
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
        """Tambah VIP: langsung ke urutan pertama. O(1), paling murah di LinkList
        karena cukup ubah satu pointer (head), tidak ada yang perlu digeser."""
        self._insert_at(0, v)
 
    def hapus(self, i):
        """
        Hapus pesanan ke-i.
        O(n) karena harus menelusuri dulu ke node sebelum posisi i
        untuk menyambungkan kembali rantainya (kecuali i == 0).
        """
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
