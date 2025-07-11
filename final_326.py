'''
INST326 Final Project 
Team: Simran Arora, Jasmine Ukonu, Madison Ellis, Julissa Hernandez

This program creates a template for a personalized Roommate Agreement, and downloads it as a PDF to the user's machine
'''
from fpdf import FPDF

class Roommate:
    '''
    Represents and holds the roommates individual information and responsibliites 
    Attributes:
        name(string): the name of the roommate
        split_list(list): this is a list that stores details such as rent, security deposit, and utilities
        busy_days(set): a set holds unique values only. In this case it will set the days when the roommate is busy

    Returns:
        get_free_days() returns the days "roommate" would not be busy

    '''
    # NEED TO ADD CONTACT INFO!!!
    # a set of days to be used later in order to calculate the days that a roommate is busy
    all_days = {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"}

    def __init__(self, name):
        """ Arg: name(str): name of the roomate"""
        self.name = name
        self.split_list = [] # list of bills divided per roomate
        self.busy_days = set() # will be used to capture a roommate's busy days

    def add_split(self, rent_split, utility_split, deposit_split): # sets the split list to become the rent, utility and deposit responsibilities per roomate
        """
        Arg:
            rent_split(float): the rent that will be split
            utility_split(float): utilitites that will be split 
            deposite_split(float): holds the deposit that will be split 
        """
        self.split_list = [rent_split, utility_split, deposit_split]

    def set_busy_days(self, days): # Sets only hold unqiue values not same numbers or days of the week 
        """Args: days(list): lists the days roommate is unavaliable"""
        self.busy_days = set(day.strip().lower() for day in days) # cleans up user input to match with the all_days set 

    def get_free_days(self): # subtracts the day variables to get avaliable days, for one roomate
        """Returns: what days roommate is avaliable """
        return Roommate.all_days - self.busy_days
    
    def input_schedule(self):
        days = input(f"Enter {self.name}'s busy days (comma-separated like: Monday, Friday): ")
        self.set_busy_days([d.strip() for d in days.split(",")])

    def __repr__(self): # display the split in a formatted fashion
        """Returns: string of roommates free days and assigned responsilitites """
        return (f"{self.name.title()}'s Responsibilities:\n"
                f"  Rent: ${self.split_list[0]}\n"
                f"  Utilities: ${self.split_list[1]}\n"
                f"  Security Deposit: ${self.split_list[2]}\n"
                f"  Free Days: {', '.join(day.capitalize() for day in sorted(self.get_free_days()))}\n") # trying to make this more official looking

class Bill:
    '''
    Calculate the split in financial responsibilities per roomate.

    Attributes:
        rent(float): total rent 
        utilitites(float): total utilities
        deposit(float): total deposit 
        period(str): description of the billling period  
    '''
    def __init__(self, rent, utilities, deposit, period): # requires full rent, utility fees and deposit amount, period requires specific format
        """
        Args:
            rent(float): total rent 
            utilitites(float): total utilities
            deposit(float): total deposit 
            period(str): description of the billling period
        """
        self.rent = rent
        self.utilities = utilities
        self.deposit = deposit
        self.period = period # billing period e.g May 2025

    def split(self, roommates): # calculate splits in financial by roomate 
        """Arg: roommates(list): list of roomate instances """
        # calculate number of roomates 
        num = len(roommates) 
        rent_split = round(self.rent / num, 2)
        utility_split = round(self.utilities / num, 2)
        deposit_split = round(self.deposit / num, 2)

        for rm in roommates:# calls the roommmate function 
            rm.add_split(rent_split, utility_split, deposit_split)  


class Pdf():
    '''
    Creates and saves a PDF consisting of roommate responsibliites and agreements

    Attributes:
        filename(str): name of the PDF file that will be created and saved
    '''

    def __init__(self, filename):
        """Arg: filename(str): namee of the PDF file """
        self.filename = filename
        # create FPDF instance and adds it to add_page
        self.pdf = FPDF('P', 'mm', 'Letter')
        self.pdf.add_page()
        # create new page if the first one runs out of room
        self.pdf.set_auto_page_break(True, 10)
        # specify fonts ( in our case, times font, regular type and 12 pts )
        self.pdf.set_font('times', '', 12)

    def generate(self, roommates, bill, rules_text, cleaning_days, chores):
        """
        Args:
            roommates(list): list of roommates 
            bill(bill): bill instnance
            rules_text(str): house rules 
            cleaning_days(list): similar freedays among roommates
            chores(list): list of chores 

        Side effect: creates and saves a formated PDF 
        """
        # create a title for the PDF 
        self.pdf.set_font('times', 'B', 16)
        # creates a centered title 
        self.pdf.cell(0, 10, f"\nRoommate Agreement - {bill.period}", ln = 1, align = 'C') # ln = 1 means ln = true, this is basically a \n 
        self.pdf.ln()

        # Roommate information
        # subheader
        self.pdf.set_font('times', 'B', 12)
        self.pdf.cell(0, 10, "Roommate Responsibilities:", ln = 1)  
        # information
        self.pdf.set_font("times", '' , 12)
        for rm in roommates:
            self.pdf.multi_cell(0, 10, str(rm))
            self.pdf.ln(2) # creates aligned spacing 
        self.pdf.ln()

        # agreement terms
        # subheader
        self.pdf.set_font('times', 'B', 12)
        self.pdf.cell(0, 10, "\n----- Agreement Terms -----", ln = 1)
        self.pdf.ln()
        # information
        self.pdf.set_font('times', '', 12)
        self.pdf.multi_cell(0, 10, rules_text.strip()) # contains the house rules 
        self.pdf.ln()
        
        # chore chart 
        # subheader 
        self.pdf.set_font('times', 'B', 12)
        self.pdf.cell(0, 10, "----- Chore Assignment -----", ln = 1)
        self.pdf.ln()
        
        # Table header
        self.pdf.set_font('times', 'B', 11)
        self.pdf.cell(90, 10, "Chore", border = 1)
        self.pdf.cell(90, 10, "Assigned To", border = 1, ln = 1)
        self.pdf.ln()

        # table set up and information
        self.pdf.set_font('times', '', 12)
        self.pdf.set_font('times', '', 11)
        for chore in chores:
            self.pdf.cell(90, 10, chore, border = 1)
            self.pdf.cell(90, 10, "__________________", border = 1, ln = 1) # blank header for format 
        self.pdf.multi_cell(0, 10,
            "Tenants may assign chores according to their schedules. "
            "All roommates are expected to follow the responsibilities outlined in this agreement. "
            "If chores need to be reassigned, the change must be agreed upon by all affected roommates."
        )
        self.pdf.ln()
        
        # ensure that the table isnt split into two pages 
        space = (len(chores) + 2) * 10
        if self.pdf.get_y() + space > 270:
            self.pdf.add_page()

        # suggested cleaning day(s)
        # sub header 
        self.pdf.set_font('times', 'B', 12)
        self.pdf.cell(0, 10, "Suggested Cleaning Day(s):", ln = 1) # creates the days header
        # information
        self.pdf.set_font('times', '', 12)
        if cleaning_days:
            self.pdf.cell(0, 10, ", ".join(sorted(cleaning_days)).capitalize(), ln = 1) # lists the day roommates can clean
        else:
            self.pdf.cell(0, 10, "No common free day found. Consider rotating responsibilities.", ln = 1)
        self.pdf.ln()

        # save the PDF 
        self.pdf.output(self.filename)
        print(f"\nPDF saved as: {self.filename}")
        print("Thanks for using our roommate agreement generator, where we help keep the peace & split with ease")

# We could have made a chores class but since we are on a tight schedule we are leaving this stray. 
# in the future if we wished to expand this project, we would likely create a chores class
def find_common_free_day(roommates):
    """
    Args: roommates(list): lists the roommates
    Returns: a list of roommates shared free days or an empty list
    """
    if not roommates:
        return [] # for if no roomates, no days to comapre to 

    common_days = roommates[0].get_free_days()
    for rm in roommates[1:]:
        common_days = common_days & rm.get_free_days() # finds the common days between roommates 

    return sorted(common_days)

def get_chores():
    """Returns: a formmated list of the chores"""
    chores_input = input("Enter chores separated by commas (e.g., Dishes, Vacuum, Trash): ")
    chores = [chore.strip().capitalize() for chore in chores_input.split(",") if chore.strip()]
    return chores


def main():
    print("-----Roommate Agreement Generator-----\n")

    # ask how many roommates there are 
    while True:
        try:
            num_roommates = int(input("How many roommates (min 2:max 5): ").strip())
            if num_roommates >5:
                raise ValueError("You reached the max amount of roommates")
            if num_roommates <2:
                raise ValueError("You need at least 2 roommates")
        except ValueError:
            print(f"{ValueError}:Invalid, try again")
            continue 
    
        # using a loop to create instances of roomates
        roommates = [] # empty list to be filled with instances of Roommate()
        for number in range(num_roommates): 
            name = input(f"Roomate {len(roommates) + 1 }'s name, or type F to finish: " + '\n').strip()
            if name.lower() == 'f': 
                break
            elif name == '': # make sure name isnt empty
                print('You must provide a valid name. Please Try again\n')
                continue
            roommates.append(Roommate(name)) # can also put instance of roomate in a variable if need be
        
        # troubleshoot a value less than 2 
        if len(roommates) < 2:
            raise ValueError ('You must have at least 2 roommates')
        else:
            break
        
    for rm in roommates: 
        rm.input_schedule()


    # input for information used in the classes 
    rent = float(input("Enter total rent amount: "))
    utilities = float(input("Enter total utilities amount: "))
    deposit = float(input("Enter total security deposit amount: "))
    period = input("Enter billing period (e.g., May 2025): ").strip()

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
    billing_period = period.lower().replace(' ', '_')
    report = Pdf(f"roommate_agreement_{billing_period}.pdf") # dynamic file name based on billing period
    report.generate(roommates, bill, rules, cleaning_days, chores)


if __name__ == "__main__":
    main()
