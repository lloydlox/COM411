print ("What type of cover does the book: soft or hard")
book_type = input ()

if book_type == ("soft"):
  answ = input("Is the book perfect bound?")
  if answ == ("yes"):
     print ("Soft covers, perfect bound books are very popular!")
  else:
    print ("SOfe covers or stiches are great for short books")
else:
  print ("Books with hard conver can be more expensive")


