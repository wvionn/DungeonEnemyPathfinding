# Tugas 1 - Dungeon Enemy Pathfinding

> Implementasi deteksi dan pergerakan Enemy menuju Player menggunakan Finite State Machine (FSM), Algoritma A* (A-Star), dan Steering Behaviour.

## 1. Identifikasi Algoritma

### 1.1 Calculate Distance (Euclidean Distance)
Calculate Distance digunakan untuk menghitung jarak lurus (Euclidean distance) antara posisi Enemy dan Player secara deterministik dengan rumus:
$$\text{Distance} = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}$$
Hasil perhitungan ini digunakan untuk mendeteksi apakah Player berada di dalam jangkauan deteksi (`detection_range`).

### 1.2 Finite State Machine (FSM)
FSM digunakan untuk mengatur status dan perilaku Enemy berdasarkan jarak:
- **`STATE IDLE`** : Enemy tetap diam/menunggu ketika jarak Player > `detection_range`.
- **`STATE CHASE`** : Enemy beralih mengejar Player ketika jarak Player $\le$ `detection_range`.

### 1.3 Pathfinding & A* (A-Star Algorithm)
- **Pathfinding** : Digunakan untuk mencari rute melewati rintangan / obstacle di dungeon map.
- **Algoritma A\*** : Menghitung rute terpendek dari Enemy ke Player secara optimal menggunakan fungsi evaluasi:
  $$f(n) = g(n) + h(n)$$
  - $g(n)$: Biaya langkah dari start ke node $n$.
  - $h(n)$: Heuristik Manhattan Distance dari node $n$ ke target Player.

### 1.4 Steering Behaviour
Steering Behaviour mengeksekusi pergerakan langkah demi langkah setelah jalur A* ditemukan dengan urutan:
1. **Calculate Direction** : $\text{Direction} = \text{Target} - \text{Current}$
2. **Calculate Velocity** : $\text{Velocity} = \text{Direction}$
3. **Update Position** : $\text{Position}_{\text{baru}} = \text{Position}_{\text{lama}} + \text{Velocity}$

---

## 2. Flowchart 

```mermaid
flowchart TD
    Start(["● Start"]) --> InputPlayer["Input posisi Player"]
    InputPlayer --> InputEnemy["Input posisi Enemy"]
    InputEnemy --> CalcDist["Calculate Distance"]

    CalcDist --> InRange{"Player dalam detection range?"}

    %% Jalur CHASE
    InRange -- YA --> StateChase["FSM = STATE CHASE"]
    StateChase --> AStar["Pathfinding menggunakan A* untuk mencari rute terpendek menuju Player"]
    AStar --> PathFound{"Jalur ditemukan?"}

    %% Jalur A* Ditemukan
    PathFound -- YA --> CalcDir["Calculate Direction menuju node berikutnya"]
    CalcDir --> CalcVel["Calculate Velocity untuk pergerakan Enemy"]
    CalcVel --> UpdatePos["Update posisi Enemy"]

    %% Jalur A* Tidak Ditemukan
    PathFound -- TIDAK --> PathNotFound["Jalur tidak ditemukan"]
    PathNotFound --> StateIdle2["FSM = STATE IDLE"]

    %% Jalur IDLE
    InRange -- TIDAK --> StateIdle1["FSM = STATE IDLE"]

    %% Penggabungan ke Loop Game
    UpdatePos --> CheckRunning{"Game masih berjalan?"}
    StateIdle2 --> CheckRunning
    StateIdle1 --> CheckRunning

    CheckRunning -- YA --> CalcDist
    CheckRunning -- TIDAK --> End(["● End"])
