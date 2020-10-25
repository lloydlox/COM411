TotalSavings = input ("Please enter total amount of savings:")
TotalSavings = int(TotalSavings)
InterestRate = float (0.02)
InterestPeriod = int(6)
print ("Your savings Period is", InterestPeriod)
print ('Todays interest rate is', InterestRate)
print ('The total money you save is', TotalSavings*InterestRate*InterestPeriod)
CurrentTotal = TotalSavings*InterestRate*InterestPeriod+TotalSavings
print ('The amount in your account', CurrentTotal)