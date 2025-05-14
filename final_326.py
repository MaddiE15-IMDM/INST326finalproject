'''
INST326 Final Project 
Team: Simran Arora, Jasmine Ukonu, Madison Ellis, Julissa Hernandez

This program creates a template for a personalized Roommate Agreement, and downloads it as a PDF to the user's machine
'''
from fpdf import FPDF

class Roommate:
    '''
    Holds instances of roommates including their responsibilities and busy/free days 

    Attributes: 

    Returns: 
    '''
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
        self.filename = filename # change to be more dynamic

        # create FPDF instance
        self.pdf = FPDF('P', 'mm', 'Letter')
        # add the page
        self.pdf.add_page()
        # create new page if the first one runs out of room
        self.pdf.set_auto_page_break(True, 10)
        # specify fonts ( in our case, times font, regular type and 12 pts )
        self.pdf.set_font("times", '', 12)

    def generate(self, roommates, bill, rules_text, cleaning_days, chores):
        
        # create a title
        self.pdf.cell(0, 10, f"\nRoommate Agreement - {bill.period}", ln = 1) # ln = 1 means ln = true, this is basically a \n 

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
    # using a loop to create instances of roomates
    roommates = [] # empty list to be filled with instances of Roommate()
    while len(roommates) <= 5: 
        name = input(f"Roomate {len(roommates) + 1 }'s name, or type F to finish: " + '\n').strip()
        if name == 'f' or 'F': 
            break
        roommates.append(Roommate(name)) # can also put instance of roomate in a variable if need be
        if len(roommates) <= 1:
            raise ValueError ('You must have at least 2 roommates') # troubleshoot a value less than 2 


    # Enter Bill Info
    rent = float(input("Enter total rent amount: "))
    utilities = float(input("Enter total utilities amount: "))
    deposit = float(input("Enter total security deposit amount: "))
    period = input("Enter billing period (e.g., May 2025): ")

    # creating an instance of Bill() 
    bill = Bill(rent, utilities, deposit, period)
    # roommates = [roommate1, roommate2] <-- no longer needed 
    # run the split method to portion the bills equally amongst roommates
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