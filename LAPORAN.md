# LAPORAN TUGAS BESAR KECERDASAN BUATAN
## Formulasi Matematis dan Implementasi Aplikasi Web Simulasi Algoritma A* Search pada 3 Lingkungan Pengujian + Game Pathfinding

**Kelompok:** 1
**Mata Kuliah:** Kecerdasan Buatan (Semester 3)
**Berkas Program:** `index.html` (aplikasi web 3-tab), `fish_astar.html` (game pathfinding), `tsp_astar.py` + `app.py` (skrip pendukung Python)
**Akses Repositori/Drive:** [Lampirkan Link Google Drive Akses Terbuka di Sini]

---

## 1. Pendahuluan & Latar Belakang Masalah
Metode pencarian heuristik (*informed search*) adalah cabang fundamental kecerdasan buatan untuk menyelesaikan masalah optimasi rute dan penjelajahan ruang keadaan (*state space*). Berdasarkan instruksi tugas besar mata kuliah:
> *"Berdasarkan kasus nyata atau simulasi kompleks, buat aplikasi yang cocok dengan metode pencarian: Best First Search, A*, Hill-Climbing, Simulated Annealing, Genetic Algorithm, dan CSP. Contoh: Simulasi sistem pengiriman barang (dari masalah TSP), silakan dikembangkan. Kelompok 1 berfokus pada A* Search."*

Kelompok 1 memilih **A* Search saja** sebagai metode yang diimplementasikan; metode lain (Best First Search, Hill-Climbing, Simulated Annealing, Genetic Algorithm, CSP) berada di luar skop kelompok ini.

Aplikasi dirancang memiliki modul pengujian independen:
1. **Modul 1 (Default): Lab Pohon Heuristik (Custom):** graf pohon dengan bobot edge dan heuristik yang dapat diubah lewat *Click-to-Edit*, dilengkapi mekanisme *Re-Opening Closed Nodes* untuk heuristik inkonsisten.
2. **Modul 2: Logistik Grid 2D (Medan Berat Non-Uniform Cost):** kurir menempuh rintangan spasial (Aspal = 1, Lumpur = 3, Sungai = 5, Tembok = tak terlewati) dengan metrik *Manhattan* dan *Euclidean*.
3. **Modul 3: TSP Logistik (Pengiriman Realistis):** tur kurir yang wajib mengunjungi semua toko lalu kembali ke gudang melalui jaringan jalan; heuristik MST dihitung dari jarak jalan terpendek.
4. **Modul 4 (Game): Sim Fish Shoes (`fish_astar.html`):** pathfinding ikan antar bangunan dengan tiga mode heuristik (Dijkstra eksak, Euclidean ilustratif, manual), *Step Back* per snapshot, dan ekspor tabel runut; ikan hanya boleh berjalan di atas jalan bercost dan mundur (backtrack) bila tidak ada jalan langsung.

---

## 2. Landasan Teori Algoritma A*

A* memilih simpul berikutnya dari antrean prioritas (*Open List*) berdasarkan:
$$f(n) = g(n) + h(n)$$

1. **$g(n)$ (Actual Cost):** akumulasi biaya nyata dari Start ke simpul $n$.
2. **$h(n)$ (Heuristic Cost):** estimasi biaya termurah dari $n$ ke Goal.
3. **Syarat Admissibility:** agar A* dijamin optimal, $h(n) \le h^*(n)$ untuk setiap $n$, dengan $h^*(n)$ jarak nyata minimum yang sesungguhnya.
4. **Konsistensi (monotonik):** $h(n) \le c(n,n') + h(n')$ untuk tiap edge. Heuristik konsisten pasti admissible; heuristik admissible yang inkonsisten tetap optimal **asal** simpul tertutup dibuka kembali (*re-open*) ketika ditemukan rute $g$ yang lebih murah, dan goal dinyatakan tercapai saat Goal **dikeluarkan** dari Open List (bukan saat pertama dibangkitkan).

Aturan tie-break yang dipakai aplikasi web: $f$ terkecil didahulukan; jika $f$ sama, $g$ terbesar didahulukan (cabang terdalam dulu).

### Matriks admissibility per mode (sesuai implementasi)

| Modul | Heuristik | Sifat | Jaminan optimal |
|---|---|---|---|
| Lab Pohon (goal K, default) | Manual terkalibrasi: $h(A)=5$, $h(B)=3$ (= jarak nyata) | Admissible | Ya |
| Lab Pohon (edit manual) | Bebas, bisa overestimate | Bisa inadmissible; aplikasi memberi *Admissibility Alert* dan menahan klaim "optimal" | Hanya jika $h \le h^*$ |
| Grid Manhattan/Euclidean | Jarak grid, biaya langkah minimum 1 | Konsisten, admissible | Ya |
| TSP Web | MST di atas closure jarak jalan + akses masuk/keluar | Admissible | Ya |
| TSP Python | MST di atas graf lengkap Euclidean | Admissible | Ya |
| Fish mode Dijkstra | Jarak jalan nyata ke Goal ($h = h^*$) | Eksak, admissible | Ya |
| Fish mode Euclidean | Jarak piksel/45, ilustratif | **Tidak dijamin** admissible; aplikasi memberi peringatan | Tidak dijamin |
| Fish mode manual | Bebas | Bisa inadmissible; aplikasi memberi peringatan | Hanya jika $h \le h^*$ |

---

## 3. Analisis Eksekusi & Pemodelan Sistem

### A. Modul 1: Lab Pohon Heuristik (Tab Default)
- Default untuk goal K: satu-satunya koridor ke K adalah `A-B(2)-E(1)-K(2) = 5`, sehingga $h(A)=5$ dan $h(B)=3$ tepat sama dengan jarak nyata (admissible).
- Nilai $h$ dapat diubah manual; bila pengguna membuat $h$ overestimate (misal $h(B)=9$), algoritma mendeteksi rute $g$ lebih murah ke simpul tertutup, membatalkan status *closed*-nya (*re-open*), dan aplikasi menampilkan peringatan admissibility serta tidak mengklaim rute "optimal".
- Saat goal diganti, goal baru otomatis $h=0$; aplikasi mencatat bahwa $h$ node lain masih terkalibrasi untuk goal lama dan perlu disesuaikan manual.

### B. Modul 2: Logistik Grid 2D (Medan Berat Non-Uniform Cost)
- **Matriks Biaya Langkah:** Aspal ($c = 1$), Lumpur ($c = 3$), Sungai ($c = 5$), Tembok (tak terlewati).
- Manhattan dan Euclidean admissible karena biaya langkah minimum adalah 1; A* memilih rute biaya total terendah, bukan jarak geometris terdekat. Contoh skenario: sungai (+5) di tengah jalur membuat rute memutar via aspal ($1+1+1$) lebih murah.
- Implementasi re-open diseragamkan dengan Tree; entri basi (*stale*) dilewati dengan loop.

### C. Modul 3: TSP Logistik Multi-Drop
- **Ruang Keadaan:** $\text{State} = (\text{lokasi kurir}, \text{himpunan belum dikunjungi})$.
- **Heuristik MST:** $h = \min \text{dist}(c,U) + \text{MST}(U) + \min \text{dist}(U,\text{depot})$, dengan $\text{dist}$ = jarak jalan terpendek (Dijkstra di atas road-graph), bukan garis lurus.
- State tur-lengkap yang kembali ke depot hanya diterima bila $g$-nya terbaik (penjagaan minimum), lalu antrean diurut ulang.
- Animasi truk mengunjungi node jalan sepanjang tur optimal hingga kembali ke gudang.
- **Perbedaan dengan `tsp_astar.py`:** skrip Python memakai graf lengkap Euclidean (6 titik Banjarmasin/Pelaihari, urutan ekspansi deterministik), sedangkan Web memakai closure road-graph; formulanya sama, domain jaraknya berbeda. Keduanya terdokumentasi agar tidak tertukar.

### D. Modul 4: Game Sim Fish Shoes
- Start permanen Kos Kan; graf acak berbiji (*seed* via `?seed=`, misal `fish_astar.html?seed=7`) dan goal = node terjauh dari Start agar demo dapat diulang.
- Mode Dijkstra menghitung $h$ eksak; mode Euclidean dan manual diawasi pemeriksa admissibility yang membandingkan $h$ dengan jarak Dijkstra nyata.
- *Step Back* mengembalikan snapshot pra-ekspansi (struktur Open/Closed, tabel, log, posisi ikan); entri basi dibuang tanpa mengotori riwayat.
- **Aturan gerak ikan:** ikan hanya menempuh jalan yang benar-benar ada. Setiap langkah menyorot jalan, menyalakan badge `cost` berwarna kuning, dan menuliskan baris log `Ikan menempuh N1 -> N4 (cost 3)`, sehingga tidak ada perpindahan tanpa biaya.
- Karena urutan ekspansi A* ($f$ terkecil) tidak selalu berimpit dengan urutan jalan, bila simpul hasil ekspansi tidak bersebelahan dengan posisi ikan, ikan **mundur (backtrack)** ke node sebelumnya dulu, baru melanjutkan dari posisi terakhir — persis perilaku penelusuran Open List saat jalur mandek. Pergerakan ini murni visualisasi; $g(n)$ dihitung dari bobot jalan saat relaksasi, bukan dari animasi.

### E. Skrip Python pendukung
- `app.py`: contoh grid **seragam** 4-arah (cost 1) dengan closed-set, tie-break $g$ terbesar, dan validasi ramah (buntu, start/goal di rintangan, start = goal). Varian medan berbobot hidup di `index.html`.
- `tsp_astar.py`: A* TSP graf-lengkap Euclidean dengan heuristik MST admissible dan urutan ekspansi deterministik (12 ekspansi state pada dataset bawaan).

---

## 4. Panduan Demonstrasi Presentasi

1. **Buka `index.html`** (berjalan lokal penuh di browser, tab Lab Pohon terbuka duluan).
2. **Demo Lab Pohon (optimal):**
   - Jalankan Play/Step apa adanya; rute `A-B-E-K` cost 5 dinyatakan optimal karena $h$ admissible.
3. **Demo Admissibility Alert (Lab Pohon):**
   - Ubah $h(B)$ menjadi 9 (overestimate), jalankan ulang; tunjukkan ekspansi terbuang ke subtree mati, *Admissibility Alert*, dan hilangnya klaim "optimal". (Graf Tree tanpa siklus, sehingga demo ini menekankan deteksi overestimate, bukan re-open.)
4. **Demo Re-open Closed Node (Fish, deterministik):**
   - Buka `fish_astar.html?seed=7`, pilih mode Manual, set $h(N1)=100$ dan $h(N3)=100$, jalankan Step; tunjukkan log *Re-open N4* saat rute $g$ lebih murah ditemukan ke simpul tertutup.
5. **Demo Grid (medan berat):**
   - Pasang Sungai (+5) melintang dengan brush toolbar; jalankan Step; tunjukkan $g/f$ memilih rute aspal termurah.
   - Tutup total jalur ke goal untuk mendemo status "Jalan Buntu" yang ditangani elegan.
6. **Demo TSP:**
   - Edit cost badge jalan (lancar/macet), eksekusi, tunjukkan tur mengunjungi semua toko dan kembali ke gudang; unduh tabel runut berekstensi `.xls`.
7. **Demo Fish (opsional, mode presentasi):**
   - Buka `fish_astar.html?seed=7`, aktifkan Mode Presentasi, mainkan Step/Back; ganti ke mode Euclidean untuk menunjukkan peringatan admissibility.
   - Pindah ke mode Manual dengan $h(n)=0$ (semua node), jalankan Step: urutan ekspansi menjalar ke simpul yang tidak bersebelahan, sehingga ikan **mundur (backtrack)** dulu dan tiap jalan yang ditempuh menyalakan badge cost + log `Ikan menempuh ... (cost ...)` — bukti tidak ada gerak gratis.

---

## 5. Kesimpulan
Aplikasi menyatukan graf akademik, navigasi medan berbobot, TSP road-graph, dan game pathfinding dalam satu prinsip: $f(n)=g(n)+h(n)$ dengan evaluasi jujur terhadap admissibility. Klaim "optimal" hanya ditampilkan bila $h$ terbukti tidak melebihi jarak nyata; bila tidak, aplikasi menampilkannya sebagai rute "tidak dijamin optimal" beserta simpul penyebabnya. Seluruh tabel runut ($g,h,f$, Open/Closed, keputusan) dapat diunduh sebagai `.xls` untuk lampiran laporan.
