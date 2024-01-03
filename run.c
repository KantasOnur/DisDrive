#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>

char* server[] = {"sh", "-c", "cd flask-backend && python3 server.py", NULL};
char* bot[] = {"sh", "-c", "cd flask-backend && python3 DisDrive.py", NULL};
char* front_end[] = {"sh", "-c", "cd client && npm start", NULL};

char** programs[] = {server, bot, front_end};
char* program_names[] = {"server", "bot", "front end"};

void runProgram(char** program, char* program_name){

    pid_t pid = fork();
    if(pid == 0){
        printf("Running %s\n", program_name);
        if(execvp(program[0], program) == -1){
            printf("Error: program %s failed to execute.\n", program_name);
            exit(-1);
        }
        exit(0);
    }

}

int main(){

    for(int i = 0; i < 3; i++){
        runProgram(programs[i], program_names[i]);
    }
    while(1){
    }
    exit(0);
}
