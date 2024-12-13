from PyQt6.QtWidgets import *
from gui import *
import csv
import os

class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        """
        Sets up the GUI and connects each button to its function.
        """
        super().__init__()
        self.setupUi(self)

        self.pin_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.search_button.clicked.connect(lambda : self.search())
        self.enter_button.clicked.connect(lambda: self.action())
        self.exit_button.clicked.connect(lambda: self.clear())
        self.account_balance = 0

    def action(self) -> None:
        """
        Performs the action selected (withdraw or deposit) based on the input
        and updates the CSV file.
        """
        try:
            amount = int(self.amount_input.text().strip())
        except ValueError:
            self.balance_label.setText("Please enter a valid amount")
            return

        if self.withdraw_button.isChecked():
            if amount > self.account_balance:
                self.balance_label.setText(f"Insufficient funds")
                return
            new_balance = self.account_balance - amount
            self.account_balance = new_balance
            self.balance_label.setText(f"New balance: ${new_balance}")
        elif self.deposit_button.isChecked():
            new_balance = self.account_balance + amount
            self.account_balance = new_balance
            self.balance_label.setText(f"New balance: ${new_balance}")

        self.update_csv_balance()

    def update_csv_balance(self) -> None:
        """
        This function updates the account balance in the CSV file.
        """
        first_name = self.firstname_input.text().strip()
        last_name = self.lastname_input.text().strip()
        pin_num = self.pin_input.text().strip()

        file_path = 'atm.csv'
        rows = []

        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            found = False
            for row in reader:
                if (row['First name'].strip().lower() == first_name.lower() and
                    row['Last name'].strip().lower() == last_name.lower() and
                    row['PIN'].strip() == pin_num):
                    row['Account Balance'] = str(self.account_balance)
                    found = True
                rows.append(row)

        if found:
            with open(file_path, mode='w', newline='') as file:
                fieldnames = ['First name', 'Last name', 'PIN', 'Account Balance']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)

    def search(self) -> None:
        """
        Searches for a user's account in the CSV file and displays the current
        account balance.
        If there is no account, it will ask the user if they want to create an account.
        """
        first_name = self.firstname_input.text().strip()
        last_name = self.lastname_input.text().strip()
        pin_num = self.pin_input.text().strip()

        if not first_name or not last_name or not pin_num:
            self.status_label.setText("Please fill all fields.")
            return

        file_path = 'atm.csv'
        entry_found = False

        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if (row['First name'].strip().lower() == first_name.lower() and
                    row['Last name'].strip().lower() == last_name.lower() and
                    row['PIN'].strip() == pin_num):
                    self.account_balance = float(row['Account Balance'])
                    self.status_label.setText(f"Account balance: ${self.account_balance}\n What would you like to do?")
                    entry_found = True
                    break

        if not entry_found:
            self.prompt_account_creation()
            #self.status_label.setText(f"Account not found\n Would you like to create an account?")

    def prompt_account_creation(self) -> None:
        """
        Prompts the user with a dialog box to create an account if it is not found.
        """
        reply = QMessageBox.question(self, 'Account not found',
                                     "Account not found. Would you like to create an account?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            self.create_account()
        else:
            self.status_label.setText('Account creation cancelled')
            self.firstname_input.clear()
            self.lastname_input.clear()
            self.pin_input.clear()

    def create_account(self) -> None:
        """
        Creates a new account by appending first name, last name and PIN to the CSV file.
        """
        first_name = self.firstname_input.text().strip()
        last_name = self.lastname_input.text().strip()
        pin_num = self.pin_input.text().strip()

        if not first_name or not last_name or not pin_num:
            self.status_label.setText('Fill all fields to create an account')
            return

        file_path = 'atm.csv'
        with open(file_path, mode = 'a', newline='') as file:
            fieldnames = ['First name', 'Last name', 'PIN', 'Account Balance']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writerow({'First name': first_name, 'Last name': last_name, 'PIN': pin_num,
                             'Account Balance': '0'})

            self.status_label.setText(f"Account created for {first_name} {last_name}")
            self.firstname_input.clear()
            self.lastname_input.clear()
            self.pin_input.clear()

    def clear(self) -> None:
        """
        Clears and resets the input fields.
        """
        self.withdraw_button.setChecked(False)
        self.deposit_button.setChecked(False)
        self.firstname_input.clear()
        self.lastname_input.clear()
        self.pin_input.clear()
        self.amount_input.clear()
        self.status_label.clear()
        self.balance_label.clear()

