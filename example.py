def main():
    word = raw_input("Input a word:")
    
    myDict = {}

    for char in word:
        if char not in myDict:
            myDict[char] = 1
        else:
            myDict[char] += 1
            
    print(myDict)

if __name__ == "__main__":
    main()
