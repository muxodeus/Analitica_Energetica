# simulator/server.py
from pymodbus.server.sync import StartTcpServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.device import ModbusDeviceIdentification

context = ModbusServerContext(slaves={
    1: ModbusSlaveContext(
        ir=ModbusSequentialDataBlock(0, [100, 200, 300, 400]), zero_mode=True
    ),
    2: ModbusSlaveContext(
        ir=ModbusSequentialDataBlock(0, [500, 600, 700, 800]), zero_mode=True
    ),
    3: ModbusSlaveContext(
        ir=ModbusSequentialDataBlock(0, [900, 1000, 1100, 1200]), zero_mode=True
    ),
}, single=False)

StartTcpServer(context, address=("0.0.0.0", 1502))
