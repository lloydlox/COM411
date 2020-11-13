print ("What phrase do you see?")
phrase = input()
print ("Reversing ....")
print ()
print ("The phrase is,",end="")
for x in range (0,len(phrase)):
  rev1 = len(phrase)-1
  rev2 = (rev1-x)
  word = (phrase[rev2])
  print (word, end='')

#print ("Reversing ....")
#print (word)
#print ("The phrase is :", word,end="")

