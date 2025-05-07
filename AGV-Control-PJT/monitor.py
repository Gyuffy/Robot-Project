import sys
import time
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout,
)
from PyQt5.QtCore import QTimer
from pymodbus.client import ModbusTcpClient


class ModbusDisplay(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initModbus()

    def initUI(self):
        self.setWindowTitle("통합 관제 서버")

        main_layout = QVBoxLayout()

        # 초기값 레이아웃
        self.init_labels = []
        init_layout = QGridLayout()
        for i in range(9):
            label = QLabel("0")
            label.setStyleSheet(
                "background-color: #dceeff; font-size: 25px; padding: 10px; text-align: center;"
            )
            label.setFixedSize(80, 50)
            self.init_labels.append(label)
            init_layout.addWidget(label, i // 3, i % 3)

        # 목표값 레이아웃
        self.goal_labels = []
        goal_layout = QGridLayout()
        for i in range(9):
            label = QLabel("0")
            label.setStyleSheet(
                "background-color: #dceeff; font-size: 25px; padding: 10px; text-align: center;"
            )
            label.setFixedSize(80, 50)
            self.goal_labels.append(label)
            goal_layout.addWidget(label, i // 3, i % 3)

        # 로봇 상태 레이아웃
        self.status_label = QLabel("준비중")
        self.status_label.setStyleSheet(
            "background-color: #dceeff; font-size: 25px; padding: 10px;"
        )
        self.status_label.setFixedHeight(50)

        main_layout.addLayout(init_layout)
        main_layout.addLayout(goal_layout)
        main_layout.addWidget(self.status_label)

        self.setLayout(main_layout)

        # Timer for update
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateData)
        self.timer.start(1000)  # 1초 간격

    def initModbus(self):
        self.client = ModbusTcpClient("127.0.0.1", port=502)
        self.client.connect()

    def updateData(self):
        if not self.client.connect():
            print("Modbus 서버 연결 실패")
            return

        rr = self.client.read_holding_registers(address=1, count=21, slave=1)
        if rr.isError():
            print("Modbus 오류")
            return

        values = rr.registers

        for i in range(9):
            self.init_labels[i].setText(str(values[i]))

        for i in range(9):
            self.goal_labels[i].setText(str(values[i + 10]))

        status_value = values[20]
        status_text = {
            0: "준비중",
            1: "초기 운전 중",
            2: "미로찾기 수행중",
            3: "작업완료",
        }.get(status_value, "알 수 없음")

        self.status_label.setText(status_text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ModbusDisplay()
    window.show()
    sys.exit(app.exec_())
