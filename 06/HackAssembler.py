from assembler import assembler
import argparse

def binary(file):
	a = assembler(file)
	a.create_binary()
	return a.binary_program

# binary_program = binary('Add.asm')
# for l in binary_program:
# 	print(l)


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('file_name', type=str)

	args = parser.parse_args()

	binary_program = binary(args.file_name)
	
	with open("my_"+args.file_name[:-4]+'.hack', 'w') as file:
		for item in binary_program:
			file.write(item + "\n")


if __name__ == '__main__':
	main()