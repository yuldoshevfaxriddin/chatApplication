import dataBase


class User:
    
    def __init__(self,id=0) -> None:
        data = dataBase.findUser(id)
        if  data:
            self.data = data
            self.id = data[0]
            self.name = data[1]
            self.username = data[2]
            self.password = data[3]
            self.created_at = data[4]
        # print(data)
    def create(self,name,username,password):
        id = dataBase.insertUser(name,username,password)[0]
        return User(id)
    
    def find(self,id):
        """
        data casadan id=id bolgandi topadi
        """
        data = dataBase.findUser(id)
        self.data = data
        self.id = data[0]
        self.name = data[1]
        self.username = data[2]
        self.password = data[3]
        self.created_at = data[4]
        return self


class Region:
    pass



class Category:
    pass

tohir = User(4)
sardor = User().create("sardor","sardooff","password")
jamshid = User().find(5)
print(tohir.data)
print(sardor.data)
print(jamshid.data)