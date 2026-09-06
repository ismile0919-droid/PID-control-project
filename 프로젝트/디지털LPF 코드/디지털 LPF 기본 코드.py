#EMA(Exponential Moving Average-지수평균이동필터)

def low_pass_filter(new_vlaue, prev_value, alpha):
    return alpha*new_vlaue+(1-alpha)*prev_value

#사용 예시
alpha=0.2
filtered=None

while True:
    raw=sensor.range

    if filtered is None:
        filtered=raw
    else:
        filtered=low_pass_filter(raw, filtered, alpha)

#이후 로직에서는 raw 대신 filtered 사용.