from pymodbus.client import ModbusTcpClient
from robodk import robolink
from robodk.robomath import *


def run_init():
    # RoboDK 연결
    RDK = robolink.Robolink()

    # AGV 목록
    AGV = [RDK.Item(f"AGV{i+1}", robolink.ITEM_TYPE_ROBOT) for i in range(8)]

    # 위치 좌표 정의 (p0 ~ p8)
    positions = [
        [1000.000000, 1600.000000, 0.000000, 0.000000],
        [2000.000000, 1600.000000, 0.000000, 0.000000],
        [3000.000000, 1600.000000, 0.000000, 0.000000],
        [1000.000000, 800.000000, 0.000000, 0.000000],
        [2000.000000, 800.000000, 0.000000, 0.000000],
        [3000.000000, 800.000000, 0.000000, 0.000000],
        [1000.000000, 0.000000, 0.000000, 0.000000],
        [2000.000000, 0.000000, 0.000000, 0.000000],
        [3000.000000, 0.000000, 0.000000, 0.000000],
    ]

    # Modbus 연결
    client = ModbusTcpClient("127.0.0.1", port=502)
    client.connect()

    # 데이터 읽기
    rr = client.read_holding_registers(address=1, count=21, slave=1)
    if rr.isError():
        print("Modbus 오류:", rr)
    else:
        values = rr.registers  # 0~8: 초기위치 / 9~17: 목표위치

        # 각 AGV를 초기 위치로 이동
        print("[초기 위치 이동]")
        client.write_register(21, 1, slave=1)
        for idx in range(9):
            agv_index = values[idx]
            if agv_index != 0:
                AGV[agv_index - 1].MoveJ(positions[idx])
        time.sleep(1)
        client.write_register(21, 0, slave=1)

        # for idx in range(8):  # AGV1 ~ AGV8
        #     position_index = values[idx]  # 예: 1 → p1
        #     print(values)
        #     if 0 <= position_index < len(positions):
        #         AGV[idx].MoveJ(positions[position_index])
        #     else:
        #         print(f"AGV{idx+1} 잘못된 초기 위치 index: {position_index}")

        # 각 AGV를 목표 위치로 이동 (원한다면 딜레이 후)
        # print("[목표 위치 이동]")
        # for idx in range(8):  # AGV1 ~ AGV8
        #     position_index = values[idx + 9]  # 목표 위치
        #     if 0 <= position_index < len(positions):
        #         AGV[idx].MoveJ(positions[position_index])
        #     else:
        #         print(f"AGV{idx+1} 잘못된 목표 위치 index: {position_index}")
