import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QLabel,
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
)
from PyQt5.QtCore import Qt
from pymodbus.client import ModbusTcpClient
from init_operation import run_init
from move_pos import run_move


class ModbusDisplay(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("통합 관제 서버")
        self.init_input_value = 0
        self.target_input_value = 0
        self.init_values = [None] * 9
        self.target_values = [None] * 9
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        title = QLabel("통합 관제 서버")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 28px")
        main_layout.addWidget(title)

        top_layout = QHBoxLayout()
        bottom_layout = QHBoxLayout()
        agv_control_layout = QHBoxLayout()

        # 초기값 영역
        self.init_buttons = []
        self.init_displays = []
        init_button_box = self.create_button_display_group(
            "초기값 입력창", self.init_buttons, self.handle_init_button
        )
        init_display_box = self.create_display_group("초기값", self.init_displays)
        top_layout.addWidget(init_button_box)
        top_layout.addWidget(init_display_box)

        init_control_layout = QHBoxLayout()
        send_init_btn = QPushButton("초기값 전송")
        send_init_btn.clicked.connect(self.send_init_values)
        reset_init_btn = QPushButton("초기값 리셋")
        reset_init_btn.clicked.connect(self.reset_init_display)
        init_control_layout.addWidget(send_init_btn)
        init_control_layout.addWidget(reset_init_btn)
        top_layout.addLayout(init_control_layout)

        # 목표값 영역
        self.target_buttons = []
        self.target_displays = []
        target_button_box = self.create_button_display_group(
            "목표값 입력창", self.target_buttons, self.handle_target_button
        )
        target_display_box = self.create_display_group("목표값", self.target_displays)
        bottom_layout.addWidget(target_button_box)
        bottom_layout.addWidget(target_display_box)

        target_control_layout = QHBoxLayout()
        send_target_btn = QPushButton("목표전송")
        send_target_btn.clicked.connect(self.send_target_values)
        reset_target_btn = QPushButton("목표리셋")
        reset_target_btn.clicked.connect(self.reset_target_display)
        target_control_layout.addWidget(send_target_btn)
        target_control_layout.addWidget(reset_target_btn)
        bottom_layout.addLayout(target_control_layout)

        main_layout.addLayout(top_layout)
        main_layout.addLayout(bottom_layout)
        self.setLayout(main_layout)

        move_init_btn = QPushButton("초기 위치 이동")
        move_init_btn.clicked.connect(self.move_agv_to_init_positions)
        move_target_btn = QPushButton("목표 위치 이동")
        move_target_btn.clicked.connect(self.move_agv_to_target_positions)
        agv_control_layout.addWidget(move_init_btn)
        agv_control_layout.addWidget(move_target_btn)
        main_layout.addLayout(agv_control_layout)

    def create_button_display_group(self, title, button_list, handler):
        box = QGroupBox(title)
        layout = QGridLayout()
        for i in range(3):
            for j in range(3):
                index = i * 3 + j
                btn = QPushButton("버튼")
                btn.setStyleSheet("background-color: lightblue")
                btn.clicked.connect(lambda _, idx=index: handler(idx))
                button_list.append(btn)
                layout.addWidget(btn, i, j)
        box.setLayout(layout)
        return box

    def create_display_group(self, title, display_list):
        box = QGroupBox(title)
        layout = QGridLayout()
        for i in range(3):
            for j in range(3):
                disp = QLabel("디스플레이")
                disp.setAlignment(Qt.AlignCenter)
                disp.setStyleSheet("background-color: lightgray; padding: 10px")
                display_list.append(disp)
                layout.addWidget(disp, i, j)
        box.setLayout(layout)
        return box

    def handle_init_button(self, idx):
        if self.init_values[idx] is None and self.init_input_value <= 8:
            self.init_values[idx] = self.init_input_value
            self.init_displays[idx].setText(str(self.init_input_value))
            self.init_input_value += 1

    def handle_target_button(self, idx):
        if self.target_values[idx] is None and self.target_input_value <= 8:
            self.target_values[idx] = self.target_input_value
            self.target_displays[idx].setText(str(self.target_input_value))
            self.target_input_value += 1

    def reset_init_display(self):
        self.init_input_value = 0
        self.init_values = [None] * 9
        for display in self.init_displays:
            display.setText("디스플레이")

    def reset_target_display(self):
        self.target_input_value = 0
        self.target_values = [None] * 9
        for display in self.target_displays:
            display.setText("디스플레이")

    def send_init_values(self):
        client = ModbusTcpClient("127.0.0.1", port=502)
        client.connect()
        for i, value in enumerate(self.init_values):
            val = value if value is not None else 0
            client.write_register(i + 1, val, slave=1)
        client.close()

    def send_target_values(self):
        client = ModbusTcpClient("127.0.0.1", port=502)
        client.connect()
        for i, value in enumerate(self.target_values):
            val = value if value is not None else 0
            client.write_register(i + 11, val, slave=1)
        client.close()

    def move_agv_to_init_positions(self):
        run_init()

    def move_agv_to_target_positions(self):
        # subprocess.Popen(["python", "move_pos.py"])
        run_move()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ModbusDisplay()
    window.show()
    sys.exit(app.exec_())
