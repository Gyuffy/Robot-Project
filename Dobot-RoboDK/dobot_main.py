from pymodbus.client import ModbusTcpClient
import DobotEDU

client = ModbusTcpClient("127.0.0.1", port=502)
client.connect()

# Dobot 연결 및 데이터 가져오기
PORT = "COM3"
device = DobotEDU.dobot_magician
device.connect_dobot(PORT)
print("연결이 완료 되었습니다")

# 관절값 읽어서 Modbus에 주기적으로 저장
def get_posj(NUM):
    a=DobotEDU.dobot_magician.get_pose(NUM)
    print(a)
    print(a['jointAngle'])

def get_posl(NUM):
    a=DobotEDU.dobot_magician.get_pose(NUM)
    print(a)
    print(a['x'])
    print(a['y'])
    print(a['z'])
    print(a['r'])

def set_sig(num1,data): # 주소, 쓰고자 하는 데이터
    client.write_register(address=num1, value=data, slave=1)

a = device.get_pose(PORT)
print (a)
# print(a['jointAngle'])
# print(a['x'], a['y'], a['z'], a['r'])
set_sig(0, int(abs(a['jointAngle'][0])))
set_sig(1, int(abs(a['jointAngle'][1])))
set_sig(2, int(abs(a['jointAngle'][2])))
set_sig(3, int(abs(a['jointAngle'][3])))

set_sig(10, int(abs(a['x'])))
set_sig(11, int(abs(a['y'])))
set_sig(12, int(abs(a['z'])))
set_sig(13, int(abs(a['r'])))

device.disconnect_dobot(PORT)
print("연결을 종료했습니다")
client.close()
