from Packages.VBCh import ChangeViewBox

if __name__ == "__main__":
	option = ''
	while option != 'q':
		nvb = input('\033[34mPlease enter the desired svg viewbox (e.g. "0 0 16 16" (without quotes)):\033[0m ').replace('"', '').strip()
		option = input('Do you want do transform... \n0. A file? \033[32m(strongly recommended)\033[0m \n1. A number (not recommended, because it will work only if your svg\'s max_x == max_y (e.g. "16 16", NOT "16 32", in this case use the option 0.))\n\n\033[34mYour choice (0 or 1, q to quit):\033[0m ').strip().lower()
		if option == "0":
			op = ''
			while not op in ['0', '1']:
				op = input('Do you want to...\n0. Paste your svg text here \033[31m(one line)\033[0m\n1. Load it from your svg file \033[32m(recommended)\033[0m\n\n\033[34mYour choice (1 or 2):\033[0m ').strip()
				if op == '0': xml = input('\nPaste your svg here \033[31m(one line)\033[0m\n:\n\n')
				elif op == '1':
					with open(input('\033[33mThe path to the ".svg" file to be transformed:\033[0m '), "r") as f:
						xml = f.read()
				else: print('\n\n\033[31mPlease, select one of the options (1 or 2)!\033[0m\n')
			cvb = ChangeViewBox(xml, True)
			cvb.cvb(nvb)
			op = ''
			while not op in ['0', '1']:
				op = input('Do you want to...\n0. Display the result here\n1. Write it into a file\n\n\033[34mYour choice (1 or 2):\033[0m ').strip()
				if op == '0': print(str(cvb))
				elif op == '1':
					with open(input('\n\033[31mBe Careful! As the following action may overrite your file if it exists.\033[0m\n\033[34mThe name or path of the file where the transformed ".svg" will be written:\033[0m  '), 'w') as f: 
						f.write(str(cvb))
						print('\033[32mDone!\033[0m\n')
				else: print('\n\n\033[31mPlease, select one of the options (1 or 2)!\033[0m\n')
		elif option == "1":
			vb = input('\033[33mEnter the old viewbox\'s size (e.g. "0 0 16 16" -> "16"):\033[0m ').replace('"', '').strip()
			op = input('\033[33mEnter Infinite Mode? (you could still press q at any time to quit) [Y/N]:\033[0m ').strip().lower()
			tr = ChangeViewBox('', False)
			if op == 'y':
				nr = input('Your number (or q): ').lower().strip()
				while nr != 'q':
					print(tr.Transform(float(nr), float(vb), float(nvb.split()[3])))
					nr = input('Your number (or q): ').lower().strip()
			elif op == 'n': print(tr.Transform(float(input('Your number: ').strip()), float(vb), float(nvb.split()[3])))
			else: print("\nError: Entered wrong option.\n")
					
		elif option != 'q': print('\n\n\033[31mPlease, select one of the options (1 or 2)!\033[0m\n')
