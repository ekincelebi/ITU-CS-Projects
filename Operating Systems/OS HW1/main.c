#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/wait.h>

int main(){

    int level = 1;
    //start from level = 1


    int child1 = fork();
    //first process is created (a parent and a child)

    if(child1 == 0){
        //if child of first process
        level++;

        int child11 = fork();
        //a new process from the child of first process

        if(child11 == 0){
            level++;

            int child111 = fork();

            if(child111 == 0){
                level++;
                printf("PID: %d, Children PID: %d, level: %d\n", getpid(),child111,level);

            }

            else{
                //child111 parent
                printf("PID: %d, Children PID: %d, level: %d\n", getpid(),child111,level);
            }



        }

        else if(child11 > 0){
            // child11 parent
            int child12 = fork();
            if(child12 == 0){
                level++;
                printf("PID: %d, Children PID: %d, level: %d\n", getpid(),child12,level);
            }

            else{
                //child12 parent
                printf("PID: %d, Children PID: %d, %d, level: %d\n", getpid(),child11,child12,level);

            }
        }



    }

    else{
        //level1 parent


        int child2 = fork();
        //create second child

        if(child2 == 0){
            //child2 child
            level++;
            int child21 = fork();

            if(child21 == 0){

                level++;

                int child211 = fork();

                if(child211 == 0){
                    level++;
                    printf("PID: %d, Children PID: %d, level: %d\n", getpid(),child211,level);
                }

                else{
                    //child211 parent
                    printf("PID: %d, Children PID: %d, level: %d\n", getpid(),child211,level);
                }



            }

            else if(child21 > 0){
                // child21 parent
                int child22 = fork();
                if(child22 == 0){
                    level++;
                    printf("PID: %d, Children PID: %d, level: %d\n", getpid(),child22,level);
                }

                else{
                    //child22 parent
                    printf("PID: %d, Children PID: %d, %d, level: %d\n", getpid(),child21,child22,level);

                }
            }
        }


        else{
            int child3 = fork();
            //created third child

            if(child3 == 0){
                level++;
                int child31 = fork();

                if(child31 == 0){
                    level++;

                    int child311 = fork();

                    if(child311 == 0){
                        level++;
                        printf("PID: %d, Children PID: %d, level: %d\n", getpid(),child311,level);
                    }

                    else{
                        printf("PID: %d, Children PID: %d, level: %d\n", getpid(),child311,level);
                    }



                }

                else if(child31 > 0){
                    int child32 = fork();

                    if(child32 == 0){
                        level++;
                        printf("PID: %d, Children PID: %d, level: %d\n", getpid(),child32,level);
                    }

                    else{
                        printf("PID: %d, Children PID: %d, %d, level: %d\n", getpid(),child31,child32,level);

                    }
                }
            }
            else{
                printf("PID: %d, Children PID: %d, %d, %d, level: %d\n", getpid(),child1,child2,child3,level);

            }

        }




    }






    return 0;



}