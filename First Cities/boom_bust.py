
import random

#how much does the bank move it's capital requirements?
capital_increment = 0.03
captial_decrement = 0.01
#what size should the capital cushion be?
captial_max = 0.3
captial_min = 0.05
#how many steps?
length_of_simulation = 1000
#how frequently should a new company start
chance_of_new_company = 0.2
#what is the return on loans to the companies
rate_of_return = 1.05
#how risky are the companies?
chance_of_returning_money = 0.9
#how long can a company go before it runs out of money when getting no new loans?
trouble_before_bankruptcy = 2

#are you going to allow bank bailouts! COMMUNISM I TELLS YOU!
bailouts = True

#company class, many of these will be created and destroyed
class company:
	def __init__(self, number):
		self.number = number
		self.debts = []
		self.trouble = 0

#bank class, only one of these will exist
class bank:
	def __init__(self):
		self.cash = 100
		self.total_money = self.cash
		self.old_total_money = self.cash
		self.captial_requirement = 0.1

	#the bank computes if it wants to offer a loan at this time
	def approve_loan(self):
		self.compute_total_money()

		if self.cash < self.captial_requirement*self.total_money or self.cash <= 10:
			return False
		else:
			return True

	#compute the banks total worth, all debts + cash
	def compute_total_money(self):
		total_money = 0
		for companie in companies:
			for i in range(len(companie.debts)):
				total_money += companie.debts[i]
		total_money += self.cash
		self.total_money = total_money


	#if you lost money then increase your captial requirements, if you made money decrease them
	def profit_and_loss(self):
		self.old_total_money = self.total_money
		self.compute_total_money()
		if self.total_money > self.old_total_money and self.captial_requirement >= captial_min:
			self.captial_requirement -= captial_decrement
		elif self.total_money < self.old_total_money and self.captial_requirement <= captial_max:
			self.captial_requirement += capital_increment


the_bank = bank()

companies = []

data = []

for i in range(length_of_simulation):
	#work out net worth
	the_bank.profit_and_loss()
	#bailout if required
	if bailouts and the_bank.total_money <= 100:
		the_bank.cash = 100
	#found a new company at random
	if random.uniform(0,1) < chance_of_new_company:
		if the_bank.approve_loan():
			new_company = company(len(companies))
			new_company.debts.append(10*rate_of_return)
			the_bank.cash -= 10
			companies.append(new_company)
	#for each company make a decision
	for companie in companies:
		#if the company is operating normally
		if companie.trouble == 0:
			#pay back loans
			if random.uniform(0,1) < chance_of_returning_money:
				for i in range(len(companie.debts)):
					if companie.debts[i] >= 1:
						companie.debts[i] -= 1
						the_bank.cash += 1

				companie.debts[:] = (value for value in companie.debts if value >= 1)				

			#ask for a loan
			else:
				if the_bank.approve_loan():
					companie.debts.append(10*rate_of_return)
					the_bank.cash -= 10

				#if the loan is not approved then the company gets into trouble
				else:
					companie.trouble += 1
		#if in trouble ask for a loan
		else:
			#the loan comes through in time
			if the_bank.approve_loan():
				companie.debts.append(10*rate_of_return)
				the_bank.cash -= 10
				companie.trouble = 0
			#the company still needs money!
			else:
				companie.trouble += 1
				#the trouble has got so bad the company goes bankrupt
				if companie.trouble >= trouble_before_bankruptcy:
					companies.remove(companie)


			
	#this is the output you see, number of companies operating the in the economy
	data.append(len(companies))

print data