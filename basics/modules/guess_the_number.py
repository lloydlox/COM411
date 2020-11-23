def guess_number ():
  import random
  print ("Please enter the minimum value:")
  mini_value = int (input())
  print ("Please enter the maximum value:")
  max_value = int (input())
  random_value = random.randrange(mini_value,max_value,1)
  print ("I am thinking of a number between", mini_value, "and", max_value,". Can you guess what it is?")
  while True:
  #while guess_value != random_value:
    guess_value = int (input())
    if guess_value == random_value:
      print ("Congratulations! You guessed my number")
      break
   
    elif guess_value < random_value:
      print ("Your guess is too low") 
      print ("Try again")
  #print ("Try again!")
    elif guess_value > random_value:
     print ("Your guess is too high")
     print ("Try again")


guess_number () 


 



