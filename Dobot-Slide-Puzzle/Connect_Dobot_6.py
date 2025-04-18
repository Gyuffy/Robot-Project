# Dobot API
import DobotEDU
import time

# A* Algorithm
import heapq, itertools
from typing import List, Tuple, Dict

counter = itertools.count()

GOAL_STATE: List[List[int]] = [
    [1, 2, 3],
    [4, 5, 6],
    [0, 0, 0],
]

ROWS, COLS = 3, 3
DIRS: Tuple[Tuple[int, int], ...] = ((-1, 0), (1, 0), (0, -1), (0, 1))

# Dobot의 실제 위치 맵핑
pos = [
    [65, 260, -18, 90],
    [105, 260, -18, 90],
    [145, 260, -18, 90],
    [65, 220, -18, 90],
    [105, 220, -18, 90],
    [145, 220, -18, 90],
    [65, 180, -18, 90],
    [105, 180, -18, 90],
    [145, 180, -18, 90] 
    ]

# Dobot 연결 및 데이터 가져오기
PORT = "COM3"
device = DobotEDU.dobot_magician
device.connect_dobot(PORT)
print("연결이 완료 되었습니다")

# Dobot 동작 함수
def homeing_robot():
    print("Homing 중...")
    DobotEDU.dobot_magician.set_homecmd(PORT)
    print("홈 위치 동작 완료되었습니다")

def movej(pos):
    p1 = pos[0]
    p2 = pos[1]
    p3 = pos[2]
    p4 = pos[3]
    DobotEDU.dobot_magician.set_ptpcmd(PORT, ptp_mode=4, x=p1, y=p2, z=p3, r=p4)
    time.sleep(0.5)
    print("movej 실행 완료")

def movejp(pos):
    p1 = pos[0]
    p2 = pos[1]
    p3 = pos[2]
    p4 = pos[3]
    DobotEDU.dobot_magician.set_ptpcmd(PORT, ptp_mode=0, x=p1, y=p2, z=p3, r=p4)
    time.sleep(0.5)
    print("movejp 실행 완료")

def grip():
    DobotEDU.dobot_magician.set_endeffector_gripper(PORT, enable=True, on=True)
    time.sleep(1)
    DobotEDU.dobot_magician.set_endeffector_gripper(PORT, enable=False, on=False)
    print("Grip!")

def ungrip():
    DobotEDU.dobot_magician.set_endeffector_gripper(PORT, enable=True, on=False)
    time.sleep(0.5)
    DobotEDU.dobot_magician.set_endeffector_gripper(PORT, enable=False, on=False)
    print("Ungrip!")

# Algorithm 구현 함수
def cell_id(r, c):
    return r * 3 + c

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
    pq = []
    visited = set()
    heapq.heappush(pq, (manhattan_distance(start), 0,
                        next(counter), start, []))

    while pq:
        f, g, _, cur, path = heapq.heappop(pq)
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
                heapq.heappush(
                    pq,
                    (g + 1 + h, g + 1,
                     next(counter), nxt, path + [mv])
                )
    return []

# 메인
if __name__ == "__main__":
    start_state = [
        [0, 6, 1],
        [0, 2, 3],
        [0, 4, 5],
    ]
    moves = solve_puzzle(start_state)

    homeing_robot()
    ungrip()

    gripped = False

    for idx, m in enumerate(moves, 1):
        print(f"{idx:02d}. tile {m['tile']} : {m['from']} → {m['to']}")
        movejp(pos[m["from"]])

        if (not gripped):
            grip()
            gripped = True
        if (idx < len(moves) and moves[idx]['tile'] == m['tile']):
            print("[SKIP]")
            continue
        
        movejp(pos[m["to"]])
        ungrip()
        gripped = False

    movejp([200, 0, 20, 90])
    print("총 이동 수:", len(moves))