
#agents system prototype

import random
import itertools

base_values = {"Chemoplast" : "TACCTCGA", 
			"Chloroplast" : "CTCACATT", 
			"Cytoplasm" : "AGCTTAGA",
			"Mitochondria" : "GGAGAAGA",
			"Sulphur Mitochondria" : "TTTGGCGG",
			"Agent Gland" : "TCCCGCAG",
			"Nucleus" : "GACCGACT",
			"Lysosomes" : "GTTCTTTA",
			"Flagella" : "GGAAGTGC",
			"Pilus" : "CCGGTCCG"}

weights = {"Chemoplast" : 1, 
			"Chloroplast" : 1, 
			"Cytoplasm" : 0,
			"Mitochondria" : 0,
			"Sulphur Mitochondria" : 1,
			"Agent Gland" : 4,
			"Nucleus" : 2,
			"Lysosomes" : 1,
			"Flagella" : 4,
			"Pilus" : 1}

#take a string and change n letters in it at random
def change_n_letters(string, n):
	if n > len(string):
		print "Error, tried to change too many letters of a string"
		return string
	else:
		#choose which letters to change
		letters_to_change = [i for i in range(len(string))]
		for j in range(len(string) - n):
			letters_to_change.remove(random.choice(letters_to_change))
		#change the letters to something new
		working_string = list(string)
		for position in letters_to_change:
			choices = ["A", "C", "G", "T"]
			choices.remove(working_string[position])
			choice = random.choice(choices)
			working_string[position] = choice

		return "".join(working_string)

#compare two codes for similarity
def compare_codes(string1, string2):
	s1 = list(string1)
	s2 = list(string2)
	output = 0
	for i in range(len(s1)):
		if s1[i] == s2[i]:
			output += 1
	return output

class species:
	def __init__(self):
		#copy the base values for the codes for your organelles
		self.codes = dict(base_values)
		#mutate the base values a little bit
		for code in self.codes.keys():
			self.codes[code] = change_n_letters(self.codes[code], 4)

jeff = species()
geoff = species()

def score_code(string, species):
	score = 0
	for organelle in species.codes.keys():
		this_score = compare_codes(string, species.codes[organelle])
		multiplier = weights[organelle]
		score += this_score*multiplier
	return score


#find the best agents for attacking Jeff
def compute_best_codes_brute_force(species):
	top_codes = []

	counter = [0 for i in range(8)]
	time = 0
	top_score = 0
	while 1:
		#compute which code to try now
		trying_code = ""
		for number in counter:
			if number is 0:
				trying_code += "A"
			if number is 1:
				trying_code += "C"
			if number is 2:
				trying_code += "G"
			if number is 3:
				trying_code += "T"
		#check how good that code is
		score = score_code(trying_code, species)
		#if the code is good enough add it to the list of top scores
		if score >= top_score*0.9:
			top_codes.append([trying_code, score])
		if score > top_score:
			top_score = score
		#increase the counter
		counter[0] += 1
		for i in range(len(counter) - 1):
			if counter[i] == 5:
				counter[i] = 0
				counter[i + 1] += 1
		if counter[len(counter) - 1] == 5:
			break
		time += 1
		if time % 10000 == 0:
			print time

	return sorted(top_codes, key=lambda x: x[1], reverse = True)
#brute force computation is slow, to see that uncomment this line!
#print "Brute force computation vs Jeff : ", compute_best_codes_brute_force(jeff)

#construct the most effective sequence
def compute_best_codes_by_construction(list_of_species):
	letters = ["A", "C", "G", "T"]
	output = []
	#for each letter
	for i in range(8):
		#keep a list of which letter is best
		current_scores = [0,0,0,0]
		for species in list_of_species:
			for key in species.codes.keys():
				#award points for matching the letter
				multipler = weights[key]
				if species.codes[key][i] == letters[0]:
					current_scores[0] += multipler
				if species.codes[key][i] == letters[1]:
					current_scores[1] += multipler
				if species.codes[key][i] == letters[2]:
					current_scores[2] += multipler
				if species.codes[key][i] == letters[3]:
					current_scores[3] += multipler
		#use the scores to determine the best letter
		high_score = 0
		letters_to_check = [0,1,2,3]
		random.shuffle(letters_to_check)
		for index in letters_to_check:
			if current_scores[index] > high_score:
				high_score = current_scores[index]
				best_letter = index
		output.append(letters[best_letter])
	return "".join(output)

print "Construction computation vs Jeff : ", compute_best_codes_by_construction([jeff])

print "Construction computation vs Jeff and Geoff", compute_best_codes_by_construction([jeff, geoff])

