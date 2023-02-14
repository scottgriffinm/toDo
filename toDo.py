from random import shuffle
import sys
import time

#GLOBAL VARIABLES
FILE = 'data.txt'

creditMessage = '''
            .-'-'-.                    .-'-'-.                                                 
           '   _    \ _______         '   _    \                                    .-''-.     
         /   /` '.   \\  ___ `'.    /   /` '.   \           .----.     .----.     .' .-.  )    
        .   |     \  ' ' |--.\  \  .   |     \  '            \    \   /    /     / .'  / /     
     .| |   '      |  '| |    \  ' |   '      |  '            '   '. /'   /     (_/   / /      
   .' |_\    \     / / | |     |  '\    \     / /             |    |'    /           / /       
 .'     |`.   ` ..' /  | |     |  | `.   ` ..' /              |    ||    |          / /        
'--.  .-'   '-...-'`   | |     ' .'    '-...-'`               '.   `'   .'         . '         
   |  |                | |___.' /'                             \        /,.--.    / /    _.-') 
   |  |               /_______.'/                               \      ///    \ .' '  _.'.-''  
   |  '.'             \_______|/                                 '----' \\    //  /.-'_.'      
   |   /                                                                 `'--'/    _.'         
   `'-'                                                                      ( _.-'            
   Scott Griffin
   scottgriffinm@gmail.com
   ascii art from https://patorjk.com/
   started on 12/1/22
   '''

writeTasksMessage = '''
Hi, what do you want to do today?

'd' - delete last
'done' - done adding tasks

'''

existSessionMessage = '''
There's an existing session:

<session_data>
Do you want to continue this session? (y/n)
'''

def skipTasks(tasks:list):
    if len(tasks)==1:
        return tasks
    else:
        toSkip = tasks[0]
        tasks = tasks[1:]
        tasks.append(toSkip)
        return tasks

def clearScreen():
    '''Print enough newlines to clear screen.'''
    noNewLines = 100
    print("\n"*noNewLines)

def endMessage():
    '''Ending message.'''
    print('''Lets go, you're done!''')
    time.sleep(3)

def saveTasks(tasks:list, file:str):
    '''Saves tasks to file.
    tasks (list) - a list of tasks
    file (str) - file compatible with python's open() function.
    '''
    f = open(file,"w")
    toWrite = ""
    for task in tasks:
        toWrite = toWrite + task + "\n"
    f.write(toWrite)
    f.close

def printTasks(tasks: list, selected:int = -1) -> str:
    '''Returns a numbered list of tasks as a string.
    tasks (list) - a list of tasks.
    selected (int) - index of tasks to add an selection arrow to. -1 means no arrow.
    '''
    totalStr = "----------Tasks----------\n"
    for iii in range(0,len(tasks)):
        partStr = f"{iii+1}: {tasks[iii]}"
        if iii == selected:
            partStr = partStr + " <--"
        totalStr = totalStr + partStr + "\n"
    return totalStr   

def writeTasks(tasks=[]) -> list:
    '''Prompts user to add or delete tasks from their task list, then randomizes that task list.
    tasks (list) - empty by default; pass a list of tasks to edit it.
    '''
    # write tasks
    while True:
        clearScreen()
        print(writeTasksMessage + printTasks(tasks))
        in_put = str(input("Enter here: ")).strip()
        if in_put == 'd':
            if len(tasks) == 0:
                print('Error: there are no tasks to delete!')
            else:
                tasks.pop()
        elif in_put == 'done':
            if len(tasks) == 0:
                print('Error: please enter at least one task.')
            else:
                break
        else:
            tasks.append(in_put)

    # randomize schedule
    while True:
        clearScreen()
        shuffle(tasks)
        print("Here's your schedule.")
        print(printTasks(tasks))
        print("Would you like to randomize it? (y/n)")
        while True:
            in_put = input('Enter here: ')
            if in_put not in ('','y','n'):
                print("Error: unexpected input")
                continue
            else:
                if in_put in('y', ''):
                    break
                elif in_put == 'n':
                    return tasks
                    
def session(tasks: list, file: str):
    '''To-do session loop.
    tasks (list) - a list of tasks.
    file (str) - file compatible with python's open() function.
    '''
    while len(tasks) != 0:
        clearScreen()
        saveTasks(tasks,file)

        print(printTasks(tasks,selected=0))
        print(f'''Your current task is {tasks[0]}.\n
'done' - complete tasks
'r' - randomize tasks
'edit' - edit tasks
'skip' - skip current task
''')
        while True: #we could store a variable for each command so we have central location to change commands
            in_put = str(input("Enter here: ")).strip()
            #TODO: implement remove command using regex

            if in_put not in ('done','r','edit', 'skip'):
                print("Error: unexpected input")
                continue
            elif in_put == 'edit':
                tasks = writeTasks(tasks=tasks)
                break
            elif in_put == 'r':
                shuffle(tasks)
                break
            elif in_put == 'done':
                tasks = tasks[1:]
                break
            elif in_put == 'skip':
                print(tasks)
                tasks = skipTasks(tasks)
                print(tasks)
                break

    #all tasks completed
    saveTasks([],file) #clear data file
    clearScreen()
    endMessage()
    sys.exit()

if __name__ == "__main__":

    print(creditMessage)
    time.sleep(3)

    #checking for data
    with open(FILE) as f:
        tasks = f.readlines()
    f.close()

    # remove newlines from tasks
    for iii in range(0, len(tasks)):
        tasks[iii] = tasks[iii].replace("\n","")

    #existing session
    if len(tasks) != 0:
        # check if user wants to continue session
        printTaskString = printTasks(tasks)
        print(existSessionMessage.replace('<session_data>',printTaskString))
        while True:
            in_put = input('Enter here: ')
            if in_put not in ('','y','n'):
                print("Error: unexpected input")
                continue
            else:
                if in_put in('y', ''):
                    session(tasks,FILE)
                elif in_put =='n':
                    break

    #new Session
    tasks = writeTasks()
    session(tasks,FILE)







