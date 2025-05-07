# Dobot API
import DobotEDU
import time

# Camera API
import pyrealsense2 as rs
import numpy as np
import cv2

# Pipeline Setting
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)  # 깊이 스트림 설정
profile = pipeline.start(config)  # pipline start

# 거리 계산을 위한 Scale 정보 가져오기
depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()  # 일반적으로 0.001단위 meter

# 정렬(depth정보를 color와 맞추기위해 정렬 필요)
align_to = rs.stream.color
align = rs.align(align_to)

# HSV 색공간에서 타겟(빨강)색상은 양쪽으로 나누어져 있음, 그래서 범위를 나누어서 설정
lower_red1 = np.array([0, 120, 70])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([170, 120, 70])
upper_red2 = np.array([180, 255, 255])

# Dobot 연결 및 데이터 가져오기
PORT = "COM3"
device = DobotEDU.dobot_magician
device.connect_dobot(PORT)
print("연결이 완료 되었습니다")


# Dobot 동작 함수
def homeing_robot():
    print("Homing 중...")
    DobotEDU.dobot_magician.set_homecmd(PORT)
    print("홈 위치 동작 완료되었습니다")


def movejp(pos):
    p1 = pos[0]
    p2 = pos[1]
    p3 = pos[2]
    p4 = pos[3]
    print(pos)
    DobotEDU.dobot_magician.set_ptpcmd(PORT, ptp_mode=0, x=p1, y=p2, z=p3, r=p4)
    time.sleep(0.5)
    print("movejp 실행 완료")


def grip():
    DobotEDU.dobot_magician.set_endeffector_gripper(PORT, enable=True, on=True)
    time.sleep(1)
    DobotEDU.dobot_magician.set_endeffector_gripper(PORT, enable=False, on=False)
    print("Grip!")


def ungrip():
    DobotEDU.dobot_magician.set_endeffector_gripper(PORT, enable=True, on=False)
    time.sleep(0.5)
    DobotEDU.dobot_magician.set_endeffector_gripper(PORT, enable=False, on=False)
    print("Ungrip!")


def pick_block(pos):
    print("#1 movejp pos 완료")

    movejp(pos)
    grip()
    goal = [65, 260, -18, 90]
    print("#3 movejp goal 완료")

    movejp(goal)
    ungrip()
    movejp([200, 0, 20, 90])


picked = False

try:
    # ROBOT의 자세 초기화
    homeing_robot()
    ungrip()

    ccy = 0
    ccx = 0

    while True:
        frames = (
            pipeline.wait_for_frames()
        )  # 카메라에서 최신 프레임을 수신(색상,깊이..)
        aligned_frames = align.process(frames)
        coloer_frame = aligned_frames.get_color_frame()
        depth_frame = aligned_frames.get_depth_frame()

        if (
            not coloer_frame or not depth_frame
        ):  # 만약 컬러 프레임, depth프레임 없는 경우 처음루프로 빠져나감.(수신실패방지)
            continue

        # 컬러프레임을 numpy배열로 변환
        color_image = np.asanyarray(coloer_frame.get_data())
        depth_image = np.asanyarray(depth_frame.get_data())
        hsv_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)
        # 컬러이미지를(BGR)를 HSV영역으로 변환

        mask1 = cv2.inRange(hsv_image, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv_image, lower_red2, upper_red2)

        mask = cv2.bitwise_or(mask1, mask2)
        # 변환한 두 마스크를 합치기

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # RETR_EXTERNAL :가장 바깥쪽 윤곽선만 추출
        # CHAIN_APPROX_SIMPLE : 윤곽선을 직선으로 단순화 시켜서 메모리를 절약
        for i in contours:
            area = cv2.contourArea(i)
            if area > 1000:
                x, y, w, h = cv2.boundingRect(i)
                cv2.rectangle(color_image, (x, y), (x + w, y + h), (0, 0, 150), 2)
                # 면적이 500픽셀보다 큰 경우만 필터링
                # boundingRect 외곽에 사각형을 그림
                # (0, 255, 0) 초록색으로 표시
                #####################

                # 중심점 계산
                cx = x + w // 2
                cy = y + h // 2

                ccy = cy
                ccx = cx
                ########

                # depth 정보 수신
                depth = depth_frame.get_distance(cx, cy)
                depth_data = f"({cx}px, {cy}px, {depth:.3f}m)"

                # 중심점에 깊이 정보 표시
                cv2.putText(
                    color_image,
                    depth_data,
                    (cx + 10, cy),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 255, 255),
                    2,
                )

                # 중심점에 마커를 그리기
                cv2.drawMarker(
                    color_image,
                    (cx, cy),
                    (0, 255, 0),
                    markerType=cv2.MARKER_CROSS,
                    markerSize=20,
                    thickness=2,
                )

                # 중심점 좌표 그리기
                # cv2.putText(color_image, f"{cx, cy}", (cx+10, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

                # pixel 수 표현
                cv2.putText(
                    color_image,
                    f"Pixel Area: {int(area)} px",
                    (cx + 10, cy + 25),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 255, 255),
                    2,
                )

        # putText를 활용해서 영상에 글자 넣기
        cv2.putText(
            color_image,
            "SSAFY VISION",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 255),
            2,
        )

        result = cv2.bitwise_and(color_image, color_image, mask=mask)  # 마스크연산
        # 마스크 연산 후 타겟 색상만 출력

        # 영상출력
        cv2.imshow("SSAFY RGBD CAMERA STREAM", color_image)  # 원본 영상
        cv2.imshow("Color Mask (HSV)", mask)  # 빨간부분흰색 마스크 , 나머지는 검정
        cv2.imshow("Color Mask2 (HSV)", result)  # 인식된 부분만 컬러로 보임.q

        # block의 위치 맵핑
        if contours != 0 and not picked:
            target_position = [ccy * (305 / 480) + 95, ccx * (410 / 640) - 210, -18, 90]
            print(target_position)
            pick_block(target_position)
            picked = True

        #'q' Key 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
finally:
    pipeline.stop()  # 리소스 해제
    cv2.destroyAllWindows()  # 모든 OpenCV창을 닫음.
