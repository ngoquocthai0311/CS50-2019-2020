import sys
import csv


def LongestConsecutive(string, contentDNA):
    # initialize the variables
    index = maximum = tempMax = 0
    end = len(contentDNA)

    # check if index is out of range
    while (index <= end - 1):
        tempIndex = index
        flag = True
        for each in string:
            if (tempIndex <= end - 1):
                # print('so sanh ' + each + ' ' + contentDNA[index] + ' tai ' + str(index))
                if (each != contentDNA[tempIndex]):
                    # update the max if necessary
                    if (tempMax > maximum):
                        maximum = tempMax
                    flag = False
                    tempMax = 0
                    break
                else:
                    tempIndex = tempIndex + 1
            else:
                break
        if (flag):
            # update tempIndex and index
            tempMax = tempMax + 1
            index = tempIndex
        else:
            index = index + 1
    return maximum


def main():
    if (len(sys.argv) != 3):
        print("Usage: python dna.py data.csv sequence.txt")
        return

    # open dna file
    fileDNA = open(f'{sys.argv[2]}', "r")
    contentDNA = list(fileDNA.read())

    # open CSV file
    with open(f'{sys.argv[1]}', 'r') as file:
        contentCSV = list(csv.reader(file, delimiter=','))

    strList = list(contentCSV[0])
    strList.remove('name')
    longestList = []

    # find the longest consecutive of each str in the DNA file
    # and append the result into longestList list
    for string in strList:
        longest = LongestConsecutive(string, contentDNA)
        longestList.append(longest)

    # check ppl's DNA
    for row in contentCSV[1::]:
        flag = True
        index = 0
        for each in row[1::]:
            if (int(each) != longestList[index]):
                flag = False
                break
            else:
                index = index + 1
        if (flag == True):
            print(row[0])
            return
    # if the program is not running the previous line
    print("No match")


main()