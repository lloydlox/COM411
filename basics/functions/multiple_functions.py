def display_ladder (steps):
  symbol_1 = (" | |")
  symbol_2 = (" *** ")
  for x in range (0,steps):
   print (symbol_1)
   print (symbol_2)

  
def create_ladder ():
  print ("How many steps remaining?")
  steps = int (input())
  display_ladder (steps)
      
create_ladder ()