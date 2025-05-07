from collections import deque

#퍼즐 상태에서 가능한 방향
MOVE= {
  0:[1,3],
  1:[0,2,4],
  2:[1,5],
  3:[0,4,6],
  4:[1,3,5,7],
  5:[2,4,8],
  6:[3,7],
  7:[4,6,8],
  8:[5,7]
}

def bfs_sliding_puzzle(start):
  queue = deque([(start, "", start.index("0"))]) #현재 상태, 이동 경로, 빈칸 위치)
  visited=set()

  while queue:
    state, path, zero_pos= queue.popleft()
    if state == TARGET: # 목표 상태 도달
      return path
    
    if state in visited:
      continue

    visited.add(state)

    for i in MOVE[zero_pos]:
      new_state= list(state)
      new_state[zero_pos], new_state[i] = new_state[i], new_state[zero_pos]
      #빈칸이랑 숫자랑 교환
      new_state_str="".join(new_state)

      if new_state_str not in visited:
        queue.append((new_state_str, path + str(i), i)) #새로운 상태를 저장

  return "해결불가" 

#실행
#목표상태
TARGET="123456780"


initial_state="123456078" #현재 상태, 중앙에 0(빈칸)이 있는 상태
solution = bfs_sliding_puzzle(initial_state) 


if solution != "해결불가":
  print(f"최단 경로: {solution}")
else:
  print("해결할 수 없는 퍼즐!")

