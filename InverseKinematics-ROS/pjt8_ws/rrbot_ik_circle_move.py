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

    def draw_circle(self, cx=1.0, cz=1.0, r=0.8, omega=3.0):
        t = 0.0
        dt = 0.02  # 20Hz

        print("Starting circular motion... (Press Ctrl+C to stop)")
        try:
            while True:
                x = cx + r * math.cos(omega * t)
                z = cz + r * math.sin(omega * t)

                result = self.ik_rrbot(x, z)
                if result:
                    q1, q2 = result
                    print(f"x={x:.3f}, z={z:.3f} -> q1={q1:.3f}, q2={q2:.3f}")
                    self.send_joint_command(q1, q2)
                else:
                    print(f"Target (x={x:.3f}, z={z:.3f}) is unreachable.")

                t += dt
                time.sleep(dt)

        except KeyboardInterrupt:
            print("Circular motion stopped.")


def main(args=None):
    rclpy.init(args=args)
    node = RRBotController()
    node.draw_circle()

    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
