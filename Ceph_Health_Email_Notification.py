# import os
import datetime
import schedule
import threading
import time


def ceph_status():
    # os.system('ceph -s > output.txt')
    ceph_file = open('output.txt', 'r')
    main_dictionary = {}
    header_key = ''
    # read output line by line
    for line in ceph_file:

        # create main key variable
        if ':\n' in line:
            header_key = line.strip()

        # create inner dictionary structures
        elif ': ' in line:

            # 1 level deep dictionary
            try:
                level1_dictionary = {}
                key, value = line.split(': ')
                level1_dictionary[key.strip()] = value.strip()
                main_dictionary[header_key.strip(':')] = level1_dictionary

            # 2 levels deep dictionary
            except ValueError:
                level1_dictionary = {}
                level2_dictionary = {}
                key, inner_key, value = line.split(': ')
                level2_dictionary[inner_key.strip()] = value.strip()
                level1_dictionary[key.strip()] = level2_dictionary
                main_dictionary[header_key.strip()] = level1_dictionary

    return main_dictionary['cluster']['health']


# Send email if ceph health is bad
def bad_health():
    while True:
        ceph_status()
        if ceph_status() != 'HEALTH_OK':
            # os.system('mail -s "CHECK CEPH HEALTH" user@domain.com < output.txt')
            print('HEALTH_BAD EMAIL SENT')
            time.sleep(3420)
        else:
            print(f'OK {datetime.datetime.now().time()}')
        time.sleep(180)


# Generate report and send via email
def monday_report():
    print(f'report sent')
    # os.system('ceph -s < monday_report.txt')
    # os.system('mail -s "Monday Midnight Report" user@domain.com < monday_report.txt')


# Schedule report to be sent every Monday at midnight
def scheduled_report():
    schedule.every().monday.at('00:00').do(monday_report)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    # Putting each task on its own thread
    t1 = threading.Thread(target=bad_health)
    t2 = threading.Thread(target=scheduled_report)
    t1.start()
    t2.start()
