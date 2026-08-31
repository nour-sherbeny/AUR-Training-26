from abc import ABC 
from enum import Enum

class ItemStatus(Enum):
    AVAILABLE="available"
    CHECKED_OUT="checked_out"
    LOST="lost" 

class LibraryItem(ABC):
    def __init__(self):
        self._status = ItemStatus.AVAILABLE  #an instance of the enum class
    def checkout(self):
        if self._status!=ItemStatus.AVAILABLE:
            raise ValueError("this item is not available")
        else:
            self._status=ItemStatus.CHECKED_OUT
            Database.save(self.items)
    
    def return_item(self):
                if self._status != ItemStatus.CHECKED_OUT:
                    raise ValueError("This item is not checked out")
                else:
                    self._status=ItemStatus.AVAILABLE
                    Database.save(self.items)
    
    def mark_lost(self):
                self._status=ItemStatus.LOST
                Database.save(self.items)

    def __lt__(self, other):
        return self.title < other.title    

    def __str__(self):
        return f"{self.title} ({self.__class__.__name__}) — {self._status.value}"        
    

class book(LibraryItem):
    def __init__(self,title,author,isbn):
        super().__init__()
        self._loan_period=21
        self.title=title
        self.author=author
        self.isbn=isbn

    @classmethod
    def from_dict(cls,data):
        book=cls(data["title"],data["author"],data["isbn"]) #value of the key title,author,isbn in data dictionary
        #ISBN 13->sum of its numbers multiplied alternately by 1&3 should give a no. div by 10
        if not cls.checksum(book.isbn):
                raise ValueError("invalid ISBN")
        book._status=ItemStatus[data["status"]]
        return book
    @staticmethod
    def checksum(isbn):
        sum=0
        i=0 #iteration
        for char in isbn:
            x=int(char)
            if i%2==0: #multiply digit by 1 in even iterations and by 3 in odd iterations
                sum=sum+x
            else:
                sum=sum+(x*3)
            i=i+1  
        if sum%10==0:
            return 1
        return 0 
      
    def to_dict(self):
        return {
            "type": "Book",
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "status": self._status.name
        }   
                    

class DVD(LibraryItem):
    def __init__(self,title,director):
        super().__init__()
        self._loan_period=5
        self.title=title
        self.director=director
    @classmethod
    def from_dict(cls,data):
        DVD=cls(data["title"],data["director"])  #value in the key title and director
        DVD._status=ItemStatus[data["status"]]
        return DVD
    def to_dict(self):
        return {
            "type": "DVD",
            "title": self.title,
            "director": self.director,
            "status": self._status.name
        }
    
class magazine(LibraryItem):
    def __init__(self,title,issue):
        super().__init__()
        self._loan_period=14
        self.title=title
        self.issue=issue
    @classmethod
    def from_dict(cls,data):
        magazine=cls(data["title"],data["issue"])  #value in the key title and issue
        magazine._status=ItemStatus[data["status"]]
        return magazine
    def to_dict(self):
        return {
            "type": "Magazine",
            "title": self.title,
            "issue": self.issue,
            "status": self._status.name
        }

ITEM_TYPES = {
    #key is a string and value is a class
    "Book":book,
    "DVD":DVD,
    "Magazine":magazine
}    

class Database():
    def load(self):   #loads data from file to the dictionary data 
        items=[] 
        try:
            f=open(r"D:\nour\AUR-Training-26\task_3\database.txt","r")
            for line in f:
                line=line.strip()
                if not line:
                    continue
                data={} 
                for field in line.split("|"):
                    key,value=field.split("=") #stores the list of strings that split returns   
                    data[key]=value
                item_type=data["type"]  #value of "type" key in data dictionary
                item_class=ITEM_TYPES[item_type]  #searches for this specific class in ITEM_TYPES dictionary
                item = item_class.from_dict(data) #call the method of this specified class
                items.append(item)
            return items   

        except:
            raise FileNotFoundError("couldn't open file")
        f.close()  
    def save(self,items):
        try:
             f=open(r"D:\nour\AUR-Training-26\task_3\database.txt","w")  
             for item in items:
                data=item.to_dict()

                line = "|".join( f"{key}={value}" for key, value in data.items()) #join fields with | between them 

                f.write(line + "\n")

        except:
            raise FileNotFoundError("couldn't open file")
        f.close()     

class Library():
    def __init__(self):
        self.database=Database()
        self.items=self.database.load()
          
    def add_item(self): 
        type=input("enter type of item to add (book/DVD/magazine): ")
        if type=="book":
            title=input("enter title of book: ")
            author=input("enter author of book: ")
            isbn=input("enter ISBN of book: ")
            item=book(title,author,isbn)
        elif type=="DVD":
            title=input("enter title of DVD: ")
            director=input("enter director of DVD: ")
            item=DVD(title,director)
        elif type=="magazine":    
            title=input("enter title of magazine: ")
            issue=input("enter issue of magazine: ")
            item=magazine(title,issue)
        self.items.append(item)
        self.database.save(self.items)  #save updates to file

    def checkout(self, item):
        item.checkout()
        self.database.save(self.items)

    def return_item(self, item):
        item.return_item()
        self.database.save(self.items)

    def mark_lost(self, item):
        item.mark_lost()
        self.database.save(self.items)

    def find_by_title(self,title):
        for item in self.items:
            if item.title==title:
                print(item)
        return None  
     
    def list_available(self):
        for item in self.items:
            if item._status == ItemStatus.AVAILABLE:
                 print(item)



library=Library()
library.list_available()
library.add_item()
library.list_available()
library.find_by_title("The Great Gatsby")
    
