import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray

import math


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


def main(args=None):
    rclpy.init(args=args)
    node = RRBotController()

    while True:
        try:
            x = float(
                input(
                    "Enter x coordinate (horizontal, 0 is at base center, right is positive): "
                )
            )

            z = float(
                input(
                    "Enter z coordinate (vertical, 0 is at base center, up is positive): "
                )
            )

        except ValueError:
            print("Invalid input. Please enter numeric values.")
            continue

        ik_result = node.ik_rrbot(x, z)
        if ik_result:
            q1, q2 = ik_result
            print(f"Input coordinates: (x={x:.4f}, z={z:.4f})")
            print(f"Joint angles (radians): [q1={q1:.4f}, q2={q2:.4f}]")
            print(
                f"Joint angles (degrees): [q1={math.degrees(q1):.4f}, q2={math.degrees(q2):.4f}]"
            )
            node.send_joint_command(q1, q2)
        else:
            print("Unable to calculate inverse kinematics for the given coordinates.")

        choice = input("Do you want to enter another coordinate? (y/n)")
        if choice.lower() != "y":
            break

    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
