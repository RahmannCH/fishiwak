# LAPORAN TUGAS BESAR KECERDASAN BUATAN
## Analisis Komparasi, Formulasi Matematis, dan Implementasi Aplikasi Web Simulasi Terpadu Algoritma A* Search pada 3 Lingkungan Pengujian

**Kelompok:** 1  
**Mata Kuliah:** Kecerdasan Buatan (Semester 3)  
**Tenggat Waktu:** 2 Minggu (Presentasi Pekan ke-7)  
**Berkas Program Utama:** `index.html` (Aplikasi Web Terpadu 3-Tab)  
**Akses Repositori/Drive:** [Lampirkan Link Google Drive Akses Terbuka di Sini]

---

## 1. Pendahuluan & Latar Belakang Masalah
Metode pencarian heuristik (*informed search*) adalah cabang fundamental kecerdasan buatan untuk menyelesaikan masalah optimasi rute dan penjelajahan ruang keadaan (*state space*). Berdasarkan instruksi tugas besar mata kuliah:
> *"Berdasarkan kasus nyata atau simulasi kompleks, buat aplikasi yang cocok dengan metode pencarian: Best First Search, A*, Hill-Climbing, Simulated Annealing, Genetic Algorithm, dan CSP. Contoh: Simulasi sistem pengiriman barang (dari masalah TSP), silakan dikembangkan. Kelompok 1 berfokus pada A* Search."*

Untuk menjawab tantangan tersebut secara menyeluruh, aplikasi dirancang memiliki 3 modul pengujian independen dalam satu antarmuka aplikasi web dinamis:
1. **Modul 1 (Default): Lab Pohon Heuristik (Custom):** Pembuktian sifat konsistensi dan kemampuan manipulasi dinamis bobot lintasan (*edge*) serta heuristik secara *Click-to-Edit*, dilengkapi mekanisme penanganan otomatis *Re-Opening Closed Nodes*.
2. **Modul 2: Logistik Grid 2D (Medan Berat Non-Uniform Cost):** Simulasi kurir menempuh rintangan spasial (Jalan Aspal = 1, Lumpur = 3, Sungai = 5, Tembok = $\infty$) dengan pembanding metrik *Manhattan* ($L_1$) dan *Euclidean* ($L_2$).
3. **Modul 3: TSP Logistik (Pengiriman Realistis):** Simulasi tur kurir yang wajib mengunjungi semua toko lalu kembali ke gudang. Jaringan jalan tetap dengan cost tiap edge yang dapat diedit, dan heuristik MST dihitung menggunakan jarak terpendek pada jaringan jalan tersebut.

---

## 2. Landasan Teori Algoritma A*

Algoritma A* memilih simpul berikutnya dalam antrean prioritas (*Priority Queue / Open List*) berdasarkan formula:
$$f(n) = g(n) + h(n)$$

1. **$g(n)$ (Actual Cost):** Akumulasi biaya nyata dari titik awal ($Start$) ke simpul saat ini ($n$).
2. **$h(n)$ (Heuristic Cost):** Estimasi biaya terendah untuk mencapai kondisi Goal dari simpul $n$.
3. **Syarat Admissibility:** Agar A* dijamin menghasilkan solusi optimal (terpendek mutlak), nilai $h(n)$ harus memenuhi $h(n) \le h^*(n)$ di mana $h^*(n)$ adalah jarak nyata minimum yang sesungguhnya.

- A* Search ($f = g + h$) memilih state dengan estimasi total terendah, memakai biaya aktual $g(n)$ dan estimasi sisa $h(n)$.
- Heuristik otomatis aplikasi admissible. Mode manual tersedia untuk eksperimen; optimalitas hanya terjamin jika nilai $h(n)$ tidak melebih-lebihkan biaya minimum sebenarnya.
- Jika rute lebih murah ditemukan ke node tertutup, node dibuka kembali dan dimasukkan ke Open List.

---

## 3. Analisis Eksekusi & Pemodelan Sistem

### A. Modul 1: Lab Pohon Heuristik (Tab Default)
- Representasi graf pohon dengan kemampuan klik langsung untuk mengubah beban biaya (misal mengubah lintasan menjadi mahal) dan heuristik.
- **Logika Re-Opening Closed Nodes:** Jika pengguna memasukkan heuristik manual yang inkonsisten sehingga algoritma menemukan rute baru yang *lebih murah* menuju simpul yang sudah telanjur dimasukkan ke dalam *Closed List*, algoritma tidak akan mengabaikannya. Simpul tersebut secara cerdas dibatalkan status *closed*-nya dan dimasukkan kembali ke antrean prioritas demi mempertahankan hukum optimalitas A*.

### B. Modul 2: Logistik Grid 2D (Medan Berat Non-Uniform Cost)
- **Matriks Biaya Langkah:** Aspal ($c = 1$), Lumpur ($c = 3$), Sungai ($c = 5$), Tembok ($c = \infty$).
- Saat rintangan sungai menghalangi garis lurus antara kurir dan tujuan:
  - *A* Search:* Menguji rute memutar melalui aspal. Karena biaya putaran ($1+1+1$) terakumulasi lebih rendah dibanding masuk sungai ($+5$), A* memilih rute dengan total biaya terendah.

### C. Modul 3: Pengayaan TSP (Traveling Salesperson Problem) Multi-Drop
- **Ruang Keadaan (State):** $\text{State}(n) = (\text{Lokasi\_Kurir\_Saat\_Ini}, \text{Daftar\_Pelanggan\_Yang\_Telah\_Dikunjungi})$.
- **Heuristik MST Prim:**
  $$h(n) = \min_{u \in U} \text{dist}(c, u) + \text{Bobot MST}(U) + \min_{u \in U} \text{dist}(u, \text{Gudang})$$
- Visualisasi memakai jaringan jalan statis. Setiap jalan memiliki cost yang dapat diedit pengguna, sementara A* menghitung jarak perjalanan antar lokasi melalui rute jalan terpendek. Animasi truk mengikuti edge jalan nyata pada tur optimal.

---

## 4. Panduan Demonstrasi Presentasi (Pekan ke-7)

1. **Buka Aplikasi `index.html`** (Aplikasi berjalan lokal secara penuh di *browser*, memuat Tab Lab Pohon terlebih dahulu).
2. **Demo Lab Pohon:**
   - Ubah salah satu bobot edge (*Click-to-Edit* angka lintasan) menjadi sangat besar.
   - Jalankan A* dan peragakan mekanisme mesinnya mendeteksi pembengkakan biaya $f(n)$ lalu membatalkan rute tersebut (*pruning* rute mahal).
3. **Demo Grid Logistik (Medan Berat):**
   - Buat rintangan Sungai (+5) di tengah jalur dengan menggunakan *brush toolbar*.
   - Jalankan **A*** dengan mode Step &rarr; Tunjukkan bagaimana perubahan cost medan memengaruhi nilai $g(n)$ dan $f(n)$.
   - Buktikan A* memilih rute aspal dengan total cost terendah, bukan sekadar jarak geometris terdekat.
4. **Demo TSP Logistik Pengiriman Nyata:**
   - Edit cost pada badge jaringan jalan untuk mensimulasikan jalan lancar atau macet.
   - Eksekusi simulasi dan tunjukkan animasi truk yang mengikuti edge jalan hingga semua toko dikunjungi lalu kembali ke gudang.

---

## 5. Kesimpulan
Aplikasi web ini menyatukan pemodelan graf akademik, navigasi medan berbobot, dan TSP pada jaringan jalan statis dalam satu antarmuka. Fokus implementasi adalah A* Search dengan evaluasi $f(n)=g(n)+h(n)$ dan heuristik admissible untuk jaminan rute optimal.
