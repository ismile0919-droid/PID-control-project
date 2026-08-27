import time

# [1. I 제어 변수 및 파라미터 초기화 (루프 밖)]
Ki = 0.05              # I 게인 (매우 작은 값부터 시작: 0.01 ~ 0.1)
integral = 0.0         # 오차 누적 저장소
INTEGRAL_MAX = 2.0     # 안티 와인드업(Anti-Windup): 적분 상한선 클램핑

prev_time = time.time()

while True:
    # [2. 루프 시간 간격(dt) 측정]
    current_time = time.time()
    dt = current_time - prev_time
    if dt <= 0.0:
        dt = 0.033
    prev_time = current_time

    # [3. 현재 오차 측정 (cm 단위)]
    error = distance1 - d2_cal_cm

    # [4. I 제어 적분 연산 및 안티 와인드업(Anti-Windup)]
    # 오차가 데드밴드 바깥에 있을 때만 시간에 비례하여 누적
    if abs(error) >= 1.0:
        integral += error * dt
        # 적분 누적 폭주 방지 (클램핑)
        integral = max(-INTEGRAL_MAX, min(INTEGRAL_MAX, integral))
    else:
        # 목표 범위(데드밴드)에 안착하면 누적 오차를 리셋 (선택 사항)
        integral = 0.0

    # [5. PI 합성 제어량 계산]
    pi_output = (Kp * error) + (Ki * integral)

    # [6. 모터 출력 변환 (기존 매핑 방식)]
    # pi_output을 바탕으로 360도 서보모터 DutyCycle 계산