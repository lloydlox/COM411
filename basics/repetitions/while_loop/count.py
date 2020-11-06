print ("How many live cables should I avoid?")
x = int(input())
print (x)
count = 0
while (count<x):
  count = count + 1
  print ("Avoiding ....Done!", count, "live cables avoided.")
  print ("All live cables have been removed", end="")