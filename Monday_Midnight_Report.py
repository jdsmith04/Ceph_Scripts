import datetime
# import os
import time
from Ceph_Health_Email_Notification import ceph_status

while True:
    current_now = datetime.datetime.now()
    current_time = current_now.time()
    current_weekday = current_now.weekday()
    ceph_status()

    if current_time == datetime.time(0, 20) and current_weekday == 4:
        print(f'status sent\t{current_time}')
        # os.system('mail -s "Monday Midnight Report" user@domain.com < output.txt')
    else:
        print('waiting')
        time.sleep(1)
