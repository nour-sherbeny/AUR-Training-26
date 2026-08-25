dict={} #empty dictionary
key="" #empty string
value=""
found_comma=0
num_items=0
try:
    f=open(".vscode/task_2/subtask_1/stock.txt", "r")
    for line in f:  
       for char in line:
          if char==',':
            found_comma=1
            continue
          elif char=='\n':
             break
          if found_comma==0:
            key=key+char #concatenation
          elif found_comma==1:
            value=value+char    
       dict[key] = int(value)
       key=""  
       value=""
       found_comma=0
       num_items=num_items+1
    f.close()

except FileNotFoundError:
    print("Couldn't open file")

def customPrint():
   print("Stock's content")
   i=1
   for key, value in dict.items() :
      print(f"{i}. {key}: {value}")
      i=i+1
   print('\n')

def check(IP):
   if type(IP)==int:
      if IP>num_items or IP<=0: 
         return -1   #invalid id
      else:
         return 1   #valid id
   elif type(IP)==str:
      IP=IP.lower()  
      if IP in dict.keys():
         return 1  #existing stock
      else:
         return 0  #new stock

def find_ID(x): 
   i=1
   for key in dict:
      if key==x:
         return i
      else:
         i=i+1  

def editFile(id):
  try:
     f=open(".vscode/task_2/subtask_1/stock.txt", "w")
     for key, value in dict.items():
        f.write(f"\n{key},{value}")
     f.close()
  except FileNotFoundError:
    print("Couldn't open file")    

while True: 
    print("MENU") 
    print("enter 1 to add stock")     
    print("enter 2 to remove stock")     
    print("enter 3 to show stock's content")     
    print("enter 4 to exit the program")      
    choice=int(input())  
    print('\n')
    if choice not in (1,2,3,4):
        print("invalid input, please try again")
        continue
    elif choice==4:
       break
    elif choice==1:
       customPrint()
       print("enter a stock name or id")
       IP=input()
       if IP.isdigit():  #because input() function returns string
           IP = int(IP)
       else:
           IP=IP.lower()    
       result=check(IP) #to check if it exists in stock.txt
       if result==1: #existing stock
          addedStock=int(input("enter the amount of stock to add: "))
          if type(IP)==int:
             i=1
             for key in dict:
                if i==IP:
                   dict[key]=dict[key]+addedStock
                   num_items=num_items+1
                   break
                else:
                   i=i+1
             editFile(IP)      
          else:
             dict[IP]=dict[IP]+addedStock 
             num_items=num_items+1  
             id=find_ID(IP)
             editFile(id)  
       elif result==0:  #new stock
          stockValue=input("enter value of stock: ")
          dict[IP]=stockValue
          num_items=num_items+1
          f=open(".vscode/task_2/subtask_1/stock.txt", "a")  #open file in append mode
          f.write(f"\n{IP},{stockValue}")  #append new stock to file
          f.close()

       else:  #invalid input  
          print("invalid input")
          continue 
    elif choice==2:
       customPrint()
       IP=input("enter a stock name or id to remove: ")
       if IP.isdigit():  
            IP = int(IP)
       else:
            IP=IP.lower()
       result=check(IP)     
       if result==0: 
          print("stock doesn't exist")
          continue 
       elif result==-1: 
          print("invalid input")
          continue  
       else:
          removeStock=int(input("enter amount of stock to remove:"))
          if removeStock<=0:
               print("invalid input")
               continue
          if type(IP)==int:  #stock id
             i=1
             for key in dict:  #to find the key in dictionary from id
                if i==IP:
                   if(dict[key]-removeStock<0):
                        print("not enough stock to remove")
                        continue
                   elif(dict[key]-removeStock==0):
                        dict.pop(key)
                        num_items=num_items-1  
                   else:
                        dict[key]=dict[key]-removeStock
                   break
                else:
                   i=i+1
             editFile(IP)           
    
          else:
             if(dict[IP]-removeStock<0):
                print("not enough stock to remove")
                continue
             else:
                dict[IP]=dict[IP]-removeStock 
                id=find_ID(IP)
                editFile(id)           
    elif choice==3:
        customPrint()
          