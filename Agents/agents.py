import random
import copy

bitstring_length = 9

print("Basic Agent Simulator")
print(" ")

agents = {"m" : [0,1,0,1,0,0], "f":[1,0,0,1,0,1], "v":[0,1,0,0,1,0], "n":[1,0,0,0,1,1], "y":[1,0,0,1,0,0], "c":[0,0,0,1,0,1] }

def compare(s1, s2):
	score = 0
	for i in range(len(s1)):
		score += 1 - abs(s1[i] - s2[i])
	return (score/bitstring_length)**5

class species:
	def __init__(self, agents):
		self.agents = copy.deepcopy(agents)
		for ag in self.agents:
			for i in range(bitstring_length - 6):
				self.agents[ag].append(random.uniform(0,1))
		#print(self.agents)

sp = []
for i in range(5):
	sp.append(species(agents))




def compare_my_agent():
	print("My agent has code:")
	print(my_agent)
	print("and will have effect")

	effects = []
	for i in range(len(sp)):
		for a in sp[i].agents:
			val = compare(my_agent, sp[i].agents[a])
			effects.append([i, a, val])

	effects.sort(key=lambda x: x[2], reverse = True)

	for e in effects:
		print("Species: ", e[0], ", organelle: ", e[1], ", strength: ", int(e[2]*100), "%")
	print(" ")


my_agent = []
for i in range(bitstring_length):
	my_agent.append(random.uniform(0,1))

print("Picking a Random Agent")
compare_my_agent()


my_agent = sp[0].agents["m"]

print("Targeting species 0 mitochondrion")
compare_my_agent()