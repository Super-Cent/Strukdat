"""
frontend/ui.py - Jendela Tkinter untuk Proyek 2EZ4U APP
"""

import os
import sys
import time
import tkinter as tk
from tkinter import scrolledtext

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from m1_pesanan import Pesanan, load_pesanan_csv
from m2_antrean import (
    AntreanNaif, AntreanMelingkar, ManajerPesananGabungan,
    ke_postfix, hitung
)
from m3_laporan import buat_laporan, cari_di_laporan_oid


MENU_STRUCTURE = [
    ("DATA", ["DATA - LOAD"]),
    ("M1 - DATA PESANAN", [
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
    ]),
    ("M2 - STACK DAN QUEUE", [
        "STACK - POSTFIX (MESIN KASIR)",
        "STACK - UNDO",
        "STACK - REDO",
        "QUEUE - ENQUEUE (ISI ANTREAN)",
        "QUEUE - DEQUEUE NAIF",
        "QUEUE - DEQUEUE CIRCULAR",
    ]),
    ("M3 - SORT DAN SEARCH", [
        "SORT - INSERTION SORT",
        "SORT - MERGE SORT",
        "SEARCH - LINEAR SEARCH",
        "SEARCH - BINARY SEARCH",
    ])
]


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("2EZ4U Food Delivery")
        self.geometry("1000x700")
        self.configure(bg="#f4f4f4")

        # --- state backend ---
        self.arr = None
        self.ll = None
        self.manager = None

        self.antrean_naif = AntreanNaif()
        self.antrean_circular = AntreanMelingkar()

        self.laporan_terakhir = None
        self.laporan_kunci = None

        self.menu_aktif = None
        self.entries = {}
        self.dropdown_vars = {}

        self._bangun_layout()

    def _bangun_layout(self):
        frame_header = tk.Frame(self, bg="#ffffff", height=35, highlightbackground="#cccccc", highlightthickness=1)
        frame_header.pack(side="top", fill="x")
        frame_header.pack_propagate(False)
        tk.Label(frame_header, text="2EZ4U Food Delivery", font=("Arial", 11, "bold"), fg="#222222", bg="#ffffff").pack(side="left", padx=10, pady=4)

        frame_main = tk.Frame(self, bg="#f4f4f4")
        frame_main.pack(side="top", fill="both", expand=True)

        frame_kiri = tk.Frame(frame_main, width=280, bg="#eaeaea", highlightbackground="#cccccc", highlightthickness=1)
        frame_kiri.pack(side="left", fill="y", padx=5, pady=5)
        frame_kiri.pack_propagate(False)

        self.listbox_menu = tk.Listbox(frame_kiri, font=("Arial", 9), selectbackground="#1e3a5f", selectforeground="white")
        self.listbox_menu.pack(fill="both", expand=True, padx=4, pady=4)
        
        for kategori, items in MENU_STRUCTURE:
            self.listbox_menu.insert("end", "=== " + kategori + " ===")
            for item in items:
                self.listbox_menu.insert("end", "  " + item)
            self.listbox_menu.insert("end", "")

        self.listbox_menu.bind("<<ListboxSelect>>", self._menu_dipilih)

        frame_kanan = tk.Frame(frame_main, bg="#f4f4f4")
        frame_kanan.pack(side="left", fill="both", expand=True, padx=8, pady=5)

        self.label_judul_form = tk.Label(frame_kanan, text="Pilih menu di sebelah kiri", font=("Arial", 12, "bold"), fg="#222222", bg="#f4f4f4", anchor="w")
        self.label_judul_form.pack(fill="x", pady=(0, 2))

        self.label_deskripsi = tk.Label(frame_kanan, text="", font=("Arial", 9), fg="#555555", bg="#f4f4f4", anchor="w", justify="left")
        self.label_deskripsi.pack(fill="x", pady=(0, 6))

        self.frame_form = tk.Frame(frame_kanan, bg="#f4f4f4")
        self.frame_form.pack(fill="x", pady=(0, 6))

        self.frame_hasil = tk.Frame(frame_kanan, bg="#ffffff", highlightbackground="#cccccc", highlightthickness=1)
        self.frame_hasil.pack(fill="both", expand=True, pady=(0, 6))
        
        self.text_hasil = scrolledtext.ScrolledText(self.frame_hasil, font=("Consolas", 9), bd=0)
        self.text_hasil.pack(fill="both", expand=True)

        frame_command = tk.Frame(frame_kanan, bg="#f4f4f4")
        frame_command.pack(fill="x", pady=(0, 2))

        tk.Label(frame_command, text="COMMAND LOG", font=("Arial", 9, "bold"), fg="#222222", bg="#f4f4f4").pack(anchor="w")
        self.text_log = scrolledtext.ScrolledText(frame_command, height=6, font=("Consolas", 9), highlightbackground="#cccccc", highlightthickness=1)
        self.text_log.pack(fill="x", pady=(2, 0))

        self.frame_status = tk.Frame(self, bg="#1e3a5f", height=24)
        self.frame_status.pack(side="bottom", fill="x")
        self.frame_status.pack_propagate(False)

        self.label_status_bar = tk.Label(self.frame_status, text="Ready", font=("Consolas", 9, "bold"), fg="white", bg="#1e3a5f")
        self.label_status_bar.pack(side="left", padx=10)

    def _log(self, teks_aksi, teks_modul, durasi_ms):
        baris = "> " + str(teks_aksi) + " [" + str(teks_modul) + "] " + "{:.2f}".format(durasi_ms) + " ms\n"
        self.text_log.insert("end", baris)
        self.text_log.see("end")
        self.label_status_bar.config(text="[" + str(teks_modul) + "] " + "{:.2f}".format(durasi_ms) + " ms")

    def _tampilkan_hasil(self, teks):
        self.text_hasil.delete("1.0", "end")
        self.text_hasil.insert("end", teks)

    def _bersihkan_form(self):
        for widget in self.frame_form.winfo_children():
            widget.destroy()
        self.entries = {}
        self.dropdown_vars = {}

    def _tambah_input_text(self, row, col, label_teks, default_val=""):
        frame_item = tk.Frame(self.frame_form, bg="#f4f4f4")
        frame_item.grid(row=row, column=col, padx=5, pady=2, sticky="w")
        
        tk.Label(frame_item, text=label_teks, font=("Arial", 9, "bold"), bg="#f4f4f4").pack(anchor="w")
        entry = tk.Entry(frame_item, width=25)
        if default_val:
            entry.insert(0, default_val)
        entry.pack(anchor="w")
        self.entries[label_teks] = entry
        return entry

    def _tambah_input_dropdown(self, row, col, label_teks, opsi_list):
        frame_item = tk.Frame(self.frame_form, bg="#f4f4f4")
        frame_item.grid(row=row, column=col, padx=5, pady=2, sticky="w")

        tk.Label(frame_item, text=label_teks, font=("Arial", 9, "bold"), bg="#f4f4f4").pack(anchor="w")
        var = tk.StringVar(value=opsi_list[0])
        dropdown = tk.OptionMenu(frame_item, var, *opsi_list)
        dropdown.config(width=16, bg="#ffffff", activebackground="#eeeeee")
        dropdown.pack(anchor="w")
        self.dropdown_vars[label_teks] = var
        return var

    def _cek_data_dimuat(self):
        if self.arr is None:
            self._tampilkan_hasil("Data belum dimuat. Pilih menu \"DATA - LOAD\" dulu.")
            return False
        return True

    def _menu_dipilih(self, event):
        seleksi = self.listbox_menu.curselection()
        if len(seleksi) == 0:
            return
        item_teks = self.listbox_menu.get(seleksi[0]).strip()
        
        if item_teks.startswith("===") or item_teks == "":
            return

        menu = item_teks
        self.menu_aktif = menu
        self.label_judul_form.config(text=menu)
        self._bersihkan_form()

        if menu == "DATA - LOAD":
            self.label_deskripsi.config(text="Memuat seluruh data transaksi pesanan dari file CSV.")
            tk.Button(self.frame_form, text="LOAD DATA", bg="#1e3a5f", fg="white", activebackground="#2c5282", activeforeground="white", font=("Arial", 9, "bold"), command=self._aksi_load).grid(row=0, column=0, pady=5)

        elif menu == "STACK - POSTFIX (MESIN KASIR)":
            self.label_deskripsi.config(text="Mengubah ekspresi kalkulasi kasir (infix) ke postfix & menghitung totalnya via Stack.")
            self._tambah_input_text(0, 0, "Ekspresi Infix", "15000 + 20000 * 2")
            tk.Button(self.frame_form, text="HITUNG", bg="#1e3a5f", fg="white", activebackground="#2c5282", activeforeground="white", font=("Arial", 9, "bold"), command=self._aksi_hitung_postfix).grid(row=0, column=1, padx=10, pady=15)

        elif menu == "STACK - UNDO":
            self.label_deskripsi.config(text="Membatalkan efek aksi dequeue/transaksi terakhir.")
            tk.Button(self.frame_form, text="STACK UNDO", bg="#1e3a5f", fg="white", activebackground="#2c5282", activeforeground="white", font=("Arial", 9, "bold"), command=self._aksi_undo).grid(row=0, column=0, pady=5)

        elif menu == "STACK - REDO":
            self.label_deskripsi.config(text="Mengerjakan ulang aksi yang baru saja dibatalkan.")
            tk.Button(self.frame_form, text="STACK REDO", bg="#1e3a5f", fg="white", activebackground="#2c5282", activeforeground="white", font=("Arial", 9, "bold"), command=self._aksi_redo).grid(row=0, column=0, pady=5)

        elif "QUEUE" in menu:
            if "ENQUEUE" in menu:
                self.label_deskripsi.config(text="Memasukkan pesanan berstatus ANTRE dari M1 ke KEDUA antrean (Naif & Circular).")
                tk.Button(self.frame_form, text="ENQUEUE ANTREAN M1", bg="#1e3a5f", fg="white", activebackground="#2c5282", activeforeground="white", font=("Arial", 9, "bold"), command=self._aksi_enqueue_m1).grid(row=0, column=0, pady=5)
            elif "NAIF" in menu:
                self.label_deskripsi.config(text="Dequeue menggunakan Array Biasa - Geser seluruh elemen memori.")
                self._tambah_input_text(0, 0, "Jumlah Dequeue", "1")
                tk.Button(self.frame_form, text="DEQUEUE NAIVE", bg="#1e3a5f", fg="white", activebackground="#2c5282", activeforeground="white", font=("Arial", 9, "bold"), command=self._aksi_dequeue_naive).grid(row=0, column=1, padx=10, pady=15)
            else:
                self.label_deskripsi.config(text="Dequeue menggunakan Circular Array - Kinerja O(1) tanpa pergeseran elemen.")
                self._tambah_input_text(0, 0, "Jumlah Dequeue", "1")
                tk.Button(self.frame_form, text="DEQUEUE CIRCULAR", bg="#1e3a5f", fg="white", activebackground="#2c5282", activeforeground="white", font=("Arial", 9, "bold"), command=self._aksi_dequeue_circular).grid(row=0, column=1, padx=10, pady=15)

        elif "SORT" in menu:
            metode = "Insertion Sort, O(n²)" if "INSERTION" in menu else "Merge Sort, O(n log n)"
            self.label_deskripsi.config(text="Metode Pengurutan: " + metode)
            self._tambah_input_text(0, 0, "Jumlah baris", "10")
            self._tambah_input_dropdown(0, 1, "Diurutkan menurut", ["Harga", "ID Pesanan (oid)", "Waktu Masuk"])
            self._tambah_input_dropdown(0, 2, "Filter Status", ["SEMUA", "DONE", "CANCEL", "ANTRE"])
            tk.Button(self.frame_form, text="URUTKAN", bg="#1e3a5f", fg="white", activebackground="#2c5282", activeforeground="white", font=("Arial", 9, "bold"), command=self._aksi_buat_laporan).grid(row=0, column=3, padx=10, pady=15)

        elif "SEARCH" in menu:
            metode = "Linear Search, O(n)" if "LINEAR" in menu else "Binary Search, O(log n)"
            self.label_deskripsi.config(text="Metode Pencarian ID Unik Pesanan: " + metode)
            self._tambah_input_text(0, 0, "Nomor pesanan (oid)", "O-000001")
            tk.Button(self.frame_form, text="CARI", bg="#1e3a5f", fg="white", activebackground="#2c5282", activeforeground="white", font=("Arial", 9, "bold"), command=self._aksi_cari_laporan).grid(row=0, column=1, padx=10, pady=15)

        elif "LIHAT PESANAN" in menu or "HAPUS PESANAN" in menu:
            self.label_deskripsi.config(text="Akses elemen data berdasarkan nomor indeks.")
            self._tambah_input_text(0, 0, "Index (0 = pertama)", "0")
            aksi_func = self._aksi_lihat if "LIHAT" in menu else self._aksi_hapus
            btn_txt = "LIHAT" if "LIHAT" in menu else "HAPUS"
            tk.Button(self.frame_form, text=btn_txt, bg="#1e3a5f", fg="white", activebackground="#2c5282", activeforeground="white", font=("Arial", 9, "bold"), command=aksi_func).grid(row=0, column=1, padx=10, pady=15)

        elif "TAMBAH PESANAN" in menu:
            self.label_deskripsi.config(text="Menambahkan pesanan baru ke struktur data.")
            self._tambah_input_text(0, 0, "Nama pelanggan")
            self._tambah_input_text(0, 1, "Resto")
            self._tambah_input_text(0, 2, "Menu")
            self._tambah_input_text(0, 3, "Harga")
            tk.Button(self.frame_form, text="TAMBAH", bg="#1e3a5f", fg="white", activebackground="#2c5282", activeforeground="white", font=("Arial", 9, "bold"), command=self._aksi_tambah).grid(row=0, column=4, padx=10, pady=15)

    def _aksi_load(self):
        path_csv = os.path.join(os.path.dirname(__file__), "..", "data", "pesanan.csv")
        self._tampilkan_hasil("Sedang memuat data, mohon tunggu...")
        self.update_idletasks()

        t0 = time.perf_counter()
        self.arr, self.ll, jumlah = load_pesanan_csv(path_csv)
        t1 = time.perf_counter()

        self.manager = ManajerPesananGabungan(self.arr, self.ll)
        self.laporan_terakhir = None
        self._tampilkan_hasil("Berhasil memuat " + str(jumlah) + " baris data pesanan.")
        self._log("load_csv", "M1 - I/O", (t1 - t0) * 1000)

    def _aksi_enqueue_m1(self):
        if not self._cek_data_dimuat(): return
        
        t0 = time.perf_counter()
        count = 0
        terakhir_oid = ""
        
        for i in range(len(self.arr)):
            p = self.arr.get(i)
            if getattr(p, 'status', None) == "ANTRE":
                self.antrean_naif.enqueue(p.oid)
                self.antrean_circular.enqueue(p.oid)
                count += 1
                terakhir_oid = p.oid
        t1 = time.perf_counter()

        pesan_log = "queue_enqueue Pelanggan Baru\n" + str(count) + " pesanan berstatus ANTRE masuk ke KEDUA antrean\n" + str(terakhir_oid) + " masuk paling belakang"
        self._tampilkan_hasil(pesan_log)
        self._log("queue_enqueue", "M2 - queue", (t1 - t0) * 1000)

    def _aksi_dequeue_naive(self):
        try:
            k = int(self.entries.get("Jumlah Dequeue", tk.Entry()).get().strip())
        except ValueError:
            k = 1

        t0 = time.perf_counter()
        terkeluar, digeser = self.antrean_naif.dequeue_banyak(k)
        t1 = time.perf_counter()

        if len(terkeluar) > 0 and self.manager is not None:
            self.manager.catat_dequeue(terkeluar)

        pesan = "queue_dequeue_naive " + str(k) + "\n" + str(len(terkeluar)) + " pesanan keluar | " + str(digeser) + " elemen digeser"
        self._tampilkan_hasil(pesan)
        self._log("queue_dequeue_naive " + str(k), "M2 - queue naif", (t1 - t0) * 1000)

    def _aksi_dequeue_circular(self):
        try:
            k = int(self.entries.get("Jumlah Dequeue", tk.Entry()).get().strip())
        except ValueError:
            k = 1

        t0 = time.perf_counter()
        terkeluar, digeser = self.antrean_circular.dequeue_banyak(k)
        t1 = time.perf_counter()

        if len(terkeluar) > 0 and self.manager is not None:
            self.manager.catat_dequeue(terkeluar)

        pesan = "queue_dequeue_circular " + str(k) + "\n" + str(len(terkeluar)) + " pesanan keluar | " + str(digeser) + " elemen digeser"
        self._tampilkan_hasil(pesan)
        self._log("queue_dequeue_circular " + str(k), "M2 - queue circular", (t1 - t0) * 1000)

    def _aksi_undo(self):
        if not self._cek_data_dimuat(): return
        t0 = time.perf_counter()
        try:
            pesan = self.manager.undo_last(self.antrean_circular)
            t1 = time.perf_counter()
            info_stack = "stack_undo\n" + str(pesan) + "\ntumpukan undo " + str(len(self.manager.stack_undo)) + ", redo " + str(len(self.manager.stack_redo))
            self._tampilkan_hasil(info_stack)
            self._log("stack_undo", "M2 - stack", (t1 - t0) * 1000)
        except Exception as e:
            self._tampilkan_hasil("Error Undo: " + str(e))

    def _aksi_redo(self):
        if not self._cek_data_dimuat(): return
        t0 = time.perf_counter()
        try:
            pesan = self.manager.redo_last(self.antrean_circular)
            t1 = time.perf_counter()
            info_stack = "stack_redo\n" + str(pesan) + "\ntumpukan undo " + str(len(self.manager.stack_undo)) + ", redo " + str(len(self.manager.stack_redo))
            self._tampilkan_hasil(info_stack)
            self._log("stack_redo", "M2 - stack", (t1 - t0) * 1000)
        except Exception as e:
            info_stack = "stack_redo\ntumpukan redo kosong, tidak ada yang diulang"
            self._tampilkan_hasil(info_stack)
            self._log("stack_redo", "M2 - stack", (t1 - t0) * 1000)

    def _aksi_hitung_postfix(self):
        expr = self.entries.get("Ekspresi Infix", tk.Entry()).get().strip()
        t0 = time.perf_counter()
        postfix = ke_postfix(expr)
        total = hitung(postfix)
        t1 = time.perf_counter()

        out_teks = "Infix   : " + str(expr) + "\nPostfix : " + str(postfix) + "\nHasil Evaluasi Stack: Rp " + str(total)
        self._tampilkan_hasil(out_teks)
        self._log("ke_postfix & hitung", "M2 - stack kasir", (t1 - t0) * 1000)

    def _aksi_buat_laporan(self):
        if not self._cek_data_dimuat(): return
        teks_maks = self.entries.get("Jumlah baris", tk.Entry()).get().strip()
        try:
            maks_baris = int(teks_maks) if teks_maks != "" else 1000
        except ValueError:
            self._tampilkan_hasil("Jumlah baris harus berupa angka.")
            return

        metode_sort = "merge" if "MERGE" in self.menu_aktif else "insertion"
        BATAS_MAKS_INSERTION = 5000
        BATAS_MAKS_MERGE = 200000

        if metode_sort == "insertion" and maks_baris > BATAS_MAKS_INSERTION:
            self._tampilkan_hasil("[PENOLAKAN SISTEM]\nJumlah baris (" + str(maks_baris) + ") terlalu besar untuk Insertion Sort O(n²).\nMaksimal baris diizinkan: " + str(BATAS_MAKS_INSERTION) + ".")
            return

        if metode_sort == "merge" and maks_baris > BATAS_MAKS_MERGE:
            self._tampilkan_hasil("[PENOLAKAN SISTEM]\nJumlah baris (" + str(maks_baris) + ") melebihi data maksimum (" + str(BATAS_MAKS_MERGE) + ").")
            return

        pilihan_kunci = self.dropdown_vars.get("Diurutkan menurut", tk.StringVar()).get()
        mapping_kunci = {"Harga": "harga", "ID Pesanan (oid)": "oid", "Waktu Masuk": "t_masuk_detik"}
        kunci = mapping_kunci.get(pilihan_kunci, "harga")

        filter_status = self.dropdown_vars.get("Filter Status", tk.StringVar()).get()
        if filter_status == "SEMUA": filter_status = None

        t0 = time.perf_counter()
        laporan = buat_laporan(self.arr, kunci=kunci, filter_status=filter_status, maks_baris=maks_baris, metode_sort=metode_sort)
        t1 = time.perf_counter()

        self.laporan_terakhir = laporan
        self.laporan_kunci = kunci

        header = "{:<5} {:<15} {:<12} {:<12} {:<18} {:<15}\n".format("#", "oid", "harga", "status", "resto", "menu")
        out_teks = header + ("-" * 80 + "\n")
        i = 0
        while i < len(laporan):
            p = laporan[i]
            out_teks += "{:<5} {:<15} {:<12} {:<12} {:<18} {:<15}\n".format(
                i + 1, str(getattr(p, 'oid', '-')), str(getattr(p, 'harga', '-')),
                str(getattr(p, 'status', '-')), str(getattr(p, 'resto', '-')), str(getattr(p, 'menu_makanan', '-'))
            )
            i += 1

        self._tampilkan_hasil(out_teks)
        self._log(metode_sort + "_sort", "M3 - " + metode_sort + " sort", (t1 - t0) * 1000)

    def _aksi_cari_laporan(self):
        if not self._cek_data_dimuat(): return
        target_oid = self.entries.get("Nomor pesanan (oid)", tk.Entry()).get().strip()

        if not target_oid:
            self._tampilkan_hasil("Masukkan ID Pesanan (oid) yang dicari.")
            return

        metode_search = "linear" if "LINEAR" in self.menu_aktif else "binary"

        if self.laporan_terakhir is None or self.laporan_kunci != "oid":
            if metode_search == "binary":
                self._tampilkan_hasil("Mengurutkan data berdasarkan ID Pesanan (oid) untuk Binary Search...")
                self.update_idletasks()
                self.laporan_terakhir = buat_laporan(self.arr, kunci="oid", maks_baris=200000, metode_sort="merge")
                self.laporan_kunci = "oid"
            else:
                self.laporan_terakhir = buat_laporan(self.arr, kunci="oid", maks_baris=1000, metode_sort="insertion")
                self.laporan_kunci = "oid"

        t0 = time.perf_counter()
        idx = cari_di_laporan_oid(self.laporan_terakhir, target_oid, metode_search=metode_search)
        t1 = time.perf_counter()

        if idx == -1:
            self._tampilkan_hasil("Pesanan dengan ID (oid) '" + str(target_oid) + "' tidak ditemukan.")
        else:
            p = self.laporan_terakhir[idx]
            out_teks = "Ditemukan pada Indeks ke-" + str(idx + 1) + " (dari " + str(len(self.laporan_terakhir)) + " data):\n\n"
            out_teks += "{:<18} : {}\n".format("ID Pesanan (oid)", getattr(p, 'oid', '-'))
            out_teks += "{:<18} : {}\n".format("Pelanggan", getattr(p, 'pelanggan', '-'))
            out_teks += "{:<18} : {}\n".format("Resto", getattr(p, 'resto', '-'))
            out_teks += "{:<18} : {}\n".format("Menu Makanan", getattr(p, 'menu_makanan', '-'))
            out_teks += "{:<18} : {}\n".format("Harga", getattr(p, 'harga', '-'))
            out_teks += "{:<18} : {}\n".format("Status", getattr(p, 'status', '-'))
            self._tampilkan_hasil(out_teks)

        self._log(metode_search + "_search", "M3 - " + metode_search + " search", (t1 - t0) * 1000)

    def _aksi_lihat(self):
        if not self._cek_data_dimuat(): return
        try:
            idx = int(self.entries.get("Index (0 = pertama)", tk.Entry()).get())
            pakai_array = "ARRAY" in self.menu_aktif
            p = self.arr.get(idx) if pakai_array else self.ll.get(idx)
            self._tampilkan_hasil(repr(p))
        except Exception as e:
            self._tampilkan_hasil("Error: " + str(e))

    def _aksi_hapus(self):
        if not self._cek_data_dimuat(): return
        try:
            idx = int(self.entries.get("Index (0 = pertama)", tk.Entry()).get())
            p = self.manager.hapus(idx)
            self._tampilkan_hasil("Terhapus:\n" + repr(p))
            self._log("hapus_pesanan", "M1 - array", 0.0)
        except Exception as e:
            self._tampilkan_hasil("Error: " + str(e))

    def _aksi_tambah(self):
        if not self._cek_data_dimuat(): return
        try:
            if "VIP" in self.menu_aktif:
                prioritas = 1
                nama_aksi = "tambah_vip"
            elif "PRIORITAS" in self.menu_aktif:
                prioritas = 2
                nama_aksi = "tambah_prioritas"
            else:
                prioritas = 3
                nama_aksi = "tambah_reguler"

            p = Pesanan(
                "O-UI-" + str(int(time.time())),
                self.entries["Nama pelanggan"].get(),
                self.entries["Resto"].get(),
                self.entries["Menu"].get(),
                int(self.entries["Harga"].get()),
                prioritas, 0, None, "ANTRE"
            )

            if prioritas == 1:
                idx = self.manager.tambah_vip(p)
            elif prioritas == 2:
                idx = self.manager.tambah_prioritas(p)
            else:
                idx = self.manager.tambah_reguler(p)

            self._tampilkan_hasil("Berhasil ditambahkan pada indeks " + str(idx) + " (Prioritas: " + str(prioritas) + "):\n" + repr(p))
            self._log(nama_aksi, "M1 - array", 0.0)
        except Exception as e:
            self._tampilkan_hasil("Error input: " + str(e))


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()