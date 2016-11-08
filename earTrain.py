import pysynth as ps
import subprocess as sp
import os
import random as rand
import sys
import signal

TEMP_NAME = 'temp.wav'
PLAYER    = 'afplay'

def makeAndPlay(song):
	ps.make_wav(song, fn=TEMP_NAME)
	sp.check_output(['/bin/sh', '-c', '%s %s' % (PLAYER, TEMP_NAME)])
	#os.remove(TEMP_NAME)

# song = [['c',4],['d#',4],['d',4],['c',4],['f',4]]

notes = 'c c# d d# e f f# g g# a a# b'.split(' ')
seqToGet = list([n + '4' for n in notes])
allNotes = []
for i in range(3,6):
	for n in notes:
		allNotes.append(n + str(i))

def genCheckSeq(ints):
	tonica = 'c4'
	index  = allNotes.index(tonica)
	acc    = []
	for i in ints:
		acc.append( (tonica, 4) )
		acc.append( (allNotes[index + i], 4) )
	return acc

#makeAndPlay(list([[n,4] for n in notes]))

rand.seed()

def randIn(seq):
	return seq[rand.randrange(0, len(seq))]

def genMelody(length, allowIntervals):
	prima  = randIn(seqToGet)
	song   = [[prima, 4]]
	schema = []
	for _ in range(length):
		noteI = allNotes.index(prima)
		interval = randIn(allowIntervals)
		ways = []
		if noteI + interval < len(allNotes):
			ways.append(1)
		if noteI - interval >= 0:
			ways.append(-1)
		interval *= randIn(ways)
		schema.append(float(interval) / 2.0)
		prima = allNotes[noteI + interval]
		song.append([prima, 4])
	return (song,schema)

def parseIntervals(text):
	try:
		l = list([int(float(i) * 2) for i in text.split(',')])
		return l
	except:
		seq = text.split('..')
		a = int(float(seq[0]) * 2)
		b = int(float(seq[1]) * 2)
		return range(a, b+1)

class Stat:
	def __init__(self):
		self.line = []
		self.dSigGood  = {}
		self.dSigAll   = {}
		self.dAbsGood  = {}
		self.dAbsAll   = {}
		self.totalGood = 0
		self.total     = 0
	def showAll(self):
		def printPerc(mess, good, total):
			print('%s %s/%s (%s%%)' % (mess, good, total, (float(good) / total * 100.0)))
		def perc(i):
			try:
				v = float(self.dSigGood[i]) / self.dSigAll[i]
				return str(v * 100) + '%'
			except:
				return 'N/A'
		print()
		for i in self.dAbsAll.keys():
			try:
				good = self.dAbsGood[i]
			except:
				good = 0
			printPerc('INTERVAL %s' % i, good, self.dAbsAll[i])
			print('\t(+)%s (-)%s' % (perc(i), perc(-i)))
		printPerc('total', self.totalGood, self.total)
	def showLine(self):
		acc = ''
		for item in self.line:
			s = ('+' if item[0] > 0 else '') + str(item[0])
			v = 'Y' if item[1] else 'N'
			acc = '%s%s:%s ' % (acc, s, v)
		print(acc)
	def addLine(self):
		def add(d, v):
			if v in d:
				d[v] += 1
			else:
				d[v] = 1
		for item in self.line:
			i   = item[0]
			val = item[1]
			if val:
				add(self.dSigGood, i)
				add(self.dAbsGood, abs(i))
				self.totalGood += 1
			add(self.dSigAll, i)
			add(self.dAbsAll, abs(i))
			self.total += 1
		self.line = []
	def succ(self,i):
		self.line.append((i,True))
	def fail(self,i):
		self.line.append((i,False))

def main():
	length = int(sys.argv[1])
	intervals = parseIntervals(sys.argv[2])
	checkP = genCheckSeq(intervals)
	checkM = genCheckSeq([-n for n in intervals])
	stat = Stat()
	def exitFun(sig, frame):
		stat.showAll()
		sys.exit(0)
	signal.signal(signal.SIGINT, exitFun)
	while True:
		melody = genMelody(length, intervals)
		ans = 'r'
		while ans == 'r':
			makeAndPlay(melody[0])
			schema = melody[1]
			ans = input('variant: ').strip()
			if ans == 'c' or ans == '+c':
				ans = 'r'
				print(list([i / 2.0 for i in intervals]))
				makeAndPlay(checkP)
			elif ans == '-c':
				ans = 'r'
				print(list([-i / 2.0 for i in intervals]))
				makeAndPlay(checkM)
		var = list([float(n) for n in ans.split(' ')])
		for i in range(len(schema)):
			if i >= len(var):
				stat.fail(schema[i])
			else:
				if abs(schema[i] - var[i]) < 0.001:
					stat.succ(schema[i])
				else:
					stat.fail(schema[i])
		stat.showLine()
		stat.addLine()
		input()

main()
