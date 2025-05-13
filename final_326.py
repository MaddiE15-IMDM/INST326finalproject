from fpdf import FPDF

# Roommate Agreement 

# calculates the bill split and holds all the bills
# class Bill(): 
    # '''
    # Calculates the payments each roommate must contribute 
    # '''

    # def __init__(self, amount, description, bill_type):
    #     self.amount = amount
    #     self.description = description
    #     self.bill_type = bill_type.lower()  # 'rent', 'utilities', or 'deposit'

    # def pays(self, roommates):

    #     share = self.amount / len(roommates) # allows for multiple roomates

    #     for rm in roommates:
    #         if self.bill_type == 'rent':
    #             rm.rent_share += share
    #         elif self.bill_type == 'utilities':
    #             rm.utility_share += share
    #         elif self.bill_type == 'deposit':
    #             rm.deposit_share += share
# love the way we have it above, might revisit because it makes our code 
# more dynamic in terms of how many roomates there can be 


class Roommate:
    # a set of days to be used later in order to calculate the days that a roomate is busy
    all_days = {"monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"}

    def __init__(self, name):
        self.name = name
        self.split_list = [] # list of bills divided per roomate
        self.busy_days = set() # will be used to capture a roomates busy days

    def add_split(self, rent_split, utility_split, deposit_split): # sets the split list to become the rent, utility and deposit responsibilities of ONE roomate
        self.split_list = [rent_split, utility_split, deposit_split]

    def set_busy_days(self, days): 
        self.busy_days = set(day.strip().lower() for day in days) # cleans up user input to be matched with the all_days set 

    def get_free_days(self): # subtract all_days by busy_days to get whatever is remaining, for ONE roomate
        return Roommate.all_days - self.busy_days

    def __repr__(self): # display the split in a formatted fashion
        return (f"{self.name}'s Responsibilities:\n"
                f"  Rent: ${self.split_list[0]}\n"
                f"  Utilities: ${self.split_list[1]}\n"
                f"  Security Deposit: ${self.split_list[2]}\n"
                f"  Free Days: {', '.join(sorted(self.get_free_days()))}\n")

class Bill:
    '''
    Calculate the split in financial responsibilities per roomate. 
    '''
    def __init__(self, rent, utilities, deposit, period): # requires full rent, utility fees and deposit 
        self.rent = rent
        self.utilities = utilities
        self.deposit = deposit
        self.period = period # billing period e.g May 2025

    def split(self, roommates): # calculate splits in financial by roomate 
        num = len(roommates) # calculate number of roomates 
        rent_split = round(self.rent / num, 2)
        utility_split = round(self.utilities / num, 2)
        deposit_split = round(self.deposit / num, 2)

        for rm in roommates:
            rm.add_split(rent_split, utility_split, deposit_split) # function from roomates 

# SIMRAN IS WORKING ON THE PDF ISSUES!!! 
class Pdf:
    def __init__(self, filename):
        self.filename = filename

    def generate(self, roommates, bill, rules_text, cleaning_days, chores):
        print(f"\nRoommate Agreement - {bill.period}")
        print("=" * 40)
        for rm in roommates:
            print(rm)
        print("\n----- Agreement Terms -----")
        print(rules_text)
        
        print("\nSuggested Cleaning Day(s):")
        if cleaning_days:
            print(", ".join(sorted(cleaning_days)))
        else:
            print("No common free day found. Consider rotating responsibilities.")

        print("\n----- Chore List -----")
        for i, chore in enumerate(chores, 1):
            print(f"{i}. {chore}")
        print("\n(You can assign these manually or rotate weekly.)")


def find_common_free_day(roommates):
    if not roommates:
        return []

    common_days = roommates[0].get_free_days()
    for rm in roommates[1:]:
        common_days = common_days & rm.get_free_days()

    return sorted(common_days)


def input_schedule(roommate):
    days = input(f"Enter {roommate.name}'s busy days (comma-separated, e.g., Monday, Friday): ")
    roommate.set_busy_days([d.strip() for d in days.split(",")])


def get_chores():
    chores_input = input("Enter chores separated by commas (e.g., Dishes, Vacuum, Trash): ")
    chores = [chore.strip().capitalize() for chore in chores_input.split(",") if chore.strip()]
    return chores


def main():
    print("-----Roommate Agreement Generator-----\n")

    # ask user for roomate names 
        # edit to be a loop: up to 5 roomates allowed 
    # name1 = input("Enter name of roommate 1: ")
    # name2 = input("Enter name of roommate 2: ")
    # roommate1 = Roommate(name1)
    # roommate2 = Roommate(name2)

    # using a loop to create instances of roomates
    roommates = [] # empty list to be filled with instances of Roommate()
    while len(roommates) <= 5: 
        name = input(f"Roomate {len(roommates) + 1 }'s name, or type F to finish: ").strip()
        if name == 'f' or 'F': 
            break
        roommates.append(Roommate(name)) # can also put instance of roomate in a variable if need be
        if len(roommates) > 1:
            raise ValueError ('You must have at least 2 roommates') # troubleshoot a value less than 2 


    # Enter Bill Info
    rent = float(input("Enter total rent amount: "))
    utilities = float(input("Enter total utilities amount: "))
    deposit = float(input("Enter total security deposit amount: "))
    period = input("Enter billing period (e.g., May 2025): ")

    bill = Bill(rent, utilities, deposit, period)
    # roommates = [roommate1, roommate2] <-- no longer needed 
    bill.split(roommates)

    # Agreement text which we decided would be inserted as is 
    rules = """
Security Deposit Rule: Each roommate is responsible for their share. Any damages will be deducted accordingly.
Contact Info: Please share phone numbers and emergency contacts.
Moving Out: A 30-day notice is required before moving out.
House Rules: Clean up after yourself, no loud music after 10PM, alternate chores weekly.
"""

    # Cleaning day calculation based on when both roomates are free 
    cleaning_days = find_common_free_day(roommates)

    # Chore collection (input from user )
    chores = get_chores()

    # Generate Report 
    # TBD on what module to use for this to actually work
    report = Pdf("roommate_agreement.pdf")
    report.generate(roommates, bill, rules, cleaning_days, chores)


if __name__ == "__main__":
    main()

# TESTS 
# roommate_1 = Roommate('Julissa')
# roomate_2 = Roommate('Jasmine')
# rent = Bill()

# might need this later....
# class PDF(FPDF): 
#     '''
#     Creates a PDF copy of the roommate agreement
#     '''
#     def _init_(self, filename):
#         super().__init__()
#         self.filename = filename
#     def header(self):
#         self.set_font("Times",'U' size=12)
#         self.cell(0,10,'Roommate Agreement', 0,1, 'C')
#         return super().header()


