# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 11:55:37 2018

@author: dgwin
"""

# Again, this uses Python 3.x.
# Please upgrade if you haven't yet.
# There are many good features of Python 3
# that aren't in 2.
# Python 3 is technically slower, but if you
# want speed, why are you using Python?
# I tried to comment throughout. Output is at the bottom

load = lambda f: [line.replace('\n', '') for line in open(f)]
words = load('ospd.txt')
print('We have %d words!' % len(words))

# Question 1
# returns the alphabetized string of the letters in the word
letters = lambda string: ''.join(sorted(string))
# creates a set on the unique occurrences of letters
anagrams = set([letters(word) for word in words])
print('Question 1: Unique anagrams: %d' % len(anagrams))

# Question 2
# initialize a dictionary of the number of times each anagram occurs
counts = {key: 0 for key in anagrams}
# iterate through the words and increase the relevant key's frequency
for word in words:
	counts[letters(word)] = counts[letters(word)] + 1 if letters(word) in counts else 1
largest_anagram = max(counts, key=lambda x: counts[x])
print('Question 2: Largest anagram is "%s" with %d words' % (largest_anagram, counts[largest_anagram]))

# Question 3
from matplotlib import pyplot as plt
# generates a histogram on the frequency of the length of anagrams
plt.hist([len(key) for key in counts.keys()])
plt.show()

# Question 4
import sqlite3 as sql
connection = sql.connect('scrabble.db')
c = connection.cursor()
# create the database
c.execute('create table anagrams (id text, count integer, words text)')

# this solves the same problem as 2, but lets us see what the words are
data = {key: [] for key in anagrams}
for word in words: data[letters(word)] += [word]

# put the values in the database
c.executemany('insert into anagrams values (?, ?, ?)', [(k, len(v), ','.join(v),) for k, v in data.items()])

# Question 4 (continued)
print('Question 4: Unique anagrams: %d' % next(c.execute('select count(*) from anagrams'))[0])

# Question 5
result = next(c.execute('select id, max(count), words from anagrams'))
print('Question 5: Largest anagram by word count is "%s" with %d words' % (results[0], results[1]))

# Question 6
# runs the same stuff as Question 4
words = load('words.txt')
anagrams = set([letters(word) for word in words])
c.execute('create table words (id text, count integer, words text)')

data = {key: [] for key in anagrams}
for word in words: data[letters(word)] += [word]

c.executemany('insert into words values (?, ?, ?)', [(k, len(v), ','.join(v),) for k, v in data.items()])
print("Question 6: Unique anagrams (Webster's): %d" % next(c.execute('select count(*) from words'))[0])

# Question 7
result = next(c.execute('select id, max(count), words from words'))
print('Question 7: Largest anagram (Webster\'s) by word count is "%s" with %d words' % (result[0], result[1]))

c.close()
connection.close()

# # # # # # # # # #
# # # Results # # #
# # # # # # # # # #

'''
We have 79339 words!
Question 1: Unique anagrams: 65783
Question 2: Largest anagram is "aeprs" with 12 words

Question 4: Unique anagrams: 65783
Question 5: Largest anagram by word count is "aeprs" with 12 words

Question 6: Unique anagrams (Webster's): 315380
Question 7: Largest anagram (Webster's) by word count is "aelrst" with 15 words
'''
