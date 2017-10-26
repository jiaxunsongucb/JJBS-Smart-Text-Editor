# -*- coding: utf-8 -*-
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import os
import re
import http.client as httplib
from hashlib import md5 as md5
import urllib
import random
import json
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from scipy.misc import imread
from wordcloud import WordCloud,ImageColorGenerator #pip install wordcloud

from TrieTree.DicTree import *
from flesch_index import *
import markov

class textBox(Text):
    '''
    The text box on the left.
    '''
    def __init__(self, *args, **kwargs):
        Text.__init__(self, *args, **kwargs)
        self.bind('<KeyRelease>', self.refresh)
        self.spelling_check=False
        self.tag_config('red', foreground='red')
        self.currentWord=''
        self.p=(0,0)
        self.currentPosition=0

    def getContent(self,content):
        '''
        Get the content in the text box and break the string into words using regular expression.
        Get the position of the word the user is editing in the text box.
        '''
        pattern = re.compile(r"[A-Za-z]+|\d+")     
        self.contentList = re.findall(pattern,content[:-1])
        self.position = []
        self.currentWord=''
        for m in pattern.finditer(content):
            self.position.append(m.span())
        if self.count("1.0", self.curosr):
            self.currentPosition=self.count("1.0", self.curosr)[0]
            for self.p in self.position:
                if self.p[0]<=self.currentPosition and self.p[1]>=self.currentPosition:
                    self.currentWord=content[self.p[0]:self.currentPosition]
                    break
    
    def refresh(self,event,selection=None):
        '''
        Clear the content in the text box, and show the processed content in the text box.
        '''
        self.content = self.get('1.0',END)
        self.curosr = self.index(INSERT)
        if selection:
            self.content=self.content[:self.p[0]]+selection+''+self.content[self.currentPosition:]
            self.curosr+='+'+str(len(selection)-len(self.currentWord))+'c'
        self.delete('1.0', END)
        self.insert('1.0', self.content[:-1])
        self.mark_set("insert", self.curosr)
        self.getContent(self.content)
        print('contentList: ',self.contentList[:15])
        print('position: ',self.position[:15])
        print('currentWord: ',self.currentWord)
        print('curosr: ',self.curosr)
        if self.spelling_check:
            self.check()
        self.wordsCount()
        suggestions.showSuggestions(self.currentWord)

    def check(self):
        '''
        Check if the current word is in the dictionary.
        '''
        for i in range(len(self.contentList)):
            if (not dic.isWord(self.contentList[i])) and ((not self.contentList[i].isnumeric()) and (self.contentList[i].isalpha())):
                self.tag_add('red', '1.0 + '+str(self.position[i][0])+' chars', '1.0 + '+str(self.position[i][1])+' chars')

    def wordsCount(self):
        '''
        Count the word in the text box.
        '''
        wordCount=len(self.contentList)
        if wordCount==0:
            count.set(str(wordCount))
        elif  wordCount==1:
            count.set(str(wordCount)+' word')
        else:
            count.set(str(wordCount)+' words')

class suggestionBox(Text):
    '''
    The suggestion box on the right.
    '''
    def __init__(self, *args, **kwargs):
        Text.__init__(self, *args, **kwargs)
        self.bind('<ButtonRelease-1>', self.select)

    def showSuggestions(self,currentWord):
        '''
        Lookf for the spelling suggestions in the dictionary and show them in the suggextion box.
        '''
        self.curosr = self.index(INSERT)
        self.delete('1.0', END)
        prediction = dic.prediction(currentWord, 100)
        self.insert('1.0', '\n'.join(prediction))
        self.mark_set("insert", self.curosr)

    def select(self,event):
        '''
        When click the word in the suggestion box, the word will be selected and sent to the text box.
        '''
        row=self.index(INSERT).split('.')[0]
        self.selection=self.get(row+'.0',row+'.end')
        print('selection: ',self.selection)
        textEntry.refresh(event,self.selection)

class translate(Button):
    '''
    The translation function.
    '''
    def __init__(self, *args, **kwargs):
        Button.__init__(self, *args, **kwargs)
        self.language = StringVar(root)
        self.language.set("Simplified Chinese") # default value
        self.language.trace("w", self.option_changed)
        self.target='zh'
        self['command']=self.translate_api
 
    def option_changed(self,*args):
        '''
        Choose the language from the option list.
        Send the option to the translation API.
        '''
        self.languageChoice=format(self.language.get())
        lan={'Simplified Chinese':'zh',
             'Traditional Chinese':'cht',
             'Spanish':'spa',
             'Arabic':'ara',
             'French':'fra',
             'Korean':'kor',
             'Thai':'th',
             'Greek':'el',
             'Japanese':'jp'}
        self.target=lan[self.languageChoice]

    def translate_api(self):
        '''
        The Baidu translate API.
        '''
        q = textEntry.get('1.0',END)
        q=q.replace('\n',' ').replace('\t',' ').replace('\r\n',' ')
        if len(q)==1:
            messagebox.showinfo("Translation", "Please provide some words.")
            return
        appid = '20170914000082688'
        secretKey = 'nMHccSZZQ1ZoeFOKOSlq'   
        httpClient = None
        myurl = '/api/trans/vip/translate?'
        fromLang = 'en'
        toLang = self.target
        salt = random.randint(32768, 65536)
        sign = appid+q+str(salt)+secretKey
        m1 = md5()
        m1.update(sign.encode(encoding='utf-8'))
        sign = m1.hexdigest()
        p = {'appid': appid,
             'q': q,
             'from': fromLang,
             'to': toLang,
             'salt': salt,
             'sign': sign
             }
        myurl = myurl+urllib.parse.urlencode(p)
        try:
            httpClient = httplib.HTTPConnection('api.fanyi.baidu.com')
            httpClient.request('GET', myurl)
            response = httpClient.getresponse()
            result = json.loads(response.read())['trans_result'][0]['dst']
            print ('Translation: ',result)
            messagebox.showinfo("Translation", result)
        except Exception as e:
            print (e)
        finally:
            if httpClient:
                httpClient.close()

def clear():
    '''
    Clear all the content in the text box.
    '''
    textEntry.delete('1.0', END)
    textEntry.refresh('<KeyRelease>')

def spellingCheck():
    '''
    The switch of spelling check function.
    '''
    textEntry.spelling_check = not textEntry.spelling_check
    textEntry.refresh('<KeyRelease>')

def fleschIndex():
    '''
    To calculate the Flesch Index and show the corresponding meaning of the index.
    '''
    content=textEntry.get('1.0',END)
    if count_words(content)<=100:
        messagebox.showinfo("Flesch Index", "We need more words.")
        return
    index=round(flesch_index(content),2)
    messages = {90 : 'This text is for 5th grade.\nIt is very easy to read, easily understood by an average 11-year-old student.',
                80 : 'This text is for 6th grade.\nIt is Easy to read, conversational English for consumers.',
                70 : 'This text is for 7th grade.\nIt is Fairly easy to read.',
                60 : 'This text is for 8th & 9th grade.\nIt is Plain English, easily understood by 13- to 15-year-old students.',
                50 : 'This text is for 10th to 12th grade.\nIt is fairly difficult to read.',
                40 : 'This text is for college.\nIt is difficult to read.',
                30 : 'This text is for college.\nIt is difficult to read.',
                20 : 'This text is for college graduate.\nIt is very difficult to read, best understood by university graduates.',
                10 : 'This text is for college graduate.\nIt is very difficult to read, best understood by university graduates.',
                0 : 'This text is for college graduate.\nIt is very difficult to read, best understood by university graduates.'}
    category = (index//10)*10
    if category in messages:
        message="The Flesch Index is {:.2f}.\n".format(index)+messages[category]
    else:
        message="This text is for kindergarden."
    messagebox.showinfo("Flesch Index", message)

def wordsCloud():
    '''
    Plot the word cloud.
    '''
    contentList=textEntry.contentList
    word_frequence={}
    for w in contentList:
        if not blacklist.isWord(w):
            if w not in word_frequence:
                word_frequence[w]=1
            else:
                word_frequence[w]+=1
    bimg=imread('cloud.png')
    wordcloud=WordCloud(background_color="white",mask=bimg,font_path='Avenir Next.ttc',max_font_size=200)
    wordcloud=wordcloud.fit_words(word_frequence)
    bimgColors=ImageColorGenerator(bimg)
    plt.axis("off")
    plt.imshow(wordcloud.recolor(color_func=bimgColors))
    plt.show()

def generateMarkovText():
    '''
    Generate the Markov Text.
    '''
    astring = textEntry.get('1.0',END)
    if count_words(astring)<=100:
        messagebox.showinfo("Generate Markov Text", "We need more words.")
        return
    m = markov.Markov(astring, 50)
    m.train()
    text = m.generate()
    messagebox.showinfo("Generate Markov Text", text)

def openFile():
    '''
    Open file from local.
    '''
    file = askopenfilename(initialdir=os.getcwd())
    try:
        return open(file,'r')
    except:
        messagebox.showinfo("Open File", "No file exists.")

def addDic(dic,f=open('words.txt','r')):
    '''
    Read the words in the file and add them into the dictionary.
    '''
    for line in f:
        dic.addWord(line.strip())
    f.close()

def addWords():
    '''
    Call the functions of openFile and addDic.
    '''
    f=openFile()
    if f:
        addDic(dic,f)
        textEntry.refresh('<KeyRelease>')

if __name__ == '__main__':
    # An instance of Trie storing dictionary.
    dic = DicTree()
    addDic(dic)
    # An instance of Trie storing the words that the word_Cloud function needs to filter.
    blacklist = DicTree()
    addDic(blacklist,open('connectives','r'))
    # The main interface
    root = Tk()
    root.title("JJBS")
    root.resizable(width=False, height=False)
    # The left hand text box and its scroll.
    textEntry = textBox(root, width=80, height=25, borderwidth=3, relief=RIDGE, highlightthickness=0, wrap=WORD)
    textEntry.grid(row=0, column=0, rowspan=6, columnspan=5)
    scrollb = Scrollbar(root, command=textEntry.yview)
    scrollb.grid(row=0, column=5, rowspan=6, sticky='nsew')
    textEntry['yscrollcommand'] = scrollb.set
    # Word counts.
    count = StringVar()
    Entry(root, width=15, textvariable=count).grid(row=6, column=0, sticky=W)
    # Translation
    Label(root, text="English-->").grid(row=6, column=1, sticky=E)  
    translation=translate(root, text='Translate')
    translation.grid(row=6, column=3, sticky=W)
    translateOption = OptionMenu(root,translation.language,'Simplified Chinese','Traditional Chinese','Arabic','Spanish','French','Korean','Thai','Greek','Japanese')
    translateOption.grid(row=6, column=2, sticky=W)
    # Clear the content in the text box.
    Button(root, text='Clear', command=clear).grid(row=6, column=4, sticky=E)    
    # The spelling suggestions box.
    Label(root, text="Spelling Suggestions:").grid(row=0, column=6, sticky=W)
    suggestions=suggestionBox(root, width=20, height=12, borderwidth=3, relief=RIDGE, highlightthickness=0)
    suggestions.grid(row=1, column=6)
    # Calculate the Flesch Index.
    Button(root, text='Flesch Index', command=fleschIndex).grid(row=2, column=6, sticky=W)
    # Markov text.
    Button(root, text='Generate Markov Text', command=generateMarkovText).grid(row=3, column=6, sticky=W)
    # Words Cloud.
    Button(root, text='Words Cloud', command=wordsCloud).grid(row=4, column=6, sticky=W)
    # Turn on/off the spelling check function.
    Checkbutton(root, text='Spelling Check', command=spellingCheck).grid(row=5, column=6, sticky=W)
    # Add customized dictionary.
    Button(root, text='Add Dictionary', command=addWords).grid(row=6, column=6, sticky=W)   
    while True: # There is a bug about drawing pictures inside tkinter, so I have to use this to make sure the program will not crash down.
        try:
            root.mainloop()
            break
        except UnicodeDecodeError:
            pass