"""
Implementasi Algoritma A* untuk Penyelesaian Traveling Salesperson Problem (TSP)
Simulasi Sistem Pengiriman Barang Logistik Multi-Tujuan
Kelompok 1 - Kecerdasan Buatan
"""

import heapq
import math

# Daftar Titik Lokasi Pengiriman (Koordinat X, Y)
# Node 0 = Gudang (Depot), Node 1..N = Titik Penerima Barang
LOKASI = {
    0: ("Gudang Logistik", (0, 0)),
    1: ("Pelanggan A (Banjarmasin Utara)", (2, 5)),
    2: ("Pelanggan B (Banjarmasin Selatan)", (5, 2)),
    3: ("Pelanggan C (Banjarmasin Barat)", (6, 7)),
    4: ("Pelanggan D (Banjarmasin Timur)", (8, 3)),
    5: ("Pelanggan E (Pelaihari Hub)", (10, 8))
}

def hitung_jarak_euclidean(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# Matriks Jarak Antar Titik
N_KOTA = len(LOKASI)
MATRIKS_JARAK = [[0.0] * N_KOTA for _ in range(N_KOTA)]
for i in range(N_KOTA):
    for j in range(N_KOTA):
        MATRIKS_JARAK[i][j] = hitung_jarak_euclidean(LOKASI[i][1], LOKASI[j][1])

def hitung_mst_prim(unvisited_nodes):
    """
    Heuristik Admissible: Minimum Spanning Tree (MST) untuk sisa node yang belum dikunjungi.
    MST menjamin nilai estimasi h(n) <= jarak sebenarnya untuk menghubungkan seluruh sisa titik.
    """
    if not unvisited_nodes:
        return 0.0

    nodes = list(unvisited_nodes)
    if len(nodes) == 1:
        return 0.0

    # Prim's Algorithm
    mst_cost = 0.0
    in_mst = {nodes[0]}
    pq = []

    for v in nodes:
        if v != nodes[0]:
            heapq.heappush(pq, (MATRIKS_JARAK[nodes[0]][v], nodes[0], v))

    while pq and len(in_mst) < len(nodes):
        cost, u, v = heapq.heappop(pq)
        if v not in in_mst:
            in_mst.add(v)
            mst_cost += cost
            for nxt in nodes:
                if nxt not in in_mst:
                    heapq.heappush(pq, (MATRIKS_JARAK[v][nxt], v, nxt))

    return mst_cost

def heuristic_tsp(current, unvisited, start_node=0):
    """
    h(n) = Jarak ke unvisited terdekat 
           + Bobot MST dari seluruh unvisited 
           + Jarak dari unvisited ke titik Gudang (start_node).
    Heuristik ini bersifat Admissible (tidak pernah overestimating).
    """
    if not unvisited:
        # Jika semua sudah dikunjungi, sisa jarak hanya kembali ke Gudang
        return MATRIKS_JARAK[current][start_node]

    # 1. Jarak dari current ke salah satu unvisited terdekat
    d_to_unvisited = min(MATRIKS_JARAK[current][u] for u in unvisited)

    # 2. Bobot MST untuk menghubungkan seluruh unvisited
    mst_weight = hitung_mst_prim(unvisited)

    # 3. Jarak dari salah satu unvisited ke depot Gudang
    d_to_depot = min(MATRIKS_JARAK[u][start_node] for u in unvisited)

    return d_to_unvisited + mst_weight + d_to_depot

def a_star_tsp(start=0):
    """
    A* Search untuk TSP:
    State direpresentasikan sebagai: (current_node, frozenset(visited_nodes))
    f(n) = g(n) + h(n)
    """
    # Open List Priority Queue: (f_score, g_score, current_node, tuple(path))
    initial_unvisited = frozenset(set(range(N_KOTA)) - {start})
    initial_h = heuristic_tsp(start, initial_unvisited, start)
    
    pq = []
    # ponytail: simpan counter unik agar tuple heapq stabil saat f sama
    counter = 0
    heapq.heappush(pq, (initial_h, 0.0, counter, start, (start,)))

    # Closed Set: menyimpan g_score terbaik untuk state (current, visited_set)
    best_g = {}

    iterasi = 0
    while pq:
        f, g, _, curr, path = heapq.heappop(pq)
        iterasi += 1

        visited_set = frozenset(path)
        state_key = (curr, visited_set)

        if state_key in best_g and best_g[state_key] < g:
            continue
        best_g[state_key] = g

        unvisited = frozenset(set(range(N_KOTA)) - set(path))

        # Goal Condition: Semua lokasi sudah dikunjungi, lalu kembali ke Gudang
        if not unvisited:
            if curr == start and len(path) == N_KOTA + 1:
                return path, g, iterasi
            # Tambahkan langkah penutup kembali ke Gudang
            g_return = g + MATRIKS_JARAK[curr][start]
            counter += 1
            heapq.heappush(pq, (g_return, g_return, counter, start, path + (start,)))
            continue

        # Ekspansi tetangga (pilih lokasi berikutnya yang belum dikunjungi)
        for nxt in unvisited:
            step_cost = MATRIKS_JARAK[curr][nxt]
            tentative_g = g + step_cost
            next_unvisited = unvisited - {nxt}
            h_next = heuristic_tsp(nxt, next_unvisited, start)
            f_next = tentative_g + h_next

            counter += 1
            heapq.heappush(pq, (f_next, tentative_g, counter, nxt, path + (nxt,)))

    return None, float('inf'), iterasi

if __name__ == "__main__":
    print("=" * 65)
    print("SIMULASI PENGIRIMAN BARANG (TSP MULTI-TUJUAN) DENGAN A* SEARCH")
    print("Kelompok 1 - Kecerdasan Buatan")
    print("=" * 65)
    print("\nDaftar Alamat Pengiriman:")
    for idx, (nama, pos) in LOKASI.items():
        print(f"  [{idx}] {nama.ljust(35)} : Koordinat {pos}")

    print("\nMenghitung rute terpendek dengan A* Search + MST Heuristic...")
    rute, total_jarak, total_iterasi = a_star_tsp(start=0)

    print("\n" + "=" * 65)
    print(f"STATUS SOLUSI     : OPTIMAL")
    print(f"TOTAL JARAK TEMPUH: {total_jarak:.3f} satuan jarak (km)")
    print(f"JUMLAH ITERASI A* : {total_iterasi} ekspansi state")
    print("=" * 65)

    print("\nUrutan Jalur Pengiriman Optimal:")
    for i in range(len(rute) - 1):
        u, v = rute[i], rute[i+1]
        jarak_segmen = MATRIKS_JARAK[u][v]
        print(f"  Langkah {i+1}: {LOKASI[u][0]} -> {LOKASI[v][0]} (Jarak: {jarak_segmen:.2f} km)")

    print(f"\nRangkuman Tur: {' -> '.join(str(n) for n in rute)}")
