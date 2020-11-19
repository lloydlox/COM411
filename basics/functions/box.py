print ("What is the word?")
word = input()
symbol_1 = ("*")
symbol_2 = ("-")
length = len(word)
space = (" ")* (length+2)
print (space)
horizontal = "+" + symbol_2 * (length+2) + "+\n"
vertical = symbol_1 + space + symbol_1
half_length = (length)  * 2
print (horizontal)
for x in range (0,4,1):
#print (horizontal)
 print (vertical)
print (word) 
print (horizontal)
#print (vertical)