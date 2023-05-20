#include <stdio.h>
#include <sys/types.h>  //
#include <unistd.h>    // uses for pid_t
#include <pthread.h>   // perror
#include <sys/wait.h>  // wait
#include <stdlib.h>    // exit
#include <string.h>
#define MAX_CHAR 100

/* this program takes a argument char argv[ ] and run an exec ()
 argc is the argument count
 argv is an array of character pointers to the arguments
*/

int main(int argc, char *argv[])
{
    char path[100] = "/bin/";
    strcat(path, argv[1]);

    printf("The terminal is running.\n");

    int fds[2]; //File decription array
    pipe(fds);  //Pipe from fds array

    // Make a fork to create a child and parent process
    int pid = fork();
    // Error handling, likely used up available pids
    if (pid < 0) {
        perror("Fork process failed. Unable to create child process");
        exit(1);
    }
    //child process created
    else if (pid == 0) {

        //no parameter
        if (argc == 1)
        {
            printf("Child process: (pid:%d).\n No parameters\n", (int) getpid());
        }    
        //one parameters
        if (argc == 2)
        {
            printf("Child process: (pid:%d).\n One parameter\n", (int) getpid());
            /*execlp uses as a system call to find ls command to run
             * argv[0] is name of a program that call ./.a.out
             * argv[1] is the first argument that execute exec()
            */
            printf( "parameter count:\n" );
            int i;
            for ( i = 1; i < argc; ++i ) {
                printf( "  %d. %s\n", i, argv[i] );
            }
           execlp(path, argv[1], NULL);
        }
        //two or more parameters
        if (argc  >= 3)
        {
            printf("Child process: (pid:%d).\n More than one parameters\n", (int) getpid());

            argv[argc++] = NULL;
                execvp(path, argv+1); // argv +1 to move to the next pointer in the array
        }
        close(fds[0]);               //No need to read the file in the child process
        dup2(fds[1], STDOUT_FILENO); //Associate stdout to the writeable end of pipe
        close(fds[1]);               //Finished writing
    }
        
    // parent process
    else {
        // parent will wait for the child process to finnish/reap zombies 
        int wc = wait(NULL);
        printf("Parent process are waiting for %d (wc:%d) (pid:%d) to complete \n", pid, wc, (int) getpid()); 
        printf("Child process completed. Parent process starts. \n");

        close(fds[1]);              //No need to write in the parent process
        dup2(fds[0], STDIN_FILENO); //Associate stdin to the
        close(fds[0]);              //Finished reading

        printf("Parent process completed.\n");
    }
}