class Notes:
	notes = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','H']
	def __init__(self,notes=None):
		if notes != None:
			self.notes = notes
		self.len = len(self.notes)
	def __getitem__(self,index):
		return self.notes[index % self.len]
	def __len__(self):
		return self.len
	def __iter__(self):
		return self.notes.__iter__()
	def index(self,a):
		return self.notes.index(a)
	def __repr__(self):
		return self.__str__()
	def __str__(self):
		return str(self.notes)
	def __add__(gamma, arg):
		if type(arg) == int:
			acc = []
			for i in range(len(gamma)):
				acc.append(gamma[i + arg])
			return Notes(acc)
		raise Exception('Notes.__add__', 'arg not int')
	def __sub__(gamma, arg):
		return gamma.__add__(arg * (-1))

notes = Notes()
chords = {
	'maj': [0, 2, 3.5], # D A F#
	'm':   [0, 1.5, 3.5], # D A F
	'maj7':   [0, 2, 3.5, 5.5], # A E G C#
	'7':  [0, 2, 3.5, 5] # A E G C
}

major = [1, 1, 0.5, 1, 1, 1]#, 0.5]
minor = [1, 0.5, 1, 1, 0.5, 1]#, 1]

def gammaFor(tonica,inters):
	inters = [int(i * 2) for i in inters]
	ind = notes.index(tonica)
	result = [tonica]
	for i in inters:
		ind += i
		result.append(notes[ind])
	return Notes(result)

def checkParallel(g1,g2):
	for note in g1:
		if not (note in g2):
			return False
	return True

def chord(note,chord='maj'):
	ind = notes.index(note)
	schema = chords[chord]
	acc = []
	for i in schema:
		sh = int(i * 2)
		acc.append( notes[ind + sh] )
	return acc


class Gammas:
	def __init__(self):
		myGammas = [gammaFor(note,major) for note in notes]
		self.major = {}
		self.minor = {}
		self.parMajor = {}
		self.parMinor = {}
		for note in notes:
			minorG = gammaFor(note,minor)
			for majorG in myGammas:
				if checkParallel(minorG,majorG):
					self.parMajor[majorG[0]] = minorG
					self.parMinor[minorG[0]] = majorG
					self.major[majorG[0]] = majorG
					self.minor[minorG[0]] = minorG
	def parallelFor(self,note):
		try:
			assert(note[-1] == 'm')
			return self.parMinor[note[:-1]]
		except:
			return self.parMajor[note]
	def gammaFor(self,note):
		try:
			assert(note[-1] == 'm')
			return self.minor[note[:-1]]
		except:
			return self.major[note]
	def inWhichGamma(self,notes):
		acc = []
		for dominanta in self.major:
			gamma = self.major[dominanta]
			if all([(n in gamma) for n in notes]):
				majName = gamma[0]
				minName = self.parallelFor(majName)[0]
				acc.append(majName + " or " + minName + 'm')
		return acc

gammas = Gammas()
