import sys
import os.path


def get_file(dropped):
	if not os.path.exists(dropped):
		print("Arquivo inválido!")
		return None
	else:
		if os.path.isdir(dropped):
			print("Arquivo inválido!")
			return None
		else:
			filename = os.path.abspath(dropped)
			print(filename)
			filecontent = ""
			with open(filename, 'rt') as file:
				for line in file.readlines():
					filecontent += line
			return filecontent

def converter2excel(filecontent):
	pass

args = sys.argv
if len(args) >= 2:
	filecontent = get_file(args[1])
	if (filecontent):
		converter2excel(filecontent)
else:
	print("Arquivo não informado!")
