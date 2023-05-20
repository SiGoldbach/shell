import os


# This is a helper function made when formatting strings for the command c .. to go up a directory
def cd_go_up():
    v = os.getcwd()
    y = v.count("/")
    val = 0
    loop_counter = 0
    for i in v:
        loop_counter = loop_counter + 1
        if i == "/":
            val = val + 1
        if val == y:
            v = v[0:loop_counter - 1]
    return v


def shell():
    while 1:
        print()
        print(os.getcwd()+": ", end=" ")
        # Here we are reading a line and tokenizing it which is one line in python.
        x = input().split("|")
        #if len is two now it must be a piped command the strings are treated and piped_calls handles the input
        if len(x) == 2:
            y=(x[0].split(" "))
            y2=(x[1].split(" "))
            y=y[0:len(y)-1]
            y2=y2[1:len(y2)]
            piped_calls(y, y2)
            continue
        x=x[0].split(" ")
        # Here is an if statement where the exit system call is used if the user types exit, which stops the current process
        if x[0] == "exit":
            exit(0)
        # We need to implement our own cd since you cant call just call is with execvp
        # here two cases are implemented going up a directory or going to down. with cd .. and cd dir_name
        if x[0] == "cd":
            if len(x) == 1:
                print("Need argument")
                continue
            current_directory = os.getcwd()
            if x[1] == "..":
                current_directory = cd_go_up()
            else:
                current_directory = current_directory + "/" + x[1]

            print(current_directory)
            try:
                # Changing directory with command os.chdir
                os.chdir(current_directory)
            except OSError:
                print("Can not find directory")
            continue

        # Here the system call fork os used to create a child process this child process will then make a system call
        p = os.fork()
        if p > 0:
            os.wait()
        # The parent will wait for the child process
        else:
            # Here the child will make a system.
            try:
                if x[len(x) - 2] == ">":
                    reader = os.open(x[len(x) - 1], os.O_CREAT | os.O_TRUNC | os.O_WRONLY)
                    os.dup2(reader, 1)
                    x = x[0:len(x) - 2]
                os.execvp(x[0], x)
                print("This should never happen ")
            except FileNotFoundError:
                print("Could not understand that command")
                # Here I kill the process with exit since if the os.execvp cannot
                # find the correct file it will not get die, so we have to kill it
                exit(0)

# used for dealing with piped commands like this command1 | command 2. This shell can only handle two
# commands in one go
def piped_calls(x, y):
    read, write = os.pipe()
    print(read)
    print(write)

    p = os.fork()
    if p > 0:
        os.close(write)
        os.wait()

    else:
        #Here the first command is executed after the stdout is change to the write end of pipe
        os.dup2(write, 1)
        os.execvp(x[0], x)
    pf = os.fork()
    if pf > 0:
        os.wait()
    else:
        os.dup2(read, 0)
        print(y)
        #Here we are formatting the string to be used properly for execvp if the there needs to be output redirection
        if y[len(y) - 2] == ">":
            reader = os.open(y[len(y) - 1], os.O_CREAT | os.O_TRUNC | os.O_WRONLY)
            y = y[0:len(x) - 1]
            #Here we are copying a file descriptor to write to the file reader instead of to stdout now
            os.dup2(reader, 1)

        os.execvp(y[0], y)


def fork_test():
    print(os.getpid())
    p = os.fork()
    print(p)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    shell()
    # See PyCharm help at https://www.jetbrains.com/help/pycharm/
