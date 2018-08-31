import queue
		
class TrieNode:
	children = dict()
	word =""
	isWord = False
	
	
	def __init__(self,input=None):
		if input == None:
			self.word = ''
		else:
			self.word = input
		self.children = dict()
		self.isWord = False
		
	def getWord(self):
		return self.word
		
	def setEnd(self, y):
		self.isWord = y
		
	def isEnd(self):
		return self.isWord
		
	def insert (self,x):
		if x in self.children:
			return None
		child = TrieNode(self.word + x)
		self.children[x] = child;
		return
			
	def getChild(self, x):
		if x in self.children:
			return self.children[x]
		else:
			return None
		
	def getChildrenCharacters(self):
		return self.children.keys()
		
class Trie:
	
	dicroot = None
	
	def __init__(self):
		self.dicroot = TrieNode()
		
# defining method to insert to the Trie Dictionary		
	def insert(self, x):
		curnode = self.dicroot
		count = 0
		x = x.lower()
		while count < len(x)-1:
			charins = x[count]
			curnode.insert(charins)
			curnode = curnode.getChild(charins)
			count +=1
		charins = x[count]
		if curnode.insert(charins)== None:
			if curnode.getChild(charins).isEnd():
				return False
			else:
				curnode.getChild(charins).setEnd(True)
				return True
		else:
			curnode.insert(charins)
			curnode.getChild(charins).setEnd(True)
			return True

			
#judging whether an insertion is a real word	 
	def search(self,x):
	 	curnode = self.dicroot
	 	count = 0
	 	x = x.lower()
	 	while count < len(x)-1:
	 		charins = x[count]
	 		if curnode.getChild(charins) == None:
	 			return False
	 		else:
	 			curnode = curnode.getChild(charins)
	 			count +=1
	 	charins = x[count]
	 	if curnode.getChild(charins)== None:
	 		return False
	 	else:
	 		return curnode.getChild(charins).isEnd()



# predict a word according to the prefex(already inserted word) and the number of suggested words; within the shortest path	 		
	def prediction(self, prefix, numwords):
	 	curnode = self.dicroot
	 	prefix = prefix.lower()
	 	q = queue.Queue(0)    # a queue to store words for later check and put them in suglist. Order of the queue is character distance from prefix
	 	suglist = [] #the list to store prediction words
	 	q.put(curnode) 
	 	for i in prefix:
	 		curnode = curnode.getChild(i)
	 		if curnode == None:
	 			return suglist   #if you cannot search along the prefix letters, return an empty suggestion list
	 	q.get()  #delete the dicroot from the queue
	 	while len(suglist)<numwords:
	 		if curnode.isEnd():
	 			suglist.append(curnode.getWord())   #if the current node itself is a word, add it to the suggestion list
	 		nextchars = curnode.getChildrenCharacters()   #traverse the current node's next characters and add them to the queue one by one
	 		if nextchars!= None:
	 			for i in nextchars:
	 				q.put(curnode.getChild(i))
	 		if q.qsize()!=0:
	 			curnode = q.get()    #delete the first node in the queue
	 		else:
	 			return suglist
	 	return suglist


if __name__ == '__main__':	
	x = Trie()
	x.insert("haha")
	x.insert("hey")
	x.insert("ji")
	x.insert("ju")
	x.insert("jupes")
	x.insert("happy")
	x.insert("hallo")
	x.insert("harley")
	x.insert("Jason")
	x.insert("jokes")
	x.insert("jakes")
	x.insert("james")
	x.insert("jam")
	x.insert("jaail")
	x.insert("jail")
	print(x.prediction("ha",5))
	print(x.search("Ber"))
	print(x.search("happy"))
	print(x.prediction("okay",3))
