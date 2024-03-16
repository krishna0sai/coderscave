import tkinter as tk
from tkinter import messagebox

class ExpenseSharingApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Expense Sharing App")
        self.window.geometry("400x400")

        self.expenses = []
        self.owed_amounts = []
        self.create_widgets()

    def create_widgets(self):
        
        name_label = tk.Label(self.window, text="Expense Name:")
        name_label.pack()
        self.name_entry = tk.Entry(self.window)
        self.name_entry.pack()

        
        amount_label = tk.Label(self.window, text="Expense Amount:")
        amount_label.pack()
        self.amount_entry = tk.Entry(self.window)
        self.amount_entry.pack()

        
        add_button = tk.Button(self.window, text="Add Expense", command=self.add_expense)
        add_button.pack()

        
        self.expense_listbox = tk.Listbox(self.window, width=50, height=10)
        self.expense_listbox.pack()

        
        split_button = tk.Button(self.window, text="Split Expenses", command=self.split_expenses)
        split_button.pack()

        
        num_friends_label = tk.Label(self.window, text="Number of Friends:")
        num_friends_label.pack()
        self.num_friends_entry = tk.Entry(self.window)
        self.num_friends_entry.pack()

        
        self.owed_listbox = tk.Listbox(self.window, width=50, height=10)
        self.owed_listbox.pack()

        
        settle_button = tk.Button(self.window, text="Settle Up", command=self.settle_up)
        settle_button.pack()

    def add_expense(self):
        name = self.name_entry.get()
        amount = float(self.amount_entry.get())

        if name and amount:
            expense = {"name": name, "amount": amount}
            self.expenses.append(expense)
            self.update_expense_listbox()
            self.name_entry.delete(0, tk.END)
            self.amount_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Expense name and amount are required.")

    def update_expense_listbox(self):
        self.expense_listbox.delete(0, tk.END)
        for expense in self.expenses:
            self.expense_listbox.insert(tk.END, f"{expense['name']}: ₹{expense['amount']}")

    def split_expenses(self):
        num_friends = int(self.num_friends_entry.get())

        if num_friends <= 0:
            messagebox.showerror("Error", "Number of friends must be greater than zero.")
        else:
            
            self.owed_listbox.delete(0, tk.END)
            self.owed_amounts.clear()

            for expense in self.expenses:
                amount_per_friend = expense["amount"] / num_friends
                for i in range(num_friends):
                    self.create_owed_amount(expense["name"], amount_per_friend, f"Friend {i+1}")

    def create_owed_amount(self, payer, amount, payee):
        owe_amount = {"payer": payer, "payee": payee, "amount": amount}
        self.owed_amounts.append(owe_amount)
        owe_string = f"{owe_amount['payer']} owes {owe_amount['payee']} ₹{owe_amount['amount']}"
        self.owed_listbox.insert(tk.END, owe_string)

    def settle_up(self):
        if not self.owed_amounts:
            messagebox.showinfo("Info", "No expenses to settle up.")
        else:
            total_owed = sum(owe_amount["amount"] for owe_amount in self.owed_amounts)
            total_friends = len(set(owe_amount["payee"] for owe_amount in self.owed_amounts))

            amount_per_friend = total_owed / total_friends

            
            for owe_amount in self.owed_amounts:
                owe_amount["amount"] -= amount_per_friend

            
            self.owed_amounts = [owe_amount for owe_amount in self.owed_amounts if owe_amount["amount"] > 0]

            
            self.owed_listbox.delete(0, tk.END)
            for owe_amount in self.owed_amounts:
                owe_string = f"{owe_amount['payer']} owes {owe_amount['payee']} ₹{owe_amount['amount']}"
                self.owed_listbox.insert(tk.END, owe_string)

            
            if not self.owed_amounts:
                messagebox.showinfo("Info", "All expenses are settled.")

if __name__ == "__main__":
    app = ExpenseSharingApp()
    app.window.mainloop()