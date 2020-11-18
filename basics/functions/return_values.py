def sum_weights (beep_weight, bop_weight):
  sum = beep_weight + bop_weight
  return (sum)

# Calculate average weight
def calc_avg_weight (beep_weight,bop_weight):
  avg_weight = sum_weights(beep_weight,bop_weight)/2
  return (avg_weight)
 #calculate the sum or average by calling the functions sum_weights & calc_avg_weight
def run ():
  print ("What is the weight of Beep?")
  beep_weight = int (input())
  print ("What is the weight of Bop?")
  bop_weight = int (input())
  print ("What would you like to calculate,(sum or average)")
  answer = input ()
  if answer == ("sum"):
    print ("The sum of Beep and Bop's weight is",sum_weights(beep_weight,bop_weight))
  elif answer == ("average"):
    print ("The average of Beep and Bop's weight is", calc_avg_weight(beep_weight,bop_weight)) 
  # run the program 
  else:
    print("That is not a recognised choice,GOODBYE!!")
run ()  
