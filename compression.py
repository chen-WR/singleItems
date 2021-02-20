def main(string):
    array1 = list(string)
    array2 = []
    counter = 0
    current = ''
    for i in range(len(array1)):
        # If current value is nothing, set the current list[i] as current and counter will incretment by 1
        if current == "":
            current = array1[i]
            counter+=1
        # If i is at the end of the range, add it to the array
        if i == (len(array1)-1):
            array2.append(str(counter)+current)
        # If current value equal the next value, incretment the counter, and continue to check next value
        elif current == array1[i+1]:
            counter+=1
        # If the next value doesnt equal the current value, add counter+current to array2 and reset current and counter       
        elif current != array1[i+1]:
            array2.append(str(counter)+current)
            current =""
            counter = 0
    # Convert array2 into string
    return ''.join(array2)

test1 = "aabbcc"
print(test1)
print(main(test1))

test2 = "abcdefgaaacccdddfgfvg"
print(test2)
print(main(test2))