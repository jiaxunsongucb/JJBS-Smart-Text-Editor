from random import randint
from numpy.random import choice

def getRandomWord(listOfWords):
		r = len(listOfWords)
		i = randint(0,r-1)
		return listOfWords[i]

#This function (findchar) is adopted from a stackoverflow question:
#https://stackoverflow.com/questions/11122291/python-find-char-in-string-can-i-get-all-indexes
def findchar(s, ch):
	return [i for i, ltr in enumerate(s) if ltr == ch]

def format(output):
	o = output[5:]
	o = o.replace(" STOP", ".")

	#ends = findchar(o, ".")

	# for i in range(len(ends)):
	# 	print(o)
	# 	o = o[:i] + o[i].upper() + o[i:]

	if o[-1] != ".": 
		o+= "."

	o = o[0].upper() + o[1:]
	
	return o

#markov 
#Call Markov(filestring) 
#should contain methods to 
##train(filestring)
##generate()  //generates numWords amount of text
class Markov(object):
	
	"""docstring for ClassName"""
	def __init__(self, arg, num):
		#Number of words to generate by default
		self.fileString = arg
		self.numWords = num
		self.BigramDictionary = {}
		self.vocab = []


	def addStops(self):
		#take filestring and replace all end punctuation with STOP tokens
		
		aug = "STOP " + (self.fileString).replace(".", " STOP").replace("!", " STOP").replace("?", " STOP")
		
		return aug

	def train(self):
		#BDictionary = {}
		
		self.fileString = self.fileString.lower()
		fs = self.addStops()

		fslist = fs.split()

		start = fslist[0]
		prev = start 

		#iterate through each word
		for wi in range(len(fslist)-1):
			word = fslist[wi]
			nextword = fslist[wi + 1]
			 
			if word in self.BigramDictionary:
				if nextword in self.BigramDictionary[word]:
					(self.BigramDictionary[word])[nextword] += 1
				else:
					(self.BigramDictionary[word])[nextword] =  1
			else:
				self.BigramDictionary[word] = {nextword: 1}

		self.vocab = [word for word in self.BigramDictionary]


	def generate(self):
		
		num = self.numWords
		vocab = self.vocab
		
		start = "STOP"
		curr = start 

		output = start 

		while num > 0: 
			if curr in vocab: 
				nextdict = self.BigramDictionary[curr]
				nextlist = [word for word in nextdict] #get keys 
				nextprobs = [nextdict[word] for word in nextdict] #get vals 

				#get a random next word based on probability of that word
				chooseNext = choice(nextlist, 1, nextprobs)[0]

				output += " " + chooseNext
				curr = chooseNext
				num -= 1
			else:
				curr = getRandomWord(vocab)

		output = format(output)
		return output
		

###Example###
if __name__ == '__main__':
	astring = '''This promotional offer is provided by The New York Times in collaboration with Google 
	for use on the Google Store only and subject to the following terms. Offer ends December 31, 2017, 
	or while supplies last, but in no event after February 28, 2018. To be eligible to receive this offer, 
	ou must be located in the United States of America, as defined by your billing ZIP code, excluding 
	any of its territories, be age 13 or older and select a qualifying subscription to The New York Times. 
	To receive the Google Home, you need to redeem your promotional code, which requires you to have an 
	internet access and have, or activate, a Google Payments account and be signed-in to a Google account. 
	You will receive your promotional code in an email from The New York Times within 7 - 10 days after 
	subscribing to the qualifying subscription. To redeem your promotional code, visit store.google.com/
	product/google_home, add the Google Home to your cart, and enter your promotional code during checkout 
	to receive your 100 percent discounted Google Home. The Google Home discount will be applied at checkout. 
	Promotional codes cannot be used with Guest Checkout. [Promotional codes and] Google Home are provided 
	by Google. Promotional code must be redeemed by 3/14/18 or it will expire. Promotional codes may be 
	redeemed only on Google Store for eligible items as allowed by applicable laws. Promotional code is 
	good for one-time use only, is not stored value, has no cash value, is not reloadable, is not transferable, 
	and has no balance after use. Google and The New York Times are not liable for lost or stolen promotional codes, 
	or for expired promotional codes that are not redeemed within the redemption period. Offer subject to change 
	or cancellation at any time. These terms are subject to applicable laws and void where prohibited by 
	law. See additional Google Store Promotion Terms for more information.'''

	m = Markov(astring, 50)
	m.train()
	text = m.generate()

	print(text)