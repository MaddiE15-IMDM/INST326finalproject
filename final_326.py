from fpdf import FPDF

# Roommate Agreement 

#creates an instance of a roommate, giving them a name and a list of bills that will be their responsibility
class Roommate(): 
    def __init__(self, name):
        self.name = name 
        self.chores = []
        self.rent_share = 0.0
        self.utility_share = 0.0
        self.deposit_share = 0.0
        # needs to take the name of user (input)
    def get_name(self):
        return self.name
    def get_chores(self):
        return self.chores
    def get_rent_share(self):
        return self.rent_share
    def get_utility_share(self):
        return self.utility_share
    def get_deposit_share(self):
        return self.deposit_share
    def set_rent_share(self,new_rent):
        self.rent_share = new_rent
                
    
    def add_chore(self, chore):
        self.chores.append(chore)
    def remove_chore(self,chore):
        # removes the chore from the roommate if completed or other roommate performs that task.
        self.chores.remove(chore)


# calculates the bill split and holds all the bills
class Bill(): 
    '''
    Calculates the payments each roommate must contribute 
    '''

    def __init__(self, amount, description, bill_type):
        self.amount = amount
        self.description = description
        self.bill_type = bill_type.lower()  # 'rent', 'utilities', or 'deposit'

    def pays(self, roommates):

        share = self.amount / len(roommates) # allows for multiple roomates

        for rm in roommates:
            if self.bill_type == 'rent':
                rm.rent_share += share
            elif self.bill_type == 'utilities':
                rm.utility_share += share
            elif self.bill_type == 'deposit':
                rm.deposit_share += share


class PDF(FPDF): 
    '''
    Creates a PDF copy of the roommate agreement
    '''
    def _init_(self, filename):
        super().__init__()
        self.filename = filename
    def header(self):
        self.set_font("Times",'U' size=12)
        self.cell(0,10,'Roommate Agreement', 0,1, 'C')
        return super().header()
#unfinished

if __name__=="__main__":
    name = input("Please enter your full name: ")
    roomate = Roommate(name)


