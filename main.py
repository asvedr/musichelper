import music
import sys

help = [
	'--gammas        : list of available gammas',
	'--chords        : list of available chord kinds',
	'-g <note,kind>  : gamma for note and kind example: "-g A,minor"',
	'-c <chord>      : show notes in chord: "-c Am"',
	'-ci <chord>     : show schema for chord: "-ci maj7',
	'-tm <note,kind> : three main in',
	'-iw <notes,>    : in which gamma this notes' 
]

def parseArgs(args):
	acc = []
	singletonKeys = ['--gammas', '-h', '--chords', '--help']
	i = 1
	while i < len(args):
		key = args[i]
		if key in singletonKeys:
			return [(key,)]
		try:
			param = args[i+1]
		except:
			raise Exception(key, 'has no params')
		if key == '-g':
			params = param.split(',')
			try:
				note = params[0]
				kind = params[1]
			except:
				raise Exception('-g', 'bad args "%s"' % param)
			if not (note in music.Notes.notes):
				raise Exception('-g', 'bad note "%s"' % note)
			if music.Gammas.schemaFor(kind) is None:
				raise Exception('-g', 'bad gamma kind "%s"' % kind)
			acc.append( (key, note, kind) )
			i += 2
		elif key == '-c':
			acc.append( (key, param) )
			i += 2
		elif key == '-ci':
			acc.append( (key, param) )
			i += 2
		elif key == '-tm':
			params = param.split(',')
			if len(params) != 2:
				raise Exception('-tm', 'bad args "%s"' % param)
			if not (params[0] in music.Notes.notes):
				raise Exception('-tm', 'bad note "%s"' % params[0])
			if music.Gammas.schemaFor(params[1]) is None:
				raise Exception('-tm', 'bad kind "%s"' % params[1])
			acc.append( (key, params[0], params[1]) )
			i += 2
		elif key == '-iw':
			notes = param.split(',')
			for n in notes:
				if not (n in music.Notes.notes):
					raise Exception('-iw', 'bad note "%s"' % n)
			acc.append( (key, notes) )
			i += 2
		else:
			raise Exception('unknown cmd', key)
	return acc

def apply(cmd):
	if cmd[0] == '-h' or cmd[0] == '--help':
		for line in help:
			print(line)
	elif cmd[0] == '--gammas':
		for g in list(music.Gammas.schemas.keys()):
			print(g)
		for g in list(music.Gammas.aliases.keys()):
			print('%s ==> %s' % (g, music.Gammas.unalias(g)))
	elif cmd[0] == '--chords':
		pass
	elif cmd[0] == '-g':
		g = music.Gammas.gammaFor(cmd[1], music.Gammas.schemaFor(cmd[2]))
		print('gamma for %s %s' % (cmd[1], cmd[2]))
		print(g)
	elif cmd[0] == '-c':
		pass
	elif cmd[0] == '-ci':
		pass
	elif cmd[0] == '-tm':
		print(music.threeMainIn(cmd[1], cmd[2]))
	elif cmd[0] == '-iw':
		print('gamma vars for notes: %s' % cmd[1])
		ans = music.inWhichGamma(cmd[1])
		if len(ans) == 0:
			print('NOT FOUND')
		else:
			for gm in ans:
				print(gm)

def main():
	try:
		args = parseArgs(sys.argv)
	except Exception as e:
		print('INPUT ERROR')
		print('%s: %s' % (e.args[0], e.args[1]))
		return
	#print args
	for cmd in args:
		apply(cmd)

main()
