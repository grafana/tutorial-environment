
#!/bin/env python3

import datetime
import math
import random
import sys
import time



requests_per_second = 2
failure_rate = 0.05
get_post_ratio = 0.9
get_average_duration_ms = 500
post_average_duration_ms = 2000


while True:

    # Exponential distribution random value of average 1/lines_per_second.
    d = random.expovariate(requests_per_second)
    time.sleep(d)
    if random.random() < failure_rate:
        status = "500"
    else:
        status = "200"
    if random.random() < get_post_ratio:
        method = "GET"
        duration_ms = math.floor(random.expovariate(1/get_average_duration_ms))
    else:
        method = "POST"
        duration_ms = math.floor(random.expovariate(1/post_average_duration_ms))
    timestamp = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
    print(f"{timestamp} level=info method={method} url=/ status={status} duration={duration_ms}ms")
    sys.stdout.flush()