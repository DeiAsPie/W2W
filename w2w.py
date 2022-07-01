import sys
import operator

if (len(sys.argv)) == 1 or sys.argv[1] == "help":
    print("""Usage :-\n$ python3 w2w.py add 2 hello world    # Add a new item with priority 2 and text "hello world" to the list\n$ python3 w2w.py ls                   # Show incomplete priority list items sorted by priority in ascending order\n$ python3 w2w.py del INDEX            # Delete the incomplete item with the given index\n$ python3 w2w.py done INDEX           # Mark the incomplete item with the given index as complete\n$ python3 w2w.py help                 # Show usage\n$ python3 w2w.py report               # Statistics""")
    exit()

arg1 = sys.argv[1]
tasks_list = []
completed_list = []

tasks = open("task.txt", "a+")
completed = open("completed.txt", "a+")


def file_to_list(file_pointer_name):
    global tasks_list
    global completed_list

    if file_pointer_name == "tasks":
        tasks.seek(0)
        for line in tasks.readlines():
            temp = []
            temp.append(int(line.split(" ")[0]))
            temp.append(line.split(" ")[1::])
            tasks_list.append(temp)

    elif file_pointer_name == "completed":
        completed.seek(0)
        for line in completed.readlines():
            completed_list.append(line)


def list_printer(list_to_print):
    global tasks_list
    global completed_list

    if list_to_print == "tasks_list":
        for i in range(len(tasks_list)):
            print(
                f'{i+1}. {" ".join(tasks_list[i][1])[:-1]} [{tasks_list[i][0]}]')

    elif list_to_print == "completed_list":
        for i in range(len(completed_list)):
            print(f"{i+1}. {(completed_list[i])[:-1]}")


def list_to_file(list_to_write_in_file):
    global tasks_list
    global completed_list

    tasks.seek(0)
    completed.seek(0)

    if list_to_write_in_file == "tasks_list":
        for i in range(len(tasks_list)):
            tasks.write(f'{tasks_list[i][0]} {tasks_list[i][1]}\n')

    elif list_to_write_in_file == "completed.txt":
        completed.write(f'{tasks_list[task_number][1]}\n')


if arg1 == "report":
    file_to_list("tasks")
    print(f"Pending : {len(tasks_list)}\n")
    list_printer("tasks_list")
    file_to_list("completed")
    print(f"Completed : {len(completed_list)}")
    list_printer("completed_list")

elif arg1 == "ls":
    file_to_list("tasks")
    if len(tasks_list) == 0:
        print("There are no pending tasks! You may use add to add something")
    for i in range(len(tasks_list)):
        print(f'{i+1}. {" ".join(tasks_list[i][1])[:-1]} [{tasks_list[i][0]}]')

elif arg1 == "add":
    if len(sys.argv) == 2:
        print("Error: Missing tasks string. Nothing added!")
        exit()
    else:
        file_to_list("tasks")
        temp = []
        temp_list = []
        temp.append(sys.argv[2])
        temp.append(sys.argv[3])
        temp_list.append(temp)
        tasks_list = sorted(temp_list, key=operator.itemgetter(0))
        print(tasks_list)
        list_to_file("tasks_list")
        print(f'Added task: "{sys.argv[3]}" with priority {sys.argv[2]}')


elif arg1 == "done":
    task_number = int(sys.argv[2])
    file_to_list("tasks")
    file_to_list("completed")
    if len(sys.argv) == 2:
        print("Error: Missing NUMBER for marking tasks as done. Please add the argument for which task you want to mark as done")
        exit()
    for num in range(len(tasks_list)):
        if tasks_list[num][0] != int(sys.argv[2]):
            print(f"Error: no incomplete item with index #{num} exists.")
            exit()
    del tasks_list[task_number - 1]
    list_to_file("tasks_list")
    print("Marked item as done.")

elif arg1 == "del":
    file_to_list("tasks")
    task_number = int(sys.argv[2])
    for num in range(len(tasks_list)):
        if tasks_list[num][0] == (task_number - 1):
            del tasks_list[task_number - 1]
            list_to_file("tasks_list")
            print(f"Deleted task #{task_number}")
            exit()
    print(
        f"Error: task with index #{task_number} does not exist. Nothing deleted.")
    exit()


tasks.close()
completed.close()
