import pyrealsense2 as rs  # 인텔 리얼센스 카메라를 제어하는 라이브러리
import numpy as np  # 이미지 데이터를 배열 형태로 처리하는 라이브러리
import cv2  # OpenCV, 영상 처리, 영상 출력을 위해서 사용

# 파이프라인 설정
pipeline = rs.pipeline()  # 파이프라인 객체 생성
config = rs.config()  # 해상도, 영상종류, 프레임을 사용하기위한 설정 객체를 생성
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
# rs.stream.color 컬러 스트림, #640 480 해상도 설정
# rs.format.bgr8 OpenCV에서 사용하는 8bit BGR형식, 30= 30프레임

# add
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)  # 깊이 스트림 설정
profile = pipeline.start(config)  # pipline start

# 깊이 센서에서 거리계산을 하기위한 Scale정보 가져오기
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


try:
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

        #####라이브3#########
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
        cv2.imshow("Color Mask2 (HSV)", result)  # 인식된 부분만 컬러로 보임.

        #'q' Key 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
finally:
    pipeline.stop()  # 리소스 해제
    cv2.destroyAllWindows()  # 모든 OpenCV창을 닫음.
