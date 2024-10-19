from assembler import assembler


file_name = 'Pong'

def binary(file):
	a = assembler(file)
	a.create_binary()
	return a.binary_program

binary_program = binary(f'{file_name}.asm')
# for l in binary_program:
# 	print(l)

def compare(binary_program, hack_file):
	file = open(hack_file, 'r')
	hack_bp = file.read().split('\n')
	if len(binary_program) != len(hack_bp):
		raise Exception('Different length')
	else:
		for i, (x,y) in enumerate(zip(binary_program,hack_bp)):
			if x!=y:
				print(i, x, y)

compare(binary_program, f'{file_name}.hack')

# a = assembler(f'{file_name}.asm')
# a.createSymbol()
# print(a.table)