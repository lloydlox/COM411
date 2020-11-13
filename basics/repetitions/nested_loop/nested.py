print ("How many roles should I have?")
rows =int(input())
print ("How many columns should I have?")
columns = int(input())
sign = (":-)")
for x in range (0,rows,1):
  #start = sign * x
  #start = sign * rows
  #print (sign)
  for number in range (0,columns,1):
    print (sign,end="")
  print ()
  
