import heapq

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(grid_size, start, goal, obstacles):
    # ponytail: grid 4-arah seragam cost 1. Upgrade ke bobot jalan jika butuh simulasi macet dinamis.
    open_set = []
    heapq.heappush(open_set, (0, start))
    
    came_from = {}
    g_score = {start: 0}
    f_score = {start: manhattan(start, goal)}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        x, y = current
        neighbors = [(x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y)]

        for nxt in neighbors:
            nx, ny = nxt
            if 0 <= nx < grid_size and 0 <= ny < grid_size and nxt not in obstacles:
                tentative_g = g_score[current] + 1
                
                if tentative_g < g_score.get(nxt, float('inf')):
                    came_from[nxt] = current
                    g_score[nxt] = tentative_g
                    f_score[nxt] = tentative_g + manhattan(nxt, goal)
                    heapq.heappush(open_set, (f_score[nxt], nxt))
                    
    return []

def cetak_grid(grid_size, start, goal, obstacles, path):
    path_set = set(path)
    print("\nVisualisasi Peta Pengiriman:")
    for y in range(grid_size):
        baris = ""
        for x in range(grid_size):
            pt = (x, y)
            if pt == start:
                baris += " S "
            elif pt == goal:
                baris += " G "
            elif pt in obstacles:
                baris += " # "
            elif pt in path_set:
                baris += " . "
            else:
                baris += " - "
        print(baris)
    print("Ket: S=Start, G=Goal, #=Rintangan, .=Jalur A*\n")

if __name__ == "__main__":
    ukuran = 8
    gudang = (0, 0)
    tujuan = (7, 7)
    rintangan = {
        (2, 1), (2, 2), (2, 3),
        (5, 4), (5, 5), (5, 6),
        (3, 4), (4, 4)
    }

    rute = a_star(ukuran, gudang, tujuan, rintangan)
    
    assert len(rute) > 0, "Rute harus ditemukan"
    assert rute[0] == gudang and rute[-1] == tujuan, "Rute harus valid dari start ke goal"

    print("=== SIMULASI SISTEM PENGIRIMAN BARANG (A* SEARCH) ===")
    print(f"Kelompok : 1")
    print(f"Gudang   : {gudang}")
    print(f"Tujuan   : {tujuan}")
    print(f"Rute     : {rute}")
    print(f"Langkah  : {len(rute) - 1}")
    cetak_grid(ukuran, gudang, tujuan, rintangan, rute)
