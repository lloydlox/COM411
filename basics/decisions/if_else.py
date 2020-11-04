#please print the activity to be calculated
print ("What is your salary?")
salary = int (input())
print ("What is your total bills?")
bills = int (input())
print ("What is your total fuel?")
fuel = int (input())
print ("What is your total car_finance?")
car_finance = int (input())
outgoings = bills + fuel + car_finance
 #Perfoming Calculation 
balance =  salary-outgoings
if balance < 500 :
  print("Your account is in trouble ,you only have :", balance, "in your Account,in short you are a broke ass")
elif balance > 300 :
  print ("Your account is looking healthy, you have", balance, "That is a well maintained account. Keep it up")  
#print ("Your total outgoings is :", outgoings)