class BankAccount:
    def __init__(self, first_name, last_name, account_id, account_type, pin, balance):
        self.first_name = first_name
        self.last_name = last_name
        self.account_id = account_id
        self.account_type = account_type
        self.pin = pin
        self.balance = balance

    def display_balance(self):
        print(f'{self.first_name} {self.last_name}\'s balance is {self.balance}')

    def deposit(self, ammount):
        self.balance += ammount
        return self.balance

    def withdraw(self, ammount):
        self.balance -= ammount
        return self.balance


test = BankAccount('Firstname', 'Lastname', 1234, 'Checking', 0000, 0)
test.deposit(96)
test.withdraw(25)
test.display_balance()
