import DobotEDU
import time
from robodk import robolink    # RoboDK API
from robodk import robomath    # Robot toolbox
RDK = robolink.Robolink()

from robodk import *      # RoboDK API
from robolink import *    # Robot toolbox

# Dobot 연결 및 데이터 가져오기
PORT = "COM3"
device = DobotEDU.dobot_magician
device.connect_dobot(PORT)
print("연결이 완료 되었습니다")

Dobot = RDK.Item("Dobot", 2)

def movej(pos):
    p1 = pos[0]
    p2 = pos[1]
    p3 = pos[2]
    p4 = pos[3]
    DobotEDU.dobot_magician.set_ptpcmd(PORT, ptp_mode=4, x=p1, y=p2, z=p3, r=p4)
    time.sleep(0.5)
    print("movej 실행 완료")

def homeing_robot():
    DobotEDU.dobot_magician.set_homecmd(PORT)
    print("홈 위치 동작 완료되었습니다")

def grip():
    DobotEDU.dobot_magician.set_endeffector_gripper(PORT, enable=True, on=True)
    time.sleep(2)
    DobotEDU.dobot_magician.set_endeffector_gripper(PORT, enable=False, on=False)
    print("grip!")

def ungrip():
    DobotEDU.dobot_magician.set_endeffector_gripper(PORT, enable=True, on=False)
    time.sleep(1)
    DobotEDU.dobot_magician.set_endeffector_gripper(PORT, enable=False, on=False)
    print("ungrip!")

# homeing_robot()

# grip()
# ungrip()

while True:
    P1 = [-24.35, 32.49, 25.63, 0.0]
    Dobot.MoveJ(P1)
    movej(P1)

    P2 = [15.33, 30.39, 25.41, 0.0]
    Dobot.MoveJ(P2)
    movej(P2)
