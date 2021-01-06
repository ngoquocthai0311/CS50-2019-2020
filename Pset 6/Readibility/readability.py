from cs50 import get_string

def main():
    letters = words = sentences = 0

    text = get_string("Text: ")

    for i in text:
        if (i >= 'A' and i <= 'Z') or (i >= 'a' and i <= 'z'):
            letters = letters + 1
        elif (i == ' '):
            words = words + 1
        elif (i == '.' or i == '?' or i == '!'):
            sentences = sentences + 1

    words = words + 1
    L = float(letters / words) * 100
    S = float(sentences / words) * 100

    index = round(0.0588 * L - 0.296 * S  - 15.8)

    if (index < 1):
        print("Before Grade 1")
    elif(index > 16):
        print("Grade 16+")
    else:
        print(f'Grade {index}')
main()