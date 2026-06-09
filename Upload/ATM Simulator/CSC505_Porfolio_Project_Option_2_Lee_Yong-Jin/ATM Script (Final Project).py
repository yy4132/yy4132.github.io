import random

pin = ["1113", "4343", "6254", "1134"]
balance = [6421.43, 51535.32, 1523.12, 532532.54]
count = 3

def receipt():
	choice = input("Would you like to have your receipt? (Y/N)\n")
	if choice == 'Y':
		print("Your transaction is now complete.\n")
		print("Transaction number: ", random.randint(10000, 1000000), "\n")
		print("Thank you and have a nice day.")
		exit()
	if choice == 'N':
		print("Thank you and have a nice day.")
		exit()

def withdraw(balance):
	print("Welcome to ATM System.\n")
	amount = float(input("\nPlease enter the amount you want to withdraw: "))
	for elements in balance:
		if float(balance[pin.index(enter_pin)] - amount) > 0:
			amount = float(balance[pin.index(enter_pin)]) - amount
			print("\nYou now have " + str(round(amount, 2)) + ".\n")
			print("\nDispensing money ...\n")
			receipt()
		else:
			print("\nYou have insufficent funds to withdraw this amount.\n")
			print("\nPlease deposit more funds first.\n")
			
while True:
	enter_pin = input("Please enter your PIN.\n")
	if enter_pin in pin:
		print("Your PIN was successful.\n")
		withdraw(balance)
			break
	if enter_pin not in pin:
		print("The PIN you entered is incorrect. You have " + str(count-1) + " attempts remaining.")
		count -= 1
	if count == 0:
		print("You have failed 3 attempts.\n")
		print("Your card is locked and will now be ejected.\n")
		exit()
	else:
		break

if __name__ == '__main__':
	pass