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
	'major': [0, 2, 3.5], # D A F#
	'm':     [0, 1.5, 3.5], # D A F
	'maj7':  [0, 2, 3.5, 5.5], # A E G C#
	'7':     [0, 2, 3.5, 5] # A E G C
}

# check two gammas to parallel
def checkParallel(g1,g2):
	for note in g1:
		if not (note in g2):
			return False
	return True

def chord(note,chord='major'):
	ind = notes.index(note)
	schema = chords[chord]
	acc = []
	for i in schema:
		sh = int(i * 2)
		acc.append( notes[ind + sh] )
	return acc

class Gammas:
	schemas = {	
		'naturalMajor'  : [1.0, 1.0, 0.5, 1.0, 1.0, 1.0, 0.5],
		'naturalMinor'  : [1.0, 0.5, 1.0, 1.0, 0.5, 1.0, 1.0],
		'harmonicMinor' : [1.0, 0.5, 1.0, 1.0, 0.5, 1.5, 0.5]
	}
	aliases = {
		'M'  : 'naturalMajor',
		'm'  : 'naturalMinor',
		'hm' : 'harmonicMinor'
	}
	@classmethod
	def unalias(cls, name):
		try:
			return cls.aliases[name]
		except:
			if name in cls.schemas:
				return name
			else:
				return None
	@classmethod
	def schemaFor(cls, name):
		if name in cls.aliases.keys():
			return cls.schemas[cls.aliases[name]]
		elif name in cls.schemas.keys():
			return cls.schemas[name]
		else:
			return None
	@classmethod
	def gammaFor(cls, tonica, schema):
		inters = [int(i * 2) for i in schema]
		ind = notes.index(tonica)
		result = [tonica]
		for i in inters:
			ind += i
			result.append(notes[ind])
		return Notes(result)
		

def inWhichGamma(notes):
	acc = []
	for tonica in Notes():
		for schema in Gammas.schemas:
			gamma = Gammas.gammaFor(tonica, schema)
			allIn = True
			for note in notes:
				allIn = allIn and (note in gamma)
			if allIn:
				acc.append( (tonica, schema) )
	return acc


def threeMainIn(tonica,kind): # sample threeMainIn(A, minor) => Am, Dm, E
	g = Gammas.gammaFor(tonica, Gammas.schemaFor('m'))
	A = g[0]
	D = g[3]
	E = g[4]
	kind = Gammas.unalias(kind)
	if kind == 'naturalMajor':
		return [A, D, E]
	elif kind == 'naturalMinor':
		return [A + 'm', D + 'm', E]
	else:
		raise Exception('threeMain', 'work only with nat major and nat minor')
