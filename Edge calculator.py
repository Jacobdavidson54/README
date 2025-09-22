print("hey welcome to  the Edge calculator")
def add(num1,num2) :
    return num1 + num2
def sub(num1,num2) :
    return num1 - num2
def mul(num1,num2) :
    return num1 * num2
def div(num1,num2) :
    return num1 / num2 

while True :
    try :
        num1 = float(input(("hey please type your fist number here :")))
        num2 = float(input(("hi again ,now type your second number here :")))
    except ValueError :
                 print("please type only numbers")
                 continue   
    operation = input("hey which operation would you like to perform-'add','sub','multi','div' or 'exit'").lower()
    if operation == 'add' :
         results = add(num1,num2)
         print("your answer is",results)
    elif operation == 'sub' :
         results = sub(num1,num2)
         print("your answer is",results)
    elif operation == 'multi' :
         results = mul(num1,num2)
         print("your answer is",results)
    elif operation == 'div' :
         try :
           results = div(num1,num2)
           print("your answer is",results)
         except ZeroDivisionError :
              print("you cant divide by zero")
              continue           
    elif operation == 'exit' :
        print("thank you for using the operation bro")
        break
    else :
         print("invalid operation please try again")
         continue
print("see you next time")




    
         



    
    


