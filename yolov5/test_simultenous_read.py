while(True):
    with open('./device_status.txt') as f:
            lines = f.readlines()
            print(lines)
    f.close()