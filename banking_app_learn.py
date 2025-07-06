import re
from colorama import Fore, init, Style
from email_validator import validate_email, EmailNotValidError

# initialize colorama
init(autoreset=True)


class User:
    def __init__(self):
        self.user_info = {
            "firstname": '',
            "lastname": '',
            "gender": '',
            "age": 0,
            "phone": '',
            "email": ''
        }

    # ---- common functionality methods -----
    @staticmethod
    def common_header(info):
        if not isinstance(info, str) or info.isalpha():
            print(Fore.LIGHTRED_EX + f"\t Header info {info} should only contain letters")
        else:
            print(Fore.LIGHTGREEN_EX + f"\n\t****** {info.title()} Information ******\n" + Style.RESET_ALL)


    # ------ Generic user data validation method ------
    @staticmethod
    def validate_user_data(user_prompt, data_type=str, valid_range=None, validation_func=None):
        """
          Purpose: Validating and verifying user input
          Args:
               user_prompt: Message displayed  to user asking for user input.
               data_type: The data type of user input.
               valid_range: List of expected user input options.
               validation_func: Method to validate specific data input.
          Returns:
                 Validated user input
        """
        while True:
            try:
                user_input = input(user_prompt).strip()
                # check for empty values
                if not user_input:
                    print(Fore.LIGHTRED_EX + "\tNo user input detected, try again\n")
                    continue
                if data_type != str:
                    user_input = data_type(user_input)
                # check for unexpected inputs
                if valid_range and user_input not in valid_range:
                    print(Fore.LIGHTRED_EX + f"\t Input {user_input} is  not a listed option!\n")
                    continue
                # check for validation function errors
                if validation_func and not validation_func(user_input):
                    continue

                # successful data validation returns user input
                return  user_input

            except ValueError:
                print(Fore.LIGHTRED_EX + f"\tInvalid user input. Expected {data_type.__name__}\n")

    # ------ Instance variable validation methods ------

    @staticmethod
    def validate_firstname(firstname):
        """Validate firstname """
        if not re.match(r"^[a-zA-Z]+$", firstname):
            print(Fore.LIGHTRED_EX + f"\t{firstname} is a valid firstname\n")
            return False
        return True

    @staticmethod
    def validate_lastname(lastname):
        """ Validate lastname """
        if not re.match(r"^[a-zA-Z]+$", lastname):
            print(Fore.LIGHTRED_EX + f"\t{lastname} is not a valid lastname\n")
            return False
        return True

    @staticmethod
    def validate_gender(gender):
        """ Validate gender """
        try:
           gender_options = ["Male", "Female"]
           formated_gender = gender.title()
           if not re.match(r"^[a-zA-Z]+$", gender) or formated_gender not in gender_options:
               print(
                   Fore.LIGHTRED_EX +
                   f"\t{gender} is not valid, "
                   f"expected gender is {gender_options[0]} "
                   f"or {gender_options[1]}\n")
               return False
           return True
        except ValueError:
            print(Fore.LIGHTRED_EX + f"\t{gender} formating not supported!\n")
            return False


    @staticmethod
    def validate_age(age):
        try:
            user_age = int(age)
            if user_age <= 0 or user_age > 100:
                print(Fore.LIGHTRED_EX + f"\tAge should be between 1 to 100 years\n")
                return False
            return True
        except ValueError:
            print(Fore.LIGHTRED_EX + f"\tInvalid input {age}, age must be a number!\n")
            return False

    @staticmethod
    def validate_phone(phone):
        """ Validate phone number """
        if not re.match(r"^0+\d{9}$", phone):
            print(Fore.LIGHTRED_EX + "\tInvalid phone number! Must be 10 digits starting with 0\n")
            return False
        return True

    @staticmethod
    def validate_email(email):
        """ Validate email address """
        try:
            # validate and get info
            email_info = validate_email(email, check_deliverability=False)
            # normalized form
            email = email_info.normalized
            return True
        except EmailNotValidError as err:
            print(Fore.LIGHTRED_EX + f"\t Invalid email: { str(err)}")
            return False

    # ---- Instance variable validation methods end -----

    # user data collection method
    def collect_user_data(self):
        self.common_header("User KYC")

        # get firstname
        self.user_info['firstname'] = self.validate_user_data(
            "\tEnter firstname: ",
            validation_func=self.validate_firstname
        ).title()

        # get lastname
        self.user_info['lastname'] = self.validate_user_data(
            "\tEnter Lastname: ",
            validation_func=self.validate_lastname
        ).title()

        # get email
        self.user_info['email'] = self.validate_user_data(
            "\tEnter email: ",
            validation_func= self.validate_email
        ).lower()

        # get phone
        self.user_info['phone'] = self.validate_user_data(
            "\tEnter phone number: ",
            validation_func= self.validate_phone
        )

        # get age
        self.user_info['age'] = self.validate_user_data(
            "\tEnter Age: ",
            validation_func= self.validate_age
        )

        # get gender
        self.user_info["gender"] = self.validate_user_data(
            "\tEnter Gender: ",
            validation_func=self.validate_gender
        ).title()

    # Display user data
    def display_user_data(self, balance):
        self.common_header("User Account Summary")
        print(Fore.LIGHTCYAN_EX + f"\tName: {self.user_info['firstname']} {self.user_info['lastname']}")
        print(Fore.LIGHTCYAN_EX + f"\tEmail: {self.user_info['email']}")
        print(Fore.LIGHTCYAN_EX + f"\tPhone No: {self.user_info['phone']}")
        print(Fore.LIGHTCYAN_EX + f"\tGender: {self.user_info['gender']}")
        print(Fore.LIGHTCYAN_EX + f"\tAge: {self.user_info['age']}")
        print(Fore.LIGHTCYAN_EX + f"\tBalance: K{balance}\n")




# Bank Class
class Bank(User):
    def __init__(self):
        super().__init__()
        self.bank_account = {
            "balance": 0
        }

     # instance method validate account balance
    @staticmethod
    def validate_balance(balance):
        """" Validate account balance """
        try:
           balance = float(balance)
           if balance <= 0:
               print(Fore.LIGHTRED_EX + "\tInitial balance must be a positive number")
               return False
           return True
        except ValueError:
           print(Fore.LIGHTRED_EX + "\tInvalid initial balance amount!")
           return False

    #  ----- get account opening balance -----
    def get_account_balance(self):
        self.common_header("Initial Balance")
        self.bank_account = self.validate_user_data(
            "\tEnter opening balance: ",
            data_type=int,
            validation_func= self.validate_balance
        )

    # ------------ Transaction methods -----
    def deposit_cash(self, amount):
        """ Deposit Cash """
        try:
            amount = float(amount)
            if amount <= 0:
                print(Fore.LIGHTRED_EX + "\tDeposit amount should  be a positive number!")
                return
            self.bank_account['balance'] += amount
            print(Fore.LIGHTGREEN_EX + f"\tDeposit of K{amount} was successful, new balance is K{self.bank_account['balance']:.2f}")
        except ValueError:
            print(Fore.LIGHTRED_EX + "\tInvalid deposit amount")

    def withdraw_cash(self, amount):
        """ Withdraw Cash """
        try:
            amount = float(amount)
            if self.bank_account['balance'] <= amount:
                print(Fore.LIGHTRED_EX + "\tWithdraw failed!, You have insufficient balance.")
                return
            self.bank_account['balance'] -= amount
            print(Fore.LIGHTGREEN_EX +
                  f"\t{amount} withdrawn successfully, "
                  f"your new account balance is K{self.bank_account['balance']:.2f}"
                  )
        except ValueError:
            print(Fore.LIGHTRED_EX + f"\tInvalid withdraw amount {amount}")

    # banking transactions menu
    def bank_transactions_menu(self):
        while True:
            self.common_header("Bank Transaction Option")
            option = self.validate_user_data(
                "\t1. Deposit\n\t2. Withdraw\n\t3. Account Summary\n\t4. Exit\n\n\tChoose an option: ",
                data_type=int,
                valid_range=range(1, 5),
                validation_func=self.validate_balance
            )

            if option == 1: # depositing
                amount = self.validate_user_data(
                    "\tEnter amount to deposit: ",
                    data_type=float,
                    validation_func= self.validate_balance
                )

                self.deposit_cash(amount)

            elif option == 2: # Withdraw
                amount = self.validate_user_data(
                    "\tEnter amount to withdraw: ",
                    data_type=float,
                    validation_func= self.validate_balance
                )
                self.withdraw_cash(amount)
            elif option == 3:
                self.display_user_data(self.bank_account['balance'])

            else:
                print(Fore.LIGHTCYAN_EX + f"\tProgram gracefully stoped by user!")
                break

    #  # display transaction information
    def display_bank_transactions(self):
        self.common_header("Banking transactions")
        self.collect_user_data()
        self.bank_transactions_menu()



# RUN APP
if __name__ == "__main__":
    try:
        bank = Bank()
        bank.display_bank_transactions()
    except KeyboardInterrupt:
        print(Fore.LIGHTRED_EX + "\n\tUser ended the program, abruptly")