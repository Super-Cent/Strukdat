"""
frontend/ui.py - Jendela Tkinter untuk Proyek 2EZ4U APP
Menyambungkan tampilan ke backend M1 (Array/LinkList) dan M2 (Antrean/Undo).

Layout (sesuai contoh di PDF soal):
- Kiri   : daftar menu
- Kanan  : form parameter (atas) + hasil (bawah)
- Bawah  : panel COMMAND, mencatat tiap perintah + modul + waktu eksekusi
"""

import os
import sys
import time
import tkinter as tk
from tkinter import scrolledtext

# backend/ ada satu level di atas frontend/, tambahkan ke sys.path supaya bisa di-import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from m1_pesanan import Pesanan, load_pesanan_csv       # noqa: E402
from m2_antrean import AntreanMelingkar, ManajerPesananGabungan    # noqa: E402
from m3_laporan import buat_laporan, cari_di_laporan    # noqa: E402


# Daftar menu ditulis sebagai tuple literal (bukan dict), urutannya menentukan
# urutan tampil di Listbox kiri.
MENU_ITEMS = (
    "DATA - LOAD",
    "ARRAY - LIHAT PESANAN",
    "ARRAY - TAMBAH PESANAN REGULER",
    "ARRAY - TAMBAH PESANAN PRIORITAS",
    "ARRAY - TAMBAH PESANAN VIP",
    "ARRAY - HAPUS PESANAN",
    "LINKEDLIST - LIHAT PESANAN",
    "LINKEDLIST - TAMBAH PESANAN REGULER",
    "LINKEDLIST - TAMBAH PESANAN PRIORITAS",
    "LINKEDLIST - TAMBAH PESANAN VIP",
    "LINKEDLIST - HAPUS PESANAN",
    "ANTREAN - ISI (ENQUEUE)",
    "ANTREAN - LAYANI BERIKUTNYA (DEQUEUE)",
    "UNDO",
    "LAPORAN - BUAT (INSERTION SORT)",
    "LAPORAN - CARI (BINARY SEARCH)",
)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("2EZ4U Food Delivery")
        self.geometry("950x650")

        # --- state backend (belum ada data sampai menu DATA - LOAD dipilih) ---
        self.arr = None
        self.ll = None
        self.manager = None   # ManajerPesananGabungan: jaga arr & ll selalu sinkron
        self.antrean = AntreanMelingkar()

        self.laporan_terakhir = None   # list Pesanan hasil buat_laporan() terakhir
        self.laporan_kunci = None      # field yang dipakai untuk sort/cari laporan terakhir

        self.menu_aktif = None
        self.entries = []  # list of (label, Entry widget) untuk form yang sedang tampil

        self._bangun_layout()

    # ------------------------------------------------------------------
    # Pembangunan layout
    # ------------------------------------------------------------------
    def _bangun_layout(self):
        # --- kiri: daftar menu ---
        frame_kiri = tk.Frame(self, width=280)
        frame_kiri.pack(side="left", fill="y")
        frame_kiri.pack_propagate(False)

        tk.Label(frame_kiri, text="2EZ4U Food Delivery",
                 font=("Arial", 12, "bold")).pack(pady=8)

        self.listbox_menu = tk.Listbox(frame_kiri)
        self.listbox_menu.pack(fill="both", expand=True, padx=6, pady=6)
        i = 0
        while i < len(MENU_ITEMS):
            self.listbox_menu.insert("end", MENU_ITEMS[i])
            i += 1
        self.listbox_menu.bind("<<ListboxSelect>>", self._menu_dipilih)

        # --- kanan: form (atas) + hasil (tengah) ---
        frame_kanan = tk.Frame(self)
        frame_kanan.pack(side="left", fill="both", expand=True)

        self.label_judul_form = tk.Label(
            frame_kanan, text="Pilih menu di sebelah kiri", font=("Arial", 11, "bold")
        )
        self.label_judul_form.pack(anchor="w", padx=8, pady=(8, 0))

        self.frame_form = tk.Frame(frame_kanan)
        self.frame_form.pack(fill="x", padx=8, pady=4)

        tk.Label(frame_kanan, text="HASIL", font=("Arial", 9, "bold")).pack(anchor="w", padx=8)
        self.text_hasil = scrolledtext.ScrolledText(frame_kanan, height=16)
        self.text_hasil.pack(fill="both", expand=True, padx=8, pady=(0, 4))

        # --- bawah: command log ---
        tk.Label(self, text="COMMAND", font=("Arial", 9, "bold")).pack(anchor="w", padx=8)
        self.text_log = scrolledtext.ScrolledText(self, height=8)
        self.text_log.pack(fill="x", padx=8, pady=(0, 8))

    # ------------------------------------------------------------------
    # Helper UI kecil
    # ------------------------------------------------------------------
    def _log(self, aksi, modul, durasi_ms):
        baris = "{:<32} -> {:<20} {:>10.3f} ms\n".format(aksi, modul, durasi_ms)
        self.text_log.insert("end", baris)
        self.text_log.see("end")

    def _tampilkan_hasil(self, teks):
        self.text_hasil.delete("1.0", "end")
        self.text_hasil.insert("end", teks)

    def _bersihkan_form(self):
        for widget in self.frame_form.winfo_children():
            widget.destroy()
        self.entries = []

    def _tambah_input(self, label_teks):
        baris = tk.Frame(self.frame_form)
        baris.pack(fill="x", pady=2)
        tk.Label(baris, text=label_teks, width=18, anchor="w").pack(side="left")
        entry = tk.Entry(baris)
        entry.pack(side="left", fill="x", expand=True)
        self.entries.append((label_teks, entry))
        return entry

    def _ambil_input(self, label_teks):
        i = 0
        while i < len(self.entries):
            lbl, entry = self.entries[i]
            if lbl == label_teks:
                return entry.get()
            i += 1
        return ""

    def _cek_data_dimuat(self):
        if self.arr is None:
            self._tampilkan_hasil("Data belum dimuat. Pilih menu \"DATA - LOAD\" dulu.")
            return False
        return True

    # ------------------------------------------------------------------
    # Routing: menu dipilih -> bangun form yang sesuai
    # ------------------------------------------------------------------
    def _menu_dipilih(self, event):
        seleksi = self.listbox_menu.curselection()
        if len(seleksi) == 0:
            return
        menu = self.listbox_menu.get(seleksi[0])
        self.menu_aktif = menu
        self.label_judul_form.config(text=menu)
        self._bersihkan_form()

        if menu == "DATA - LOAD":
            tk.Button(self.frame_form, text="LOAD DATA", command=self._aksi_load).pack(pady=6)

        elif menu == "ARRAY - LIHAT PESANAN" or menu == "LINKEDLIST - LIHAT PESANAN":
            self._tambah_input("Index (0 = pesanan pertama)")
            tk.Button(self.frame_form, text="LIHAT", command=self._aksi_lihat).pack(pady=6)

        elif (menu == "ARRAY - TAMBAH PESANAN REGULER"
              or menu == "ARRAY - TAMBAH PESANAN PRIORITAS"
              or menu == "ARRAY - TAMBAH PESANAN VIP"
              or menu == "LINKEDLIST - TAMBAH PESANAN REGULER"
              or menu == "LINKEDLIST - TAMBAH PESANAN PRIORITAS"
              or menu == "LINKEDLIST - TAMBAH PESANAN VIP"):
            self._tambah_input("Nama pelanggan")
            self._tambah_input("Resto")
            self._tambah_input("Menu")
            self._tambah_input("Harga")
            tk.Button(self.frame_form, text="TAMBAH", command=self._aksi_tambah).pack(pady=6)

        elif menu == "ARRAY - HAPUS PESANAN" or menu == "LINKEDLIST - HAPUS PESANAN":
            self._tambah_input("Index (0 = pesanan pertama)")
            tk.Button(self.frame_form, text="HAPUS", command=self._aksi_hapus).pack(pady=6)

        elif menu == "ANTREAN - ISI (ENQUEUE)":
            self._tambah_input("Isi pesanan (teks bebas)")
            tk.Button(self.frame_form, text="ENQUEUE", command=self._aksi_enqueue).pack(pady=6)

        elif menu == "ANTREAN - LAYANI BERIKUTNYA (DEQUEUE)":
            tk.Button(self.frame_form, text="DEQUEUE", command=self._aksi_dequeue).pack(pady=6)

        elif menu == "UNDO":
            tk.Button(self.frame_form, text="UNDO", command=self._aksi_undo).pack(pady=6)

        elif menu == "LAPORAN - BUAT (INSERTION SORT)":
            self._tambah_input("Filter resto (kosongkan = semua)")
            self._tambah_input("Filter status (DONE/CANCEL/ANTRE, kosongkan = semua)")
            self._tambah_input("Urutkan berdasarkan (harga / t_masuk_detik)")
            self._tambah_input("Maks baris (disarankan <= 2000)")
            tk.Button(self.frame_form, text="BUAT LAPORAN", command=self._aksi_buat_laporan).pack(pady=6)

        elif menu == "LAPORAN - CARI (BINARY SEARCH)":
            self._tambah_input("Nilai yang dicari")
            tk.Button(self.frame_form, text="CARI", command=self._aksi_cari_laporan).pack(pady=6)

    # ------------------------------------------------------------------
    # Aksi-aksi (dipanggil tombol), tiap aksi: panggil backend + catat waktu
    # ------------------------------------------------------------------
    def _aksi_load(self):
        path_csv = os.path.join(os.path.dirname(__file__), "..", "data", "pesanan.csv")

        # Tampilkan status dulu & paksa redraw, karena load 200.000 baris
        # makan waktu beberapa detik dan Tkinter bakal terlihat "freeze"
        # kalau tidak dikasih tahu dulu ke pengguna.
        self._tampilkan_hasil("Sedang memuat 200.000 data, mohon tunggu...")
        self.update_idletasks()

        t0 = time.perf_counter()
        self.arr, self.ll, jumlah = load_pesanan_csv(path_csv)  # limit=None -> semua baris
        t1 = time.perf_counter()

        self.manager = ManajerPesananGabungan(self.arr, self.ll)
        self.laporan_terakhir = None
        self.laporan_kunci = None

        self._tampilkan_hasil(
            "Berhasil load {} baris pesanan dari data/pesanan.csv ke Array & LinkList.".format(jumlah)
        )
        self._log("load", "M1 - I/O", (t1 - t0) * 1000)

    def _aksi_lihat(self):
        if not self._cek_data_dimuat():
            return
        try:
            idx = int(self._ambil_input("Index (0 = pesanan pertama)"))
        except ValueError:
            self._tampilkan_hasil("Index harus berupa angka.")
            return

        pakai_array = self.menu_aktif.startswith("ARRAY")
        struktur = self.arr if pakai_array else self.ll
        nama_modul = "M1 - array" if pakai_array else "M1 - linked list"
        nama_aksi = "array_get" if pakai_array else "linklist_get"

        t0 = time.perf_counter()
        try:
            p = struktur.get(idx)
            t1 = time.perf_counter()
            self._tampilkan_hasil(repr(p))
        except IndexError as e:
            t1 = time.perf_counter()
            self._tampilkan_hasil("Error: {}".format(e))
        self._log(nama_aksi, nama_modul, (t1 - t0) * 1000)

    def _aksi_tambah(self):
        if not self._cek_data_dimuat():
            return
        pelanggan = self._ambil_input("Nama pelanggan")
        resto = self._ambil_input("Resto")
        menu_makanan = self._ambil_input("Menu")
        try:
            harga = int(self._ambil_input("Harga"))
        except ValueError:
            self._tampilkan_hasil("Harga harus berupa angka.")
            return

        if "REGULER" in self.menu_aktif:
            prioritas = 3
        elif "PRIORITAS" in self.menu_aktif:
            prioritas = 2
        else:
            prioritas = 1

        oid = "O-UI-{}".format(int(time.time() * 1000) % 1000000)
        p = Pesanan(oid, pelanggan, resto, menu_makanan, harga, prioritas, 0, None, "ANTRE")

        # Ditambahkan ke Array DAN LinkList sekaligus (selalu sinkron),
        # tapi waktunya tetap dicatat terpisah supaya bisa dibandingkan.
        if prioritas == 3:
            idx, waktu_arr, waktu_ll = self.manager.tambah_reguler(p)
            nama_aksi = "tambah_reguler"
        elif prioritas == 2:
            idx, waktu_arr, waktu_ll = self.manager.tambah_prioritas(p)
            nama_aksi = "tambah_prioritas"
        else:
            idx, waktu_arr, waktu_ll = self.manager.tambah_vip(p)
            nama_aksi = "tambah_vip"

        self._tampilkan_hasil(
            "Berhasil tambah di index {} (dari {} total data sekarang):\n{}\n\n"
            "Data ini ADA DI KEDUA struktur (Array & LinkList) di index yang sama.".format(
                idx, len(self.arr), p
            )
        )
        self._log(nama_aksi, "M1 - array", waktu_arr)
        self._log(nama_aksi, "M1 - linked list", waktu_ll)

    def _aksi_hapus(self):
        if not self._cek_data_dimuat():
            return
        try:
            idx = int(self._ambil_input("Index (0 = pesanan pertama)"))
        except ValueError:
            self._tampilkan_hasil("Index harus berupa angka.")
            return

        try:
            # Dihapus dari Array DAN LinkList sekaligus (tetap sinkron).
            p, waktu_arr, waktu_ll = self.manager.hapus(idx)
            self._tampilkan_hasil(
                "Terhapus dari KEDUA struktur:\n{}".format(p)
            )
            self._log("hapus_pesanan", "M1 - array", waktu_arr)
            self._log("hapus_pesanan", "M1 - linked list", waktu_ll)
        except IndexError as e:
            self._tampilkan_hasil("Error: {}".format(e))

    def _aksi_enqueue(self):
        isi = self._ambil_input("Isi pesanan (teks bebas)")
        if isi == "":
            isi = "pesanan-tanpa-nama"

        t0 = time.perf_counter()
        self.antrean.enqueue(isi)
        t1 = time.perf_counter()

        self._tampilkan_hasil("Antrean sekarang berisi {} pesanan.".format(len(self.antrean)))
        self._log("enqueue", "M2 - antrean", (t1 - t0) * 1000)

    def _aksi_dequeue(self):
        t0 = time.perf_counter()
        try:
            keluar = self.antrean.dequeue()
            t1 = time.perf_counter()
            self._tampilkan_hasil(
                "Dilayani: {}\nSisa antrean: {}".format(keluar, len(self.antrean))
            )
        except IndexError as e:
            t1 = time.perf_counter()
            self._tampilkan_hasil("Error: {}".format(e))
        self._log("dequeue", "M2 - antrean", (t1 - t0) * 1000)

    def _aksi_undo(self):
        if not self._cek_data_dimuat():
            return

        t0 = time.perf_counter()
        try:
            # undo() membalikkan aksi di KEDUA struktur sekaligus (tetap sinkron).
            aksi = self.manager.undo()
            t1 = time.perf_counter()
            self._tampilkan_hasil(
                "Undo berhasil (di Array & LinkList sekaligus).\n"
                "Aksi yang dibatalkan: {}".format(aksi)
            )
        except IndexError as e:
            t1 = time.perf_counter()
            self._tampilkan_hasil("Error: {}".format(e))
        self._log("undo", "M2 - undo", (t1 - t0) * 1000)

    def _aksi_buat_laporan(self):
        if not self._cek_data_dimuat():
            return

        filter_resto = self._ambil_input("Filter resto (kosongkan = semua)").strip()
        if filter_resto == "":
            filter_resto = None

        filter_status = self._ambil_input("Filter status (DONE/CANCEL/ANTRE, kosongkan = semua)").strip()
        if filter_status == "":
            filter_status = None
        elif filter_status not in ("DONE", "CANCEL", "ANTRE"):
            self._tampilkan_hasil('Filter status harus "DONE", "CANCEL", "ANTRE", atau dikosongkan.')
            return

        kunci = self._ambil_input("Urutkan berdasarkan (harga / t_masuk_detik)").strip()
        if kunci == "":
            kunci = "harga"
        if kunci != "harga" and kunci != "t_masuk_detik":
            self._tampilkan_hasil('Kunci urut harus "harga" atau "t_masuk_detik".')
            return

        teks_maks = self._ambil_input("Maks baris (disarankan <= 2000)").strip()
        try:
            maks_baris = int(teks_maks) if teks_maks != "" else 1000
        except ValueError:
            self._tampilkan_hasil("Maks baris harus berupa angka.")
            return

        self._tampilkan_hasil("Sedang membuat laporan (filter + insertion sort), mohon tunggu...")
        self.update_idletasks()

        t0 = time.perf_counter()
        laporan = buat_laporan(
            self.arr, kunci=kunci,
            filter_resto=filter_resto, filter_status=filter_status,
            maks_baris=maks_baris,
        )
        t1 = time.perf_counter()

        self.laporan_terakhir = laporan
        self.laporan_kunci = kunci

        teks = "Laporan terbentuk: {} baris, diurutkan berdasarkan '{}'.\n\n".format(len(laporan), kunci)
        teks += "10 baris pertama:\n"
        i = 0
        while i < 10 and i < len(laporan):
            teks += " - {}\n".format(laporan[i])
            i += 1
        self._tampilkan_hasil(teks)
        self._log("buat_laporan (insertion_sort)", "M3 - laporan", (t1 - t0) * 1000)

    def _aksi_cari_laporan(self):
        if self.laporan_terakhir is None:
            self._tampilkan_hasil('Belum ada laporan. Pilih menu "LAPORAN - BUAT (INSERTION SORT)" dulu.')
            return

        teks_nilai = self._ambil_input("Nilai yang dicari").strip()
        try:
            nilai_target = int(teks_nilai)
        except ValueError:
            self._tampilkan_hasil("Nilai yang dicari harus berupa angka.")
            return

        t0 = time.perf_counter()
        idx = cari_di_laporan(self.laporan_terakhir, self.laporan_kunci, nilai_target)
        t1 = time.perf_counter()

        if idx == -1:
            self._tampilkan_hasil(
                "Tidak ditemukan pesanan dengan {} = {} di laporan terakhir.".format(
                    self.laporan_kunci, nilai_target
                )
            )
        else:
            self._tampilkan_hasil(
                "Ditemukan di index {} (dari {} baris laporan):\n{}".format(
                    idx, len(self.laporan_terakhir), self.laporan_terakhir[idx]
                )
            )
        self._log("cari_di_laporan (binary_search)", "M3 - laporan", (t1 - t0) * 1000)


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
