# Roomate Agreement 

#creates an instance of a roomate, giving them a name and a list of bills that will be their responsibility
class Roomate(): 
    def __init__(self, name): 
        self.name = name 
        self.chores = []
        self.rent_share = 0.0
        self.utility_share = 0.0
        self.deposit_share = 0.0
    
    def add_chore(self, chore): 
        self.chores.append(chore)
    


# calculates the bill split and holds all the bills
class Bill(): 
    '''
    Calculates the payments each roomate must contribute 
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


class PDF: 
    '''
    Creates a PDF copy of the roomate agreement
    '''
