#include <stdlib.h>
#include <stdio.h>

int main() {
    pid_t pid;
    int i;

    for (i = 0; ; i++)  {
        pid = fork();

        if (pid > 0) {
            // parent process
            printf("Zombie #%d born:\n", i + 1);
            while (1==1) sleep(10);
        } else {
            // child process: drivel then exit
            printf("    *drool* Boooo! Arrgghh! *slobber*\n");
            exit(0);
        }
    }

    return 0;
}
