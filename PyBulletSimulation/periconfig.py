import sys


class Peri():
	def __init__(self):
		self.limbassoc = {}#dictionary of limbs => array of tuples of limb/time info
	
	def sortLimb(self):
		#print(len(list(self.limbassoc.keys())))
		for j in range(len(list(self.limbassoc.keys()))):
			plans = self.limbassoc[j]
			#print(len(plans))
			plans.sort(key= lambda x: x[2])
	def wrapped_export(self, t, i):
		#return a list
		#print(t)
		toreturn = []
		for j in range(len(list(self.limbassoc.keys()))):
			plans = self.limbassoc[j] #yes its zero-indexed. but you knew that right?
			k = 0
			#print(plans[k][2])
			while k < len(plans) and plans[k][2] <= t:
				#print(plans[k][2])
				theplan = plans[k]
				k += 1
			toreturn.append(theplan[0])
			toreturn.append(theplan[1]) #add in the strength and direction
		#print("----")
		return toreturn
		
peri = Peri()
rawconfig = open("configuration.txt", "r")
myline = rawconfig.readline()

while myline:
	entry = myline.strip().split(",")
	
	if len(entry) == 4: #hopefully will filter out bad stuff
		#print(float(entry[3]))
		if not (int(entry[0]) in peri.limbassoc):
			peri.limbassoc[int(entry[0])] = []
		peri.limbassoc[int(entry[0])].append((float(entry[1]), float(entry[2]), float(entry[3])))
	
	
	myline = rawconfig.readline()

rawconfig.close()

peri.sortLimb()