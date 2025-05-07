from pymodbus.client import ModbusTcpClient

client = ModbusTcpClient("127.0.0.1", port=502)
client.connect()

def get_sig(num): # 원하는 주소
    result = client.read_holding_registers(address=num, count=1, slave=1)

    print("서버에서 읽어온 값은...")
    print(f"데이터 값 ->>>>> {result.registers[0]}")

def set_sig(num1,data): # 주소, 쓰고자 하는 데이터
    client.write_register(address=num1, value=data, slave=1)

get_sig(0) #j1
get_sig(1) #j2
get_sig(2) #j3
get_sig(3) #j4

get_sig(10) #x
get_sig(11) #y
get_sig(12) #z
get_sig(13) #r

client.close()