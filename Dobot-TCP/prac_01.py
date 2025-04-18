import DobotEDU
import time
import socket

PORT = 'COM3'

def start_server():
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
    time.sleep(2)
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
movel(174.1, 167.0, 11.8, 90.0)
movej(69.6, 261.8, 0.0, 90.0)
movej(109.4, 259.4, -16.8, 90.0)
movej(109.4, 259.4, 0.0, 90.0)
movej(68.6, 222.4, -20.2, 90.0)
movej(68.6, 222.4, 0.0, 90.0)
movej(107.4, 221.1, -18.1, 90.0)
movej(107.4, 221.1, 0.0, 90.0)
movej(149.2, 217.7, -19.6, 90.0)
movej(149.2, 217.7, 0.0, 90.0)
movej(69.5, 182.8, -18.3, 90.0)
movej(69.5, 182.8, 0.0, 90.0)
movej(107.1, 179.6, -19.7, 90.0)
movej(107.1, 179.6, 0.0, 90.0)
movej(149.6, 177.5, -21.8, 90.0)
# vacuum_on()
# vacuum_off()
grip()
# ungrip()
set_digital(1, 1)
time.sleep(1)
set_digital(1, 0)
