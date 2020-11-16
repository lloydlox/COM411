
print ("Program Started!")
# get ascii code from user
print ("Please enter an ASCII code:")
ascii_code = int(input())
# specify a range to acceptable in the input
if ascii_code in range (32,126,1):
  print ("The Characteer represented by the ASCII code" ,ascii_code,"is", chr(ascii_code))
# error to be displayed
else:
  print ("Input not within range")

