import random
#database connection
from pymongo import MongoClient

try:
    client = MongoClient('localhost',27017)
    print('Connected to DB')
except:
    print('Database connection was not established Successfully')

from pprint import pprint

#create database
mydb = client['Bank_customer_details']
#create table
mycollection = mydb['Account_Details']


class BankProcess:
    # global account_number
    def __init__(self):
        
        pass

    def create_account(self,name,id_proof,initial_deposit):
        # global account_number
        self.account_number = random.randint(11636475892,11658362854)
        mydict = { str(self.account_number):{"name": name, "id_proof": id_proof, "Initial_deposit":initial_deposit }}
        mycollection.insert_one(mydict)
        print('Account Created and your Account number is {}'.format(self.account_number))
        return self.account_number


    def authenticate(self,account_number):
        value = mycollection.find({},{"{}".format(str(account_number))})
        fetch = []
        for values in value:
            fetch.append(values)
        field = [x for x in fetch if len(x)>1]
        dic_output = field[0]
        val = (dic_output[str(account_number)]['name'])
        
        if mycollection.find({str(account_number): {"$exists": True}}).limit(1).count()>0:
            print('Found your account {} , please wait....'.format(val))
            self.account_number = account_number
            return True
        else:
            print("cannot find your account number. recheck")
            return False
            
    def withdraw(self,withdrawal_amount,account_number):
        self.initial_deposit = 0
        value = mycollection.find({},{"{}".format(str(account_number))})
        fetch = []
        for values in value:
            fetch.append(values)
        field = [x for x in fetch if len(x)>1]
        dic_output = field[0]
        id = (dic_output['_id'])
        val = (dic_output[str(account_number)]['Initial_deposit'])
        self.initial_deposit = val
        if withdrawal_amount > self.initial_deposit:
            print('Insufficient Balance')
        else:
            amt = self.initial_deposit-withdrawal_amount
            mycollection.update_one(
                {'_id':id},
                {'$set':
                    {'{}.Initial_deposit'.format(account_number):amt}
                }
            )
        print('Withdrawal was successful')
        self.display_balance(account_number)

    def deposit(self,deposit_amount,account_number):
        value = mycollection.find({},{"{}".format(str(account_number))})
        fetch = []
        for values in value:
            fetch.append(values)
        print(fetch)
        field = [x for x in fetch if len(x)>1]
        dic_output = field[0]
        id = (dic_output['_id'])
        print(id)
        val = (dic_output[str(account_number)]['Initial_deposit'])
        print(val)
        val +=deposit_amount
        mycollection.update_one(
                {'_id':id},
                {'$set':
                    {'{}.Initial_deposit'.format(account_number):val}
                }
            )
        print('Deposit was Successful..')
        self.display_balance(account_number)
    
    def display_balance(self,account_number):
        value = mycollection.find({},{"{}".format(str(account_number))})
        fetch = []
        for values in value:
            fetch.append(values)
        field = [x for x in fetch if len(x)>1]
        dic_output = field[0]
        val = (dic_output[str(account_number)]['Initial_deposit'])
        print('Available balance :',val)


        
bp = BankProcess()
# bp.create_account('Goutham','DL',10000)
# bp.create_account('vicky','passport',500)
# bp.create_account('Mouric','aadhar',1000)
# bp.create_account('steve','DL',3000)
# bp.withdraw(11,11639021814) 
# bp.deposit(30,11639021814)

while True:
    print('Please enter your choice')
    print('1 - Create new account')
    print('2 - Access Existing Account')
    print('3 - Exit')

    userChoice = int(input())
    acc_num = 0
    if userChoice is 1:
        print('Enter your name')
        name = input()
        print('Enter your id_ proof. DL or AADHAR or PASSPORT')
        idp = input()
        print('Enter initial amount you want to deposit')
        ini = int(input())
        acc_num = (bp.create_account(name,idp,ini))
        
    elif userChoice is 2:
        print('Enter your account number')
        accountN = int(input())
        authenticationStatus = bp.authenticate(accountN)
        if authenticationStatus:
            while True:
                print("Please enter 1 to withdraw")
                print("Please enter 2 to deposit")
                print("Please enter 3 to check Balance")
                print("Please enter 4 for previous menu")
                userChoice = int(input())

                if userChoice is 1:
                    print('Enter withdrawal amount')
                    w_amt = int(input())
                    bp.withdraw(w_amt,accountN)
                elif userChoice is 2:
                    print('Enter sum you want to deposit')
                    d_amt = int(input())
                    bp.deposit(d_amt,accountN)
                elif userChoice is 3:
                    bp.display_balance(accountN)
                elif userChoice is 4:
                    break
                else:
                    print('please choose valid option listed')
    elif userChoice is 3:
        quit()
    else:
        print('please enter valid option')
    