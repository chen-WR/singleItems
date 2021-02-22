import random

def swap(list1, p1, p2):
    list1[p1], list1[p2] = list1[p2], list1[p1]
    return list1

def weirdSort(list1):
    flag = True
    while flag:
        counter = 0
        # 0-8
        for i in range(0, len(list1)-1):
            if list1[i] > list1[i+1]:
                swap(list1, i, i+1)
                counter += 1
        if counter == 0:
            flag = False
            
    return list1

def main(list1):
    return weirdSort(list1)


# Test
print(main(list1=[2,4,3,2,1,7]))