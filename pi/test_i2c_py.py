from smbus2 import SMBus


# I2C address: 8
addr = 0x8
# Bus 1 on Pi
bus = SMBus(1)

while (True):

    num1 = int(input("Enter num1 (-50 to 50): "))
    num2 = int(input("Enter num2 (-50 to 50): "))

    # adding 128 to deal with negatives, so each number is 1 byte
    data = [num1 + 128, num2 + 128]
    # print([num1, num2])
    # print(data)

    bus.write_i2c_block_data(addr, 0, data)

    response = [0]

    while (response[0] == 0):
        # return 1 byte, either a 0 for wait or a 1 for continue
        response = bus.read_i2c_block_data(addr, 0, 1)

    print("response of 1 received")
