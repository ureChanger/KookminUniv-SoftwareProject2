from math import factorial as fact

def operator(numStr, key):
    if key == 'factorial':
        try:
            n = int(numStr)
            r = str(fact(n))
        except:
            r = 'Error!'
        return r

    elif key == 'decToBin':
        try:
            n = int(numStr)
            r = bin(n)[2:]
        except:
            r = 'Error!'
        return r

    elif key == 'binToDec':
        try:
            n = int(numStr, 2)
            r = str(n)
        except:
            r = 'Error!'
        return r

    elif key == 'toRoman':
        n = int(numStr)
        if n>100:
            raise ValueError("Value must be less than 100.")
        num = (100, 90, 50, 40, 10, 9, 5, 4, 1)
        roman_num = ('C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I')

        result = ""

        for i in range(len(num)):
            count = int(n / num[i])
            result += roman_num[i] * count
            n -= num[i] * count

        return result