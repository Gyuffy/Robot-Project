from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
import logging

# Log 출력
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

store_uint1 = ModbusSlaveContext(
    # di=ModbusSequentialDataBlock(0, [0]*10),
    # co=ModbusSequentialDataBlock(0, [0]*10),
    # ir=ModbusSequentialDataBlock(0, [0]*10),
    hr=ModbusSequentialDataBlock(0, [0]*1000)
)

context = ModbusServerContext(slaves={1: store_uint1}, single=False)

StartTcpServer(context=context, address=("127.0.0.1", 502))