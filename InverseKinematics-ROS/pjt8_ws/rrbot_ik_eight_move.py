import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray

import math
import time


class RRBotController(Node):
    def __init__(self):
        super().__init__("rrbot_controller")

        self.publisher = self.create_publisher(
            Float64MultiArray, "/forward_position_controller/commands", 10
        )

        self.BASE_HEIGHT = 2.0
        self.L1 = 1.0
        self.L2 = 1.0

    def ik_rrbot(self, x, z):
        # 목표 지점까지의 거리
        r = math.sqrt(x**2 + z**2)

        # 도달할 수 없는 위치인 경우
        if r > self.L1 + self.L2 or r < abs(self.L1 - self.L2):
            return None

        # Law of cosines for q2
        cos_q2 = (r**2 - self.L1**2 - self.L2**2) / (2 * self.L1 * self.L2)
        q2 = math.acos(cos_q2)  # elbow-down 방식

        # Law of cosines for q1
        k1 = self.L1 + self.L2 * math.cos(q2)
        k2 = self.L2 * math.sin(q2)
        q1 = math.atan2(x, z) - math.atan2(k2, k1)
        return q1, q2

    def send_joint_command(self, q1, q2):
        msg = Float64MultiArray()
        msg.data = [q1, q2]
        self.publisher.publish(msg)
        print(f"Joint command sent: [q1={q1:.4f}, q2={q2:.4f}]")

    def draw_eight(self, cx=1.0, cz=1.0, A=0.5, B=0.5, omega=3.0):
        """
        ∞ 모양 (infinity path)을 그리는 동작
        cx, cz: 중심 위치
        A, B: 각각 x, z 방향의 크기
        omega: 회전 속도
        """
        t = 0.0
        dt = 0.05

        print("Starting ∞ path motion... (Ctrl+C to stop)")

        try:
            while True:
                x = cx + A * math.sin(omega * t)
                z = cz + B * math.sin(omega * t) * math.cos(omega * t)  # Lemniscate

                result = self.ik_rrbot(x, z)
                if result:
                    q1, q2 = result
                    print(
                        f"x={x:.3f}, z={z:.3f} -> q1={math.degrees(q1):.1f}°, q2={math.degrees(q2):.1f}°"
                    )
                    self.send_joint_command(q1, q2)
                else:
                    print(f"Unreachable: x={x:.3f}, z={z:.3f}")

                t += dt
                time.sleep(dt)

        except KeyboardInterrupt:
            print("∞ path motion stopped.")


def main(args=None):
    rclpy.init(args=args)
    node = RRBotController()
    node.draw_eight()

    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
