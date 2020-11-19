def display_in_a_box (word):
  symbol_1 = ("*")
  symbol_2 = ("-")
  length = len(word)
  space = (" ")* (length+2)
  horizontal = "+" + symbol_2 * (length+2) + "+\n"
  vertical = symbol_1 + space + symbol_1
#half_length = (length)  * 2
  print (horizontal)
  for x in range (0,4,1):
#print (horizontal)
   print (vertical)
  print (word) 
  print (horizontal)
  return

def display_lower_case (word):
  lower = (word.lower())  
  return (lower)

def display_upper_case (word):
  upper = (word.upper())
  return (upper)

def display_mirrored (word):
  mirror = (word)[::-1]
  print (mirror)  
  return (mirror)

def display_repeat (word):
  print ("How many times times do you want to repeat the word")
  times = int (input())
  for time in range (0,times,1):
    print (display_lower_case(word))
    print (display_upper_case(word))
  return 

def run ():
  print ("Please enter a word")
  word = input ()
  print ("How would you like the word to be presentd choose from the following\n1) Display in a box\n2) Display Lower case\n3) Display Upper Case \n4) Display Mirrored\n5) Display repeated")
  choice = int (input())
  if choice ==1:
    print (display_in_a_box(word))
  elif choice == 2:
    print (display_lower_case(word))
  elif choice == 3:
    print (display_upper_case(word))
  elif choice == 4:
    print (display_mirrored(word))  
  elif choice == 5:
    print (display_repeat(word))  

run ()  
