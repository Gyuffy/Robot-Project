from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
import logging

#LOG 출력
logging.basicConfig()
log=logging.getLogger()
log.setLevel(logging.DEBUG)
###

#Modbus Data Black (HR) 0~10까지 생성을 하고 각 자리에 0~9까지 값을 입력
'''
hr_block=ModbusSlaveContext(
    hr=ModbusSequentialDataBlock(0,[i for i in range(0,100)])
)
'''
#di : Discrete input (읽기 전용| 0 1)
#co : Coils (읽기,쓰기 | 0 1)
#ir : Input Registers(읽기 전용 | 0 65535) 
#hr : Holdung Registers(읽기,쓰기 | 0~65535)

store_unint1= ModbusSlaveContext(
    di=ModbusSequentialDataBlock(0, [0]*10),
    co=ModbusSequentialDataBlock(0, [0]*10),
    ir=ModbusSequentialDataBlock(0, [0]*100),
    hr=ModbusSequentialDataBlock(0, [0]*1000)
)

context=ModbusServerContext(slaves={1: store_unint1}, single=False)

StartTcpServer(context=context, address=("127.0.0.1",502))