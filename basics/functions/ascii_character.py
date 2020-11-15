
print ("Program Started!")
# get ascii code from user
print ("Please enter an ASCII code:")
ascii_code = int(input())
if ascii_code in range (32,126,1):
  print ("The Characteer represented by the ASCII code" ,ascii_code,"is", chr(ascii_code))

else:
  print ("Input not within range")

