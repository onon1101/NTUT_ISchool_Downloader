from tqdm import tqdm
import time
import os

programing_bar = tqdm(total = 1000, unit_scale=True)
status_count = 0


while True:
    time.sleep(0.01)
    status_count += 1
    programing_bar.update(1)

    if status_count > 1000:
        break

programing_bar.close()