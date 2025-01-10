import os 
import time

for i in range(0,1):
	print("Stealing data...")
	time.sleep(2)

class start:
	print("You are here:",os.getcwd())
	system = os.chdir("/")

	directory = os.listdir()
	print("Oh look what we have here ", ', '.join(directory))

	system2 = os.chdir("/home/wolfy/Documentos/python-stuff")
	with open("info.txt", "w") as file:
		file.write(str(directory))
		print("Ficheiro guardado com sucesso!")

	os.remove("info.txt")
	print("Apagado com sucesso!")

begin = start()