import heapq
from typing import List, Tuple, Dict

GOAL_STATE: List[List[int]] = [
    [1, 2, 3],
    [4, 0, 0],
    [0, 0, 0],
]

ROWS, COLS = 3, 3
DIRS: Tuple[Tuple[int, int], ...] = ((-1, 0), (1, 0), (0, -1), (0, 1))

def cell_id(r, c):
    return r * 3 + c          # 3×3 고정이므로 COLS 생략 가능

def manhattan_distance(state: List[List[int]]) -> int:
    dist = 0
    for i in range(ROWS):
        for j in range(COLS):
            val = state[i][j]
            if val:                             # 0은 빈칸
                goal_x = (val - 1) // COLS
                goal_y = (val - 1) % COLS
                dist += abs(i - goal_x) + abs(j - goal_y)
    return dist


def serialize(state: List[List[int]]) -> str:
    return ''.join(str(num) for row in state for num in row)


def get_neighbors(state: List[List[int]]) -> List[Tuple[List[List[int]], Dict]]:
    """(다음 상태, 이동 정보) 반환"""
    blanks = [(i, j) for i in range(ROWS) for j in range(COLS) if state[i][j] == 0]
    out: List[Tuple[List[List[int]], Dict]] = []

    for x, y in blanks:
        for dx, dy in DIRS:
            nx, ny = x + dx, y + dy
            if 0 <= nx < ROWS and 0 <= ny < COLS and state[nx][ny] != 0:
                new_state = [row[:] for row in state]
                tile_val = new_state[nx][ny]
                new_state[x][y], new_state[nx][ny] = tile_val, 0
                move_info = {
                    'tile': tile_val,
                    'from': cell_id(nx, ny),
                    'to':   cell_id(x,  y),
                }
                out.append((new_state, move_info))
    return out


def solve_puzzle(start: List[List[int]]) -> List[Dict]:
    pq: List[Tuple[int, int, List[List[int]], List[Dict]]] = []
    visited = set()
    heapq.heappush(pq, (manhattan_distance(start), 0, start, []))

    while pq:
        f, g, cur, path = heapq.heappop(pq)
        key = serialize(cur)
        if key in visited:
            continue
        visited.add(key)

        if cur == GOAL_STATE:
            return path

        for nxt, mv in get_neighbors(cur):
            k = serialize(nxt)
            if k not in visited:
                h = manhattan_distance(nxt)
                heapq.heappush(pq, (g + 1 + h, g + 1, nxt, path + [mv]))
    return []


if __name__ == "__main__":
    start_state = [
        [0, 1, 3],
        [4, 2, 0],
        [0, 0, 0],
    ]
    moves = solve_puzzle(start_state)

    for idx, m in enumerate(moves, 1):
        print(f"{idx:02d}. tile {m['tile']} : {m['from']} → {m['to']}")
    print("총 이동 수:", len(moves))
