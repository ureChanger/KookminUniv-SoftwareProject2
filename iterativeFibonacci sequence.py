import time

def fibo(n) :
    if n <= 1 :
        return n
    return fibo(n-1) + fibo(n-2)

def iterfibo(n):
    first_num = 0
    second_num = 1
    sum_num = 1

    for i in range(2, n+1):
        sum_num = first_num + second_num
        first_num = second_num
        second_num = sum_num

    return sum_num



while True :
    nbr = int(input("Enter a nmumber : "))

    ts = time.time()
    fibonumber = iterfibo(nbr)
    ts = time.time() - ts
    print("IterFio(%d)=%d, time %.6f" %(nbr, fibonumber, ts))

    ts = time.time()
    fibonumber = fibo(nbr)
    ts = time.time() - ts
    print("Fibo(%d)=%d, time %.6f" % (nbr, fibonumber, ts))