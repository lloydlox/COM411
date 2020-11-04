direction_1 = ("right")
direction_2 = ("left")
direction_3 = ("up")
direction_4 = ("down")
print ("The posible directions to move your paint brush are:",direction_1 ,direction_2, direction_3,direction_4)
print ("Which direction should I move my paint brush:")
moveside = (input())
if moveside == direction_1:
  print ("Moving brush right!!")
elif moveside == direction_2:
  print ("Moving brush left!!")
elif moveside == direction_3:
 print ("Moving brush up!!")
else:
  print ("Moving brush down!!!")
#direction = input ()
#if (direction == right):
 # print ("Moving the brush to the right!!")
#elif (moveside == left):
 # print ("Moving the brush to the left!!!")
#elif (direction == up):
#  print ("Moving the brush Up!!!")
#else :
  #print ("Moving the brush down !!!!")
#print ("the end")
