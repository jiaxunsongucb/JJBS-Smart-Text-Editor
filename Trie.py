from collections import deque

class Trie():
    
    class TrieNode():
        def __init__(self, word=""):
            self.letters = dict() # key: letter, value: TrieNodes
            self.end = False
            self.word = word
        
        def insert(self, l):
            if not self.contains(l):
                self.letters[l] = Trie.TrieNode(self.word + l)
        
        def contains(self, l):
            return l in self.letters
        
        def getChild(self, l):
            return self.letters[l]
        
        def setEnd(self):
            self.end = True
        
        def isEnd(self):
            return self.end
        
        def getWord(self):
            return self.word
    
    def __insert(node, word):
        if len(word) == 0:
            node.setEnd()
        else:
            node.insert(word[0])
            Trie.__insert(node.getChild(word[0]), word[1:])
        return node
    
    def __search(node, word):
        if len(word) == 0:
            return node.isEnd()
        elif not node.contains(word[0]):
            return False
        else:
            return Trie.__search(node.getChild(word[0]), word[1:])
        
    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.root = Trie.TrieNode()

    def insert_r(self, word):
        """
        Inserts a word into the trie.
        :type word: str
        :rtype: void
        """
        word = word.lower()
        self.root = Trie.__insert(self.root, word)
    
    def insert(self, word):
        """
        Inserts a word into the trie.
        :type word: str
        :rtype: void
        """
        currNode = self.root
        p = 0
        while p < len(word):
            currNode.insert(word[p])
            currNode = currNode.getChild(word[p])
            p += 1
        currNode.setEnd()
    
    def search(self, word):
        """
        Returns if the word is in the trie.
        :type word: str
        :rtype: bool
        """
        word = word.lower()
        return Trie.__search(self.root, word)
    
    def prediction(self, prefix, limit):
        prefix = prefix.lower()
        currNode = self.root
        result = []
        
        while len(prefix) != 0:
            if not currNode.contains(prefix[0]):
                return result
            currNode = currNode.getChild(prefix[0])
            prefix = prefix[1:]
        
        q = deque()
        q.append(currNode)
        while len(q) and len(result) < limit:
            currtNode = q.popleft()
            if currtNode.isEnd():
                result.append(currtNode.getWord())
            for l in currtNode.letters:
                q.append(currtNode.letters[l])
        return result


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
