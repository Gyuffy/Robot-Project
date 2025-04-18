import DobotEDU
import time
import socket

PORT = 'COM3'

tx = 0
ty = 0
tz = 0
tr = 0

def start_server():
    global tx
    global ty
    global tz
    global tr
    host = '127.0.0.1'
    port = 20000
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"서버 오픈 중입니다 {host}:{port}에서 대기 중입니다...")

    client_socket, addr = server_socket.accept()
    print(f"{addr}가 연결됨")
    while True:
        data = client_socket.recv(1024).decode('utf-8')
        if not data:
            print("클라이언트가 연결을 종료했습니다")
            break
        print(f"클라이언트 메세지: {data}")

        if data.strip().lower() == "run":   # 띄어쓰기 및 대문자를 소문자로 변환하여 파싱
            print("RUN 메세지 수신")
            break

        if data.strip().lower() == "part1":
            print("part1 메시지 수신")
            tx = 60.9
            ty = -244.3
            tz = -22.9
            tr = -35.9
            break

        if data.strip().lower() == "part2":
            print("part2 메시지 수신")
            tx = 99.5
            ty = -245.7
            tz = -17.7
            tr = -27.9
            break

        if data.strip().lower() == "part3":
            print("part3 메시지 수신")
            tx = 140.5
            ty = -243.9
            tz = -17.3
            tr = -20.0
            break

    client_socket.close()
    server_socket.close()
    print("서버가 종료 되었습니다")

def connect_robot():
    DobotEDU.dobot_magician.connect_dobot(PORT)
    print("연결이 완료 되었습니다")

def disconnect_robot():
    DobotEDU.dobot_magician.disconnect_dobot(PORT)
    print("연결을 종료했습니다")

def homeing_robot():
    DobotEDU.dobot_magician.set_homecmd(PORT)
    print("홈 위치 동작 완료되었습니다")

def vacuum_on():
    DobotEDU.dobot_magician.set_endeffector_suctioncup(PORT, enable=True, on=True)
    time.sleep(0.5)

def vacuum_off():
    DobotEDU.dobot_magician.set_endeffector_suctioncup(PORT, enable=False, on=False)
    time.sleep(0.5)

def grip():
    DobotEDU.dobot_magician.set_endeffector_gripper(PORT, enable=True, on=True)
    time.sleep(2)
    DobotEDU.dobot_magician.set_endeffector_gripper(PORT, enable=False, on=False)

def ungrip():
    DobotEDU.dobot_magician.set_endeffector_gripper(PORT, enable=True, on=False)
    time.sleep(1)
    DobotEDU.dobot_magician.set_endeffector_gripper(PORT, enable=False, on=False)

def movej(p1, p2, p3, p4):
    DobotEDU.dobot_magician.set_ptpcmd(PORT, ptp_mode=1, x=p1, y=p2, z=p3, r=p4)
    time.sleep(0.5)
    
def movel(p1, p2, p3, p4):
    DobotEDU.dobot_magician.set_ptpcmd(PORT, ptp_mode=2, x=p1, y=p2, z=p3, r=p4)
    time.sleep(0.5)

def set_digital(PORT_NUM, LEV):
    DobotEDU.dobot_magician.set_iodo(PORT, port=PORT_NUM, level=LEV)

start_server()
connect_robot()
homeing_robot()
# movej(0, 0, 0, 0)
time.sleep(2)
grip()
time.sleep(3)
ungrip()
print(f"{tx}, {ty}, {tz}, {tr}")
movej(200.0, -150.0, 30.0, -30.0)
movej(tx, ty, 0.0, tr)
movej(tx, ty, tz, tr)
grip()
movej(tx, ty, 0.0, tr)
time.sleep(1)
movej(tx, ty, tz, tr)
ungrip()
movej(tx, ty, 0.0, tr)
# vacuum_on()
# vacuum_off()
# grip()
# ungrip()
set_digital(1, 1)
time.sleep(1)
set_digital(1, 0)
