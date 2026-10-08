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
3. **Modul 3: TSP Logistik (Pengiriman Realistis):** Simulasi perjalanan tur kurir multi-pelanggan kembali ke gudang (*drag & drop map*) dengan panduan heuristik *Minimum Spanning Tree* (MST) untuk membuktikan penghematan bahan bakar A* terhadap rute serakah (*Greedy*).

---

## 2. Landasan Teori Algoritma A*

Algoritma A* memilih simpul berikutnya dalam antrean prioritas (*Priority Queue / Open List*) berdasarkan formula:
$$f(n) = g(n) + h(n)$$

1. **$g(n)$ (Actual Cost):** Akumulasi biaya nyata dari titik awal ($Start$) ke simpul saat ini ($n$).
2. **$h(n)$ (Heuristic Cost):** Estimasi biaya terendah untuk mencapai kondisi Goal dari simpul $n$.
3. **Syarat Admissibility:** Agar A* dijamin menghasilkan solusi optimal (terpendek mutlak), nilai $h(n)$ harus memenuhi $h(n) \le h^*(n)$ di mana $h^*(n)$ adalah jarak nyata minimum yang sesungguhnya.

- **Greedy Best-First ($f = h$):** Bersifat *myopic* (rabun). Agen hanya tergiur oleh simpul yang tampak terdekat saat ini tanpa memedulikan akumulasi beban jarak yang telah dilalui ($g$). Sering kali terjebak dalam rute berbiaya tinggi (*Heuristic Trap*).
- **A* Search ($f = g + h$):** Memperhitungkan akumulasi $g(n)$ yang sudah dikeluarkan. Jika suatu cabang di awal tampak dekat namun memiliki medan berat di tengah jalan, A* secara otomatis berbalik arah (*backtracking/pruning*) untuk mencari alternatif yang secara absolut lebih murah.

---

## 3. Analisis Eksekusi & Pemodelan Sistem

### A. Modul 1: Lab Pohon Heuristik (Tab Default)
- Representasi graf pohon dengan kemampuan klik langsung untuk mengubah beban biaya (misal mengubah lintasan menjadi mahal) dan heuristik.
- **Logika Re-Opening Closed Nodes:** Jika pengguna memasukkan heuristik manual yang inkonsisten sehingga algoritma menemukan rute baru yang *lebih murah* menuju simpul yang sudah telanjur dimasukkan ke dalam *Closed List*, algoritma tidak akan mengabaikannya. Simpul tersebut secara cerdas dibatalkan status *closed*-nya dan dimasukkan kembali ke antrean prioritas demi mempertahankan hukum optimalitas A*.

### B. Modul 2: Logistik Grid 2D (Medan Berat Non-Uniform Cost)
- **Matriks Biaya Langkah:** Aspal ($c = 1$), Lumpur ($c = 3$), Sungai ($c = 5$), Tembok ($c = \infty$).
- Saat rintangan sungai menghalangi garis lurus antara kurir dan tujuan:
  - *Greedy Best-First:* Menerjang sungai secara membabi-buta karena tergiur nilai $h(n)$ yang mengecil. Menghasilkan total biaya yang sangat boros.
  - *A\* Search:* Menguji rute memutar melalui aspal. Karena biaya putaran ($1+1+1$) terakumulasi lebih rendah dibanding masuk sungai ($+5$), A* dengan cerdas bermanuver menghindari rintangan mahal.

### C. Modul 3: Pengayaan TSP (Traveling Salesperson Problem) Multi-Drop
- **Ruang Keadaan (State):** $\text{State}(n) = (\text{Lokasi\_Kurir\_Saat\_Ini}, \text{Daftar\_Pelanggan\_Yang\_Telah\_Dikunjungi})$.
- **Heuristik MST Prim:**
  $$h(n) = \min_{u \in U} \text{dist}(c, u) + \text{Bobot MST}(U) + \min_{u \in U} \text{dist}(u, \text{Gudang})$$
- Visualisasi diangkat ke standar profesional: Titik logistik dapat digeser secara dinamis, sistem menampilkan jaringan koneksi jalan beserta angka radius geometrisnya, dan animasi rute disempurnakan dengan kehadiran ikon truk kurir yang bergerak mulus sepanjang tur optimal. Algoritma akan menghitung secara latar belakang (*background check*) seberapa besar A* mampu menghemat jarak dan bahan bakar dibandingkan *Greedy*.

---

## 4. Panduan Demonstrasi Presentasi (Pekan ke-7)

1. **Buka Aplikasi `index.html`** (Aplikasi berjalan lokal secara penuh di *browser*, memuat Tab Lab Pohon terlebih dahulu).
2. **Demo Lab Pohon:**
   - Ubah salah satu bobot edge (*Click-to-Edit* angka lintasan) menjadi sangat besar.
   - Jalankan A* dan peragakan mekanisme mesinnya mendeteksi pembengkakan biaya $f(n)$ lalu membatalkan rute tersebut (*pruning* rute mahal).
3. **Demo Grid Logistik (Medan Berat):**
   - Buat rintangan Sungai (+5) di tengah jalur dengan menggunakan *brush toolbar*.
   - Jalankan **Greedy** &rarr; Tunjukkan agen nekat menerobos sungai karena rabun heuristik.
   - Jalankan **A\*** &rarr; Buktikan AI menghindari sungai dan memutar lewat aspal demi penghematan.
4. **Demo TSP Logistik Pengiriman Nyata:**
   - Pindahkan titik-titik toko/pelanggan dan Gudang menggunakan tetikus secara leluasa.
   - Eksekusi simulasi dan tunjukkan animasi kurir (Truk) menjalankan tugas pengirimannya, serta sebutkan perbandingan penghematan biaya bahan bakar di akhir iterasi.

---

## 5. Kesimpulan
Aplikasi web ini menyatukan pemodelan graf akademik, navigasi medan berbobot, dan penyelesaian logistik nyata TSP (*Traveling Salesperson*) dalam satu kesatuan kode. Berdasarkan seluruh uji kasus, sistem komputasi berhasil membuktikan bahwa A* Search senantiasa mendominasi keefisienan biaya (*Cost*) mutlak atas pendekatan sederhana (*Greedy Best-First*).
