num = int(input("n: "))

sum = 0
x=1
while x<=num:
    sum=sum + 1/(x*x)
    x=x+1
    
print ("the sum is:" , sum)