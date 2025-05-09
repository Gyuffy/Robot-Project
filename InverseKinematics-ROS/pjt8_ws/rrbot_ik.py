import math


class RRBotController:
    def __init__(self):
        self.BASE_HEIGHT = 2.0
        self.L1 = 1.0
        self.L2 = 1.0

    def ik_rrbot(self, x, z):
        # z에서 base height를 빼서 평면상의 상대 위치로 변환
        z = z - self.BASE_HEIGHT

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
        q1 = math.atan2(z, x) - math.atan2(k2, k1)
        return -q1, -q2


def main():
    controller = RRBotController()

    print("RRBot Inverse Kinematics Calculator")
    print("Enter 'q' to quit")

    while True:
        try:
            x_input = input(
                "Enter x coordinate (horizontal, 0 is at base center, right is positive): "
            )

            if x_input.lower() == "q":
                break
            x = float(x_input)

            z_input = input(
                "Enter z coordinate (vertical, 0 is at base center, up is positive): "
            )

            if z_input.lower() == "q":
                break
            z = float(z_input)

            ik_result = controller.ik_rrbot(x, z)
            if ik_result:
                q1, q2 = ik_result
                print(f"Input coordinates: (x={x:.4f}, z={z:.4f})")
                print(f"Joint angles (radians): [q1={q1:.4f}, q2={q2:.4f}]")
                print(
                    f"Joint angles (degrees): [q1={math.degrees(q1):.4f}, q2={math.degrees(q2):.4f}]"
                )
            else:
                print(
                    "Unable to calculate inverse kinematics for the given coordinates."
                )

        except ValueError:
            print("Invalid input. Please enter numeric values.")


if __name__ == "__main__":
    main()
