# import library
from cs50 import get_int
# main function


def main():

    while True:
        # input the height
        height = get_int("Height: ")
        if height in [1, 2, 3, 4, 5, 6, 7, 8]:
            break

    for i in range(height):
        space = height - (i + 1)
        star = height - space
        print(" " * space + "#" * star + "  " + "#" * star)


# treating the function as int main(void)
main()