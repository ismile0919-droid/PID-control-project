# [제어 파라미터]
Kp = 0.5               # P 게인 (0.4~0.6)
Kd = 0.03              # D 게인 (진동 억제용 브레이크: 0.01~0.05 범위 실측)
DEADBAND_CM = 1.0

prev_deviation = 0.0
prev_time = time.time()

# -------------------------------------------------------------
# [루프 내부 - 오차(deviation) 계산 직후]
current_time = time.time()
dt = current_time - prev_time
prev_time = current_time

if dt <= 0.0 or dt > 0.2:
    dt = 0.033

# 1. D(미분) 연산: 오차의 변화 속도 (cm/s)
# 오차가 줄어들 때는 derivative와 deviation의 부호가 반대가 되어 브레이크로 작동
derivative = (deviation - prev_deviation) / dt
prev_deviation = deviation

# 2. PD 합성 제어량 계산 (I항 완전 제거)
pd_output = (Kp * deviation) + (Kd * derivative)

# 3. 불감대 및 서보모터 구동
if abs(deviation) < DEADBAND_CM:
    Ut = 7.35  # 데드밴드 안착 시 완전 정지
elif pd_output > 0:
    duty_delta = (pd_output / MAX_PHYSICAL_ERROR_CM) * 2.5
    Ut = 7.5 + min(2.5, max(0.0, duty_delta))
else:
    duty_delta = (abs(pd_output) / MAX_PHYSICAL_ERROR_CM) * 2.2
    Ut = 7.2 - min(2.2, max(0.0, duty_delta))

pwm.ChangeDutyCycle(Ut)