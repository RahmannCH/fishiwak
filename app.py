import heapq

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(grid_size, start, goal, obstacles):
    # Contoh grid seragam 4-arah dengan cost langkah 1.
    # Varian medan berbobot (aspal/lumpur/sungai) diimplementasikan di index.html modul Grid.
    if start == goal:
        return [start]
    for pt, nama in ((start, "Start"), (goal, "Goal")):
        if not (0 <= pt[0] < grid_size and 0 <= pt[1] < grid_size):
            print(f"{nama} {pt} di luar grid.")
            return []
    if start in obstacles or goal in obstacles:
        print("Start/Goal tidak boleh berada di atas rintangan.")
        return []

    open_set = []
    counter = 0
    heapq.heappush(open_set, (manhattan(start, goal), 0, counter, start))

    came_from = {}
    g_score = {start: 0}
    closed = set()

    while open_set:
        _, _, _, current = heapq.heappop(open_set)
        if current in closed:
            continue
        closed.add(current)

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
                    f = tentative_g + manhattan(nxt, goal)
                    counter += 1
                    heapq.heappush(open_set, (f, -tentative_g, counter, nxt))

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

    if not rute:
        print("Tidak ada rute dari gudang ke tujuan (jalur tertutup rintangan).")
    elif rute[0] != gudang or rute[-1] != tujuan:
        print("Rute tidak valid dari start ke goal.")
    else:
        print("=== SIMULASI SISTEM PENGIRIMAN BARANG (A* SEARCH) ===")
        print(f"Kelompok : 1")
        print(f"Gudang   : {gudang}")
        print(f"Tujuan   : {tujuan}")
        print(f"Rute     : {rute}")
        print(f"Langkah  : {len(rute) - 1}")
        cetak_grid(ukuran, gudang, tujuan, rintangan, rute)
