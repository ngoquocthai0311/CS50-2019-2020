from cs50 import get_int


def main():
    number = get_int("Number: ")

    count = totalSum = 0

    temp = number

    while(int(temp) > 0):
        count = count + 1
        if (count % 2):
            totalSum += temp % 10
        else:
            totalSum += (temp % 10) * 2
        temp /= 10
    if (count > 12 and count < 17):
        if (count == 16):
            head_num = int(number / pow(10, count - 2))
            if (head_num > 50 and head_num < 56):
                print("MASTERCARD")
                return
            else:
                head_num /= 10
                if (int(head_num) == 4):
                    print("VISA")
                    return
        elif (count == 15):
            head_num = int(number / pow(10, count - 2))
            if (head_num == 34 or head_num == 37):
                print("AMEX")
                return
        elif (count == 13):
            head_num = int(number / pow(10, count - 1))
            if (head_num == 4):
                print("Visa")
                return

    print("INVALID")




main()