class Parser:
	def __init__(self, file):
		# opens the input file/stream and gets ready to parse it
		my_file = open(file, 'r')
		file_list = [(x.split('//')[0]).strip() for x in my_file.read().split('\n')]
		self.file_list = [x for x in file_list if x!=''] # comments and empty lines removed
		for line in self.file_list:
			if ' ' in line:
				raise Exception('Whitespace in code')

		self.line_counter = -1 # initially there is no current instruction
		self.file_length = len(self.file_list)
	
	def __repr__(self):
		return self.file_list
	
	def current_line(self):
		return self.file_list[self.line_counter]

	def hasMoreLines(self):
		return self.line_counter<self.file_length-1
	
	def advance(self):
		if self.hasMoreLines():
			self.line_counter += 1
		else:
			raise Exception('No more lines')
	
	def instructionType(self):
		line = self.current_line()
		if line[0]=='@':
			return 'A_INSTRUCTION'
		elif line[0]=='(':
			return 'L_INSTRUCTION'
		else:
			return 'C_INSTRUCTION'
	
	def symbol(self):
		line = self.current_line()
		instruction = self.instructionType()
		if instruction == 'A_INSTRUCTION':
			return line[1:]
		elif instruction == 'L_INSTRUCTION':
			return line[1:-1]
		else:
			raise Exception("Not A_INSTRUCTION or L_INSTRUCTION")
	
	def dest(self):
		instruction = self.instructionType()
		if instruction !='C_INSTRUCTION':
			raise Exception('Not C_INSTRUCTION')

		line = self.current_line()
		if '=' in line:
			return line.split('=')[0]
		else:
			return None
	
	def comp(self):
		instruction = self.instructionType()
		if instruction !='C_INSTRUCTION':
			raise Exception('Not C_INSTRUCTION')

		line = self.current_line()
		if '='in line:
			line = line.split('=')[1]
		if ';' in line:
			line = line.split(';')[0]
		if line == '':
			raise Exception('comp missing')
		return line 
	
	def jump(self):
		instruction = self.instructionType()
		if instruction !='C_INSTRUCTION':
			raise Exception('Not C_INSTRUCTION')

		line = self.current_line()
		if ';' in line:
			return line.split(';')[-1]
		else:
			return None



class Code:
	def dest(self, s):
		if s == None:
			return '000'
		d1, d2, d3 = 0,0,0
		if 'M' in s:
			d3=1
		if 'D' in s:
			d2=1
		if 'A' in s:
			d1=1
		return str(d1)+str(d2)+str(d3)


	def comp(self,s):
		a = 0
		if 'M' in s:
			a = 1
		s_temp=s.replace('A', 'X')
		s_temp=s_temp.replace('M', 'X')

		d = {'0':'101010', '1':'111111', '-1':'111010', 'D':'001100', 'X':'110000', '!D':'001101', '!X':'110001', '-D':'001111', '-X':'110011', 'D+1':'011111', 'X+1':'110111', 'D-1':'001110', 'X-1':'110010', 'D+X':'000010', 'D-X':'010011', 'X-D':'000111', 'D&X':'000000', 'D|X':'010101'}
		if s_temp not in d:
			print(f'comp={s_temp}')
			raise Exception('Comp is invalid:')
		return str(a)+d[s_temp]

	def jump(self,s):
		if s == None:
			return '000'
		d = {'JGT':'001', 'JEQ':'010', 'JGE':'011', 'JLT':'100', 'JNE':'101', 'JLE':'110', 'JMP':'111'}
		if s in d:
			return d[s]
		else:
			raise Exception('Invalid jump keyword')


class SymbolTable:
	def __init__(self):
		d = {'SP':0, 'LCL':1, 'ARG':2, 'THIS':3, 'THAT':4, 'SCREEN':16384, 'KBD':24576}
		for i in range(16):
			d['R'+str(i)] = i
		self.d = d
		self.special = set(['SP', 'LCL', 'ARG', 'THIS', 'THAT', 'SCREEN','KBD'] + ['R'+str(i) for i in range(16)])
	def __repr__(self):
		return str(self.d)
	def addEntry(self, symbol, address):
		self.d[symbol] = address
	def contains(self, symbol):
		return symbol in self.d
	def getAddress(self,symbol):
		if symbol in self.d:
			return self.d[symbol]
		raise Exception('symbol not in table')

def int_to_binary(n):
	binary = bin(n)[2:]
	return '0'*(16-len(binary)) + binary #pad to get 16-bit

class assembler:
	def __init__(self,file):
		self.parser = Parser(file)
		self.table = SymbolTable()
		self.binary_program = []

	def createSymbol(self):
		p = self.parser
		table = self.table
		p.line_counter = -1
		real_counter = -1 #counting lines of binary program (i.e. excluding L-instruction)
		A_variables = []
		L_variables = []
		while p.hasMoreLines():
			p.advance()
			real_counter += 1

			if p.instructionType() in ['A_INSTRUCTION']:
				sym = p.symbol()
				if sym not in A_variables and sym not in table.special and sym not in L_variables and sym[0] not in '1234567890': # check that symbol is not number
					A_variables.append(sym)
			if p.instructionType() in ['L_INSTRUCTION']:
				sym = p.symbol()			
				L_variables.append(sym)
				table.addEntry(sym,real_counter)
				real_counter -=1
				if sym in A_variables:
					A_variables.remove(sym)
		#print(A_variables)
		for i, sym in enumerate(A_variables):
			table.addEntry(sym, 16+i)
		

		p.line_counter = -1 # reset for second read

	def create_binary(self):
		self.createSymbol()
		p = self.parser
		table = self.table 
		bp = self.binary_program
		C_translate = Code()

		while p.hasMoreLines():
			p.advance()
			instruction = p.instructionType()

			if instruction == 'C_INSTRUCTION':
				d,c,j = p.dest(), p.comp(), p.jump()
				ds, cs, js = C_translate.dest(d), C_translate.comp(c), C_translate.jump(j)
				bp.append('111'+cs+ds+js)

			if instruction == 'L_INSTRUCTION':
				pass 

			if instruction == 'A_INSTRUCTION':
				sym = p.symbol()
				if sym[0] in '1234567890':
					binary = int_to_binary(int(sym))
				else:
					binary = int_to_binary(table.getAddress(sym))
				bp.append(binary)





