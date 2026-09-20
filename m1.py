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
 
    def __len__(self):
        return self.size
 
 
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
 
    print()
    print("=== Test LinkList ===")
    ll = LinkList()
    for oid in ["O-000001", "O-000002", "O-000003", "O-000004", "O-000005"]:
        ll.append(oid)
    print("Ukuran:", len(ll))
    print("get(0):", ll.get(0))
    print("get(4):", ll.get(4))
 