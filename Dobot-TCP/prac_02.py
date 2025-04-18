import DobotEDU
import time
import socket

def connect_robot(NUM):
    DobotEDU.dobot_magician.connect_dobot(NUM)
    print("연결이 완료 되었습니다 !!")

def disconnect_robot(NUM):
    DobotEDU.dobot_magician.disconnect_dobot(NUM)

def homeing_robot(NUM):
    DobotEDU.dobot_magician.set_homecmd(NUM)
    print("홈 위치 동작 완료되었습니다 !!")

def vacuum_on(NUM):
    DobotEDU.dobot_magician.set_endeffector_suctioncup(NUM, enable=True, on=True)
    time.sleep(0.5)

def vacuum_off(NUM):
    DobotEDU.dobot_magician.set_endeffector_suctioncup(NUM,enable=False, on=False)
    time.sleep(0.5)

def grip():
    DobotEDU.dobot_magician.set_endeffector_gripper(PORT,enable=True, on=True)#Grip
    time.sleep(2)
    DobotEDU.dobot_magician.set_endeffector_gripper(PORT,enable=False, on=False)

def ungrip():
    DobotEDU.dobot_magician.set_endeffector_gripper(PORT,enable=True, on=False)#Grip
    time.sleep(2)
    DobotEDU.dobot_magician.set_endeffector_gripper(PORT,enable=False, on=False)


def Movej(NUM,p1,p2,p3,p4):
    DobotEDU.dobot_magician.set_ptpcmd(NUM, ptp_mode=4, x=p1 , y=p2 , z=p3 ,r=p4 )

def set_digital(NUM1,NUM2,NUM3): #18번 또는 19번
    # DobotEDU.dobot_magician.set_iomultiplexing(NUM1, 18, 1)
    DobotEDU.dobot_magician.set_iodo(NUM1, port=NUM2, level=NUM3)#ON
    print("~~~~")





def start_server():
    host='127.0.0.1'
    port=20000
    server_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host,port))
    server_socket.listen(1)
    print(f"서버오픈중입니다. {host}:{port}에서 대기중입니다...")

    client_socket, addr =server_socket.accept()
    print(f"{addr}가 연결됨 !!!")
    while True :
        data=client_socket.recv(1024).decode('utf-8')
        if not data:
            print("클라이언트가 연결을 종료했습니다..!!")
            break
        print(f"클라이언트 메세지: {data}")

        if data.strip().lower() == "run": #Run, RUn ruN 전부 소문자 처리
            print("RUN 메세지 수신!!")
            break
    
    client_socket.close()
    server_socket.close()
    print("서버가 종료가 되었습니다.")

PORT='COM3'
connect_robot(PORT)
#vacuum_on(PORT)
# homeing_robot(PORT)

#grip()
set_digital(PORT,18,1)
time.sleep(4)
#ungrip()
set_digital(PORT,18,0)#16
time.sleep(2)


#vacuum_off(PORT)

disconnect_robot(PORT)

'''
#start_server()
homeing_robot(PORT)

vacuum_on(PORT)
time.sleep(5)
vacuum_off(PORT)
disconnect_robot(PORT)


#Movej(PORT,10,10,10,0)
#set_digital(PORT,1,1)
#time.sleep(1)
#set_digital(PORT,1,0)

'''

