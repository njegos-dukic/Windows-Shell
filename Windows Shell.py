import csv, os, msvcrt

def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print(turn_green('{}{}/'.format(indent, os.path.basename(root)).rstrip()))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f).rstrip())

def turn_blue(string): return ('\033[94m{}\033[00m'.format(string)) #94m - Blue

def turn_red(skk): return ('\033[91m{}\033[00m'.format(skk)) 

def turn_green(skk): return ('\033[92m{}\033[00m'.format(skk)) 

def set_home_directory():
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

def is_CSV_database_correct():
    with open('UsersDB.csv', 'r') as csv_file:
        reader = csv.DictReader(csv_file)

        if reader.fieldnames == ['Username', 'Password']:
            csv_file.close()  
            return True

    csv_file.close()  
    return False

def create_CSV():
    with open('UsersDB.csv', 'w') as csv_file:
        fieldnames = ['Username', 'Password']
        writer = csv.DictWriter(csv_file, fieldnames = fieldnames, lineterminator = '\n')
        writer.writeheader()
    csv_file.close()

def check_CSV_database():
    if not os.path.isfile('UsersDB.csv'):
        create_CSV()
        os.system('cls')
        print(turn_blue('UsersDB.csv ') + 'file created. \nPlease ' + turn_blue('register ') + 'account before trying to log in.\n')
        os.system('pause')

    else:
        if not is_CSV_database_correct():
            os.rename(r'UsersDB.csv', r'[OLD] UsersDB.csv')
            os.system('cls')
            create_CSV()
            print(turn_blue('UsersDB.csv ') + 'file is not properly formatted. \nIt\'s renamed to ' + turn_blue('[OLD] UsersDB.csv ') + 'and new empty file is created. \nPlease ' + turn_blue('register ') + 'before trying to log in.\n')
            os.system('pause')

def is_CSV_database_empty():
    with open('UsersDB.csv', 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        rows = list(reader)
        number_of_entries = len(rows)
    csv_file.close()    
    
    if number_of_entries == 0:
        return True
    
    return False
    

def win_getpass(prompt, stream=None):
    import sys

    for c in prompt:
        msvcrt.putwch(c)

    pw = ""
    while (True):
        c = msvcrt.getwch()
        if c == '\r' or c == '\n':
            break
        if c == '\003': # ALT
            raise KeyboardInterrupt
        if c == '\b': # Backspace
            if pw == '':
                pass
            else:
                pw = pw[:-1]
                msvcrt.putwch('\b')
                msvcrt.putwch(" ")
                msvcrt.putwch('\b')
        else:
            pw = pw + c
            msvcrt.putwch("*")

    msvcrt.putwch('\r')
    msvcrt.putwch('\n')
    return pw

def logged_out():
    logged_in = False
    check_CSV_database()
    is_empty = is_CSV_database_empty()
    os.system('cls')
    print('Logged in: False.')
    print('Commands: ' + turn_blue('login') + ', ' + turn_blue('register') + ', ' + turn_blue('list') + ', ' + turn_blue('clear') + ', ' + turn_blue('exit') + '.')
    print('Type ' +  turn_blue('help') + ' for more information.')

    if is_empty:
        print(turn_red('Users Database is empty. ') + 'Please register before trying to log in.')

    while(logged_in == False):
        command = input('\nEnter Command: ')
        command = ' '.join(command.split())
        command = command.strip().lower()
        arguments = command.split(' ', 2)
        arguments[0] = arguments[0].lower()
        check_CSV_database()
        is_empty = is_CSV_database_empty()

        if command:
            if command.split()[0] in ['where', 'go', 'create', 'print', 'find', 'finddat', 'logout']:
                print(turn_red('Please log in first.'))

            elif command == 'help':
                print('Type ' + turn_green('HELP COMMAND') + ' for more information on specific command.')
        
            elif arguments[0] == 'help' and len(arguments) == 2:
                if arguments[1].lower() == 'login':
                    print(turn_green('LOGIN') + ' - Log in to access privileged commands.')
                    continue
                if arguments[1].lower() == 'register':
                    print(turn_green('REGISTER') + ' - Create new account.')
                    continue
                if arguments[1].lower() == 'list':
                    print(turn_green('LIST') + ' - List existing accounts.')
                    continue
                if arguments[1].lower() == 'clear':
                    print(turn_green('CLEAR') + ' - Clear console.')
                    continue
                if arguments[1].lower() == 'exit':
                    print(turn_green('EXIT') + ' - Close application.')
                    continue

            elif command == 'login':
                if is_empty:
                    print(turn_red('No users in the database. ') + 'Please register account first.')
                    continue
                
                username = (input(turn_blue('\nUsername: '))).strip()
                password = win_getpass(turn_blue('Password: '))

                if not username or not password:
                    print(turn_red('\nUsername or password blank. ') + 'Please try again.')
                    continue
                    
                with open('UsersDB.csv', 'r') as csv_file:
                    reader = csv.DictReader(csv_file)
                    for row in reader: # row is OrderedDict
                        entered_user = row.get('Username') 
                        entered_password = row.get('Password')
                        if entered_user == username and entered_password == password: 
                            logged_in = True
                            print(turn_green('\nYou have successfully logged in.\n'))
                            os.system('pause')

                csv_file.close()
                        
                if logged_in == False:
                    print(turn_red('\nWrong username or password.'))

            elif command == 'register':
                username = (input(turn_blue('\nEnter username: '))).strip()
                password = win_getpass(turn_blue('Enter password: '))
                            
                if not username or not password:
                    print(turn_red('\nUsername or password blank. ') + 'Please try again.')
                    continue
                            
                elif username:
                    present = False
                    with open('UsersDB.csv', 'r') as csv_file:
                        reader = csv.DictReader(csv_file)
                        for row in reader: # row is OrderedDict
                            if username == row.get('Username'):
                                present = True
                                print(turn_red('\nSelected username is not available. ') + 'Please choose another.')
                                break

                    csv_file.close()
                                
                if not present:
                    with open('UsersDB.csv', 'a') as csv_file:
                        fieldnames = ['Username', 'Password']
                        writer = csv.DictWriter(csv_file, fieldnames = fieldnames, lineterminator = '\n')
                        writer.writerow({'Username' : username, 'Password' : password})

                    csv_file.close()

                    is_empty = False
                    print('\nAccount \'' + turn_green(username) + '\' successfully created.')

            elif command == 'list':
                
                if is_empty:
                    print(turn_green('No available accounts.'))
                else:
                    for c in 'Accounts: ':
                        msvcrt.putwch(c)
                    with open('UsersDB.csv', 'r') as csv_file:
                        reader = csv.DictReader(csv_file)
                        first = True
                        for row in reader: # row is OrderedDict
                            if first:
                                print(turn_blue(row.get('Username')))
                                first = False
                            else:
                                print(turn_blue('          ' + row.get('Username')))

                    csv_file.close()

            elif command == 'clear':
                os.system('cls')
                print('Logged in: False.')
                print('Commands: ' + turn_blue('login') + ', ' + turn_blue('register') + ', ' + turn_blue('list') + ', ' + turn_blue('clear') + ', ' + turn_blue('exit') + '.')
                print('Type ' + turn_blue('help') + ' for more information.')
                
                if is_empty:
                    print(turn_red('Users Database is empty. ') + 'Please register before trying to log in.')

            elif command == 'exit':
                print(turn_green('\nThank you for using our program.\n'))
                os.system('pause')
                return ""
 
            else:
                print(turn_red('Invalid command.'))
            
        else:
            print(turn_red('Please enter command.'))
    
    return username
    
def logged_in(username):
    os.system('cls')
    print('Logged in: True.')
    print('Commands: '  + turn_blue('where') + ', ' + turn_blue('go') + ', ' + turn_blue('create') + ', ' + turn_blue('list') + ', ' + turn_blue('print') + ', ' + turn_blue('find') + ', ' + turn_blue('findDat') + ', ' + turn_blue('clear') + ', ' + turn_blue('logout') + ', ' + turn_blue('exit') + '.')
    print('Type ' + turn_blue('help') + ' for more information.\n')
    while(True):
        command = input(turn_blue(username + ' >> '))
        original_command = command
        command = command.strip()
        command = ' '.join(command.split())
        arguments = command.split(' ', 2)
        arguments[0] = arguments[0].lower()

        if arguments[0] == 'logout' and len(arguments) == 1:
            print(turn_green('\nYou have succesfully logged out.\n'))
            os.system('pause')
            return True

        elif command.lower() == 'help':
            print('Type ' + turn_green('HELP COMMAND') + ' for more information on specific command.\n')
        
        elif arguments[0] == 'help' and len(arguments) == 2:
            if arguments[1].lower() == 'where':
                print(turn_green('WHERE') + ' - Show current working directory.\n')
                continue
            if arguments[1].lower() == 'go':
                print(turn_green('GO PATH') + ' - Change current working directory.\n')
                continue
            if arguments[1].lower() == 'create':
                print(turn_green('CREATE [-d] NAME') + ' - Create file or directory.\n')
                continue
            elif arguments[1].lower() == 'list':
                print(turn_green('LIST [PATH]') + ' - Display directory & file tree of current or specified directory.\n')
                continue
            if arguments[1].lower() == 'print':
                print(turn_green('PRINT FILE') + ' - Print .txt file content.\n')
                continue
            if arguments[1].lower() == 'find':
                print(turn_green('FIND "TEXT" FILE') + ' - Search file for specified text.\n')
                continue
            if arguments[1].lower() == 'finddat':
                print(turn_green('FINDDAT FILE [ROOT]') + ' - Search file tree for specified file.\n')
                continue
            if arguments[1].lower() == 'clear':
                print(turn_green('CLEAR') + ' - Clear console.\n')
                continue
            if arguments[1].lower() == 'logout':
                print(turn_green('LOGOUT') + ' - Log out.\n')
                continue
            if arguments[1].lower() == 'exit':
                print(turn_green('EXIT') + ' - Close application.\n')
                continue

        elif arguments[0] == 'exit' and len(arguments) == 1:
            print(turn_green('\nThank you for using our program.\n'))
            os.system('pause')
            return False

        elif arguments[0] == 'clear' and len(arguments) == 1:
            os.system('cls')
            print('Logged in: True.')
            print('Commands: '  + turn_blue('where') + ', ' + turn_blue('go') + ', ' + turn_blue('create') + ', ' + turn_blue('list') + ', ' + turn_blue('print') + ', ' + turn_blue('find') + ', ' + turn_blue('findDat') + ', ' + turn_blue('clear') + ', ' + turn_blue('logout') + ', ' + turn_blue('exit') + '.')
            print('Type ' + turn_blue('help') + ' for more information.\n')

        elif arguments[0] == 'where' and len(arguments) == 1:
                print(turn_green('Current location: ') + os.getcwd() + '\n')

        elif arguments[0] == 'go':
            if len(arguments) < 2:
                print(turn_red('Not enough arguments in command. ') + 'Please specify path.\n')
            else:
                arguments = command.split(' ', 1)
                if '\\' in arguments[1]: # Dat path za pomjeranje
                    new_path = arguments[1]
                else:
                    new_path = os.getcwd() + '\\' + arguments[1]
                    
                if os.path.isdir(new_path):
                    os.chdir(new_path)
                    print(turn_green('Current directory is now: ') + os.getcwd() + '\n')
                else:
                    print (turn_red('Path is not valid.\n'))

        elif arguments[0] == 'create':
            if len(arguments) < 2:
                print (turn_red('Not enough arguments in command. ') + 'Please specify name and/or flag.\n')
                continue

            else:
                old_path = os.getcwd() 

                if arguments[1] == '-d': 
                    if len(arguments) == 3: 
                        if '\\' in arguments[2]: 
                            arguments[2] = arguments[2].rstrip('\\') 
                            path = '\\'.join(arguments[2].split('\\')[0:-1]) 
                            if os.path.exists(path): 
                                os.chdir(path) 
                                directory_name = os.path.basename(arguments[2]) 
                                
                            else: 
                                print(turn_red('Path is not valid.\n'))
                                continue

                        else: 
                            directory_name = arguments[2]
                            
                        check = True 
                        path = os.getcwd() + '\\' + directory_name 

                        if os.path.exists(path):
                            print(turn_red('Folder with the same name already exists in this directory. ') + 'Please specify different name.\n')
                            check = False 

                        invalid_characters = ['\\', '/', ':', '*', '?', '\"', '<', '>', '|'] 
                        for char in invalid_characters: 
                            if char in directory_name: 
                                check = False
                                print(turn_red('Invalid character in directory name. ') + 'Please don\'t use \\, /, *, ?, \", <, > or |.\n')
                                break

                        if check: 
                            print('Created directory: \'' + turn_green(directory_name) + '\' in: ' + turn_green(os.getcwd()) + '.\n') 
                            os.mkdir(directory_name) 
                            os.chdir(old_path) 

                    else:
                        print(turn_red('Invalid command. ') + 'Please specify name of a directory that you want to create.\n') 
                        
                elif arguments[1]: 
                    arguments = command.split(' ', 1) 
                    if '\\' in arguments[1]: 
                        arguments[1] = arguments[1].rstrip('\\') 
                        path = '\\'.join(arguments[1].split('\\')[0:-1]) 
                        if os.path.exists(path): 
                            os.chdir(path) 
                            file_name = os.path.basename(arguments[1]) 
                            
                        else: 
                            print(turn_red('Path is not valid.\n'))
                            continue
                        
                    else: 
                        file_name = arguments[1]
                            
                    check = True 
                    path = os.getcwd() + '\\' + file_name 

                    if os.path.exists(path): 
                        print(turn_red('File with the same name already exists in this directory. ') + 'Please specify different name.\n')
                        check = False

                    invalid_characters = ['\\', '/', ':', '*', '?', '\"', '<', '>', '|']
                    for char in invalid_characters:  
                        if char in file_name: 
                            check = False
                            print(turn_red('Invalid character in file name. ') + 'Please don\'t use \\, /, *, ?, \", <, > or |.\n')
                            break

                    if check:
                        open(file_name, 'w+', newline = '') 
                        print('Created file: \'' + turn_green(file_name) + '\' in: ' +  turn_green(os.getcwd()) + '.\n') 
                        os.chdir(old_path) 

        elif arguments[0] == 'list':
            arguments = command.split(' ', 1)
            if command == 'list':
                list_files(os.getcwd())
                
            else:
                if os.path.isdir(arguments[1]):
                    list_files(arguments[1])

                else:
                    print(turn_red('Path is not valid.\n'))

            print('')
            
        elif arguments[0] == 'print':
            arguments = command.split(' ', 1)

            file_path = os.getcwd() + '\\' + os.path.basename(arguments[1])
            if os.path.isfile(file_path):
                if '.txt' not in os.path.basename(file_path)[-4:]:
                    print(turn_red('Please select text file for printing.\n'))
                
                else:
                    txt_file = open(file_path, 'r')
                    file_contents = txt_file.read()
                    print (turn_green(arguments[1] + ' content:\n') + file_contents.rstrip() + '\n')
                    txt_file.close()
                
            else:
                print(turn_red('File with that name does not exist in working directory.\n'))

        elif arguments[0] == 'find':
            lindex = -1
            rindex = -1

            for i in range(len(original_command)):
                if original_command[i] == '\"' and lindex == -1 : lindex = i
                if original_command[-i] == '\"' and rindex == -1 : rindex = i

            text = original_command[lindex+1:-rindex]

            if lindex == len(original_command) - rindex or original_command[-rindex + 1] != ' ' or text == '':
                print(turn_red('Invalid command. ') + 'Plese specify file and text for searching.\n')
                continue

            else:
                file_name = (original_command[-rindex + 1 : ]).strip()
                file_path = os.getcwd() + '\\' + file_name
                if os.path.isfile(file_path):
                    if '.txt' not in os.path.basename(file_path)[-4:]:
                        print(turn_red('Please select text file for searching.\n'))

                    else:
                        txt_file = open(file_path, 'r')
                        file_contents = txt_file.read().rstrip()
                        txt_file.close()
                            
                        text_found = False
                        file_contents_list = file_contents.split('\n')
                        for lines in file_contents_list:
                            if text in lines:
                                text_found = True
                                # print (lines)
                                line = file_contents_list.index(lines)
                                print ('Text \"' + turn_green(text) + '\" is found in file at line: ' + turn_green(str(line + 1)) + '.\n')
                                break

                        if text_found == False:
                            print ('Text \"' +  turn_green(text) + '\" is not found in the file.\n')
                                
                else:
                    print(turn_red('No file with that name in working directory.\n'))

        elif arguments[0] == 'finddat':
            if len(arguments) < 2:
                print (turn_red('Not enough arguments in command.\n'))
                continue

            elif '\\' not in command:
                arguments = command.split(' ', 1)
                lookup_file = arguments[1]
                lookup_root = os.getcwd() 

            else: 
                parts = command.split('\\', 1) 
                parts_spaced = parts[0].split(' ') 

                if len(parts_spaced) == 2: 
                    print(turn_red('Please enter the name of the file that you want to look for.\n'))
                    continue

                lookup_root = parts_spaced[-1] + '\\' + parts[1] 
                lookup_file = (command[8:-len(lookup_root)]).strip() 
            
            if not os.path.isdir(lookup_root):
                print(turn_red('Path is not valid.\n'))
                continue
            
            file_found = False
            for root, dirs, files in os.walk(lookup_root):
                if lookup_file in files or lookup_file in root:
                    found_path = root
                    file_found = True
                            
            if file_found == True:
                print ('File \'' + turn_green(lookup_file) + '\' is found in ' + turn_green(found_path) + '.\n')

            else:
                print ('File \'' + turn_green(lookup_file) + '\' is not found in the ' + turn_green(lookup_root) + ' directory tree.\n')
            
        else: 
            print(turn_red('Invalid command.\n'))

set_home_directory()
is_active = True
while (is_active):
    username = logged_out()
    if (username == ""):
        is_active = False
        continue
    is_active = logged_in(username)