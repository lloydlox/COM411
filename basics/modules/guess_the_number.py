import random
print ("Please enter the minimum value:")
mini_value = int (input())
print ("Please enter the maximum value:")
max_value = int (input())
random_value = random.randrange(mini_value,max_value,1)
print ("I am thinking of a number between", mini_value, "and", max_value,". Can you guess what it is?")
guess_value = int (input())
if guess_value < random_value:
  print ("Your guess is too low")
if guess_value > random_value:
     print ("Your guess is too high")
elif guess_value ==random_value:
    print ("Congratulations! You guessed my number")
else:
    print ("Try again")  
while guess_value > random_value or guess_value < random_value:
   guess_value = int (input())


