//Ekin Çelebi
//150160152
//30.04.2020

// Development environment: Lubuntu 16.04 or ITU SSH servers
// To compile: gcc oshw2.c -o hw2 -pthread
// To run: ./hw2 interval_min interval_max np nt
// Example: ./hw2 101 200 2 2

#include <sys/ipc.h>
#include <sys/shm.h>
#include <sys/sem.h>
#include <sys/types.h>

//  for handling signals
#include <signal.h>

//  for fork
#include <unistd.h>

//  other necessary headers
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include<pthread.h>


//struct for sending arguments to thread func
typedef struct start_finish_val{
    int startVal;
    int endVal;
    int processOrder;
    int threadOrder;
    
} RangeData;

pthread_mutex_t m_lock;
//pthread_cond_t cond;

int *globalcp;


void* Primes(void* arg)
{
    RangeData *arg_struct = (RangeData*) arg;
    
    int starter = arg_struct->startVal; //start value
    int finisher = arg_struct->endVal;
    int tOrder = arg_struct->threadOrder;
    int pOrder = arg_struct->processOrder;
    
    pthread_mutex_lock(&m_lock); //mutex lock
   
    printf("Thread %d.%d: searching in %d-%d\n",pOrder,tOrder,starter,finisher);
    //prime number finder
    for( int x = starter; x <= finisher; x ++){
        if( x == 2 )
            globalcp[2]=2;
            
        for( int y = 2; y < x; y++){
            if((x % y) == 0 ){
                break;
            }
            else if((y + 1) == x){
                globalcp[x]=x; //put found primes in shared memory
            }
        }
    }

    pthread_mutex_unlock(&m_lock); //mutex unlock
    //pthread_cond_signal(&cond);

    //terminating the thread
    pthread_exit(0);
}


/*  The ftok() function returns a key based on path and id
  that is usable in subsequent calls to semget() and
  shmget()
*/

int KEYSEM; //semaphore for processes
int KEYSEM2; //semaphore for threads
int KEYSHM; //shared memory


void initKeys(char* argv[])
{
    char cwd[256];
    char* keyString;
    
    //  get current working directory
    getcwd(cwd, 256);
    
    //  form keystring
    keyString = malloc(strlen(cwd) + strlen(argv[0]) + 1);
    strcpy(keyString, cwd);
    strcat(keyString, argv[0]);
    
    KEYSEM = ftok(keyString, 1);
    KEYSEM2 = ftok(keyString, 2);
    KEYSHM = ftok(keyString, 3);
    
    //  deallocate keystring
    free(keyString);
    
    //  if you use get_current_dir_name, result of that call must be deallocated by caller
    //because it creates its own buffer to store path.
    //but in this example we use getcwd and our own buffer.
}


//  increment operation
void sem_signal(int semid, int val)
{
    struct sembuf semaphore;
    semaphore.sem_num = 0;
    semaphore.sem_op = val;  //  relative:  add sem_op to value
    semaphore.sem_flg = 0;
    semop(semid, &semaphore, 1);
}


//  decrement operation
void sem_wait(int semid, int val)
{
    struct sembuf semaphore;
    semaphore.sem_num = 0;
    semaphore.sem_op = (-1*val);  //  relative:  add sem_op to value
    semaphore.sem_flg = 0;
    semop(semid, &semaphore, 1);
}


//  signal handling function
void mysignal(int signum)
{
    //printf("Received signal with num=%d\n", signum);
}


void mysigset(int num)
{
    struct sigaction mysigaction;
    mysigaction.sa_handler = (void*) mysignal;
    
    //  using the signal-catching function identified by sa_handler
    mysigaction.sa_flags = 0;

    //  sigaction() system call is used to change the action taken by
    //a process on receipt of a specific signal(specified with num);
    sigaction(num, &mysigaction, NULL);
}





int main(int argc, char *argv[])
{
    int interval_min, interval_max, np, nt;
    int myOrder = 0;  //  order of the running process
    
    //command line arguments initializations
    interval_min = atoi(argv[1]);
    interval_max = atoi(argv[2]);
    np = atoi(argv[3]); //number of processes
    nt = atoi(argv[4]); // number of threads
    
    int spread = interval_max+1;
    //later spread will be used to create shared memory
    //size of interval_max+1
     
    
    mysigset(12);  //  signal handler with num=12
    
    
    int shmid = 0;  //  shared memory id
    
    //  creating a shared memory area
    shmid = shmget(KEYSHM, spread*sizeof(int), 0700|IPC_CREAT);
    
    globalcp=(int *)shmat(shmid,0,0);
    
    for(int mem_i = 0; mem_i <= interval_max; mem_i++ ){
        globalcp[mem_i] = 0;
    }
    //assign zero for each space of shared memory
    
    
    //  initialize semaphore and shared memory keys
    initKeys(argv);
    
     
    int f=1;  //  return value of fork()
    int child[np];  //  child process ids
    int i;
    //  create child processes
    for (i = 0; i < np; ++i)
    {
        if (f > 0)
            f = fork();
        if (f == -1)
        {
            printf("fork error...\n");
            exit(1);
        }
        if (f == 0)
            break;
        else
            child[i] = f;  //  get pid of each child process
    }
    
    
    int termSem = 0, lock = 0;  //  semaphore ids
    if (f > 0)  //  parent process code
    {
        //  creating a semaphore for synchronization(value = 0)
        //between parent and its children
        termSem = semget(KEYSEM2, 1, 0700|IPC_CREAT); //semaphore name is termSem
        semctl(termSem, 0, SETVAL, 0);
        
        //  creating a semaphore for mutual exclusion(value=1)
        //between child processes
        lock = semget(KEYSEM, 1, 0700|IPC_CREAT); //semaphore name is lock
        semctl(lock, 0, SETVAL, 1);
        
        
        //  wait for 2 seconds
        sleep(2);
        
        //  sending the signal 12 to start child processes
        printf("Master: Started.\n");
        for (i = 0; i < np; ++i)
            kill(child[i], 12);
        //  decreasing semaphore (wait for all children)
        sem_wait(termSem, np);
        //wait for all children
        
        printf("Master: Done.");
        
       
        printf(" Prime numbers are: ");
        for(int loop = 0; loop <=interval_max; loop++){
            if(globalcp[loop]!=0)
                printf("%d, ", globalcp[loop]);
        }
        //each nonzero element in shared memory is prime number
        printf("\n");
        
        
        //  detaching the shared memory segment from the address
        //space of the calling process(parent)
        shmdt(globalcp);
        
        
        
        //  removing the created semaphores and shared memory
        semctl(termSem, 0, IPC_RMID, 0);
        semctl(lock, 0, IPC_RMID, 0);
        
        
        
        shmctl(shmid, IPC_RMID, 0);
        
        //  parent process is exiting
        exit(0);
    }
    
    
    else
    {
       
        
        
        //  wait until receiving a signal
        pause();
        
        
        
        //  to show which child process is running
        myOrder = i+1;
        
        printf("Slave %d: Started. ", myOrder);
        
        //  returning the semaphore ids for KEYSEM and KEYSEM2
        lock = semget(KEYSEM, 1, 0);
        termSem = semget(KEYSEM2, 1, 0);
        
    
        //  waiting for semaphore with id=lock to
            //enter critical section
        
        sem_wait(lock, 1);
            
         
        //find interval range for processes
        
        
        int mod = (( interval_max - interval_min )+1) % np;
        int pSpread = (( interval_max - interval_min )+1)/np;
        
        int pStart;
        int pEnd;
        
        if(mod != 0){
            if(myOrder <= mod){
                pStart = (interval_min+ (pSpread * (myOrder-1))) + myOrder-1;
                pEnd = pStart + pSpread;
            }
            else{
                pStart = (interval_min+ (pSpread * (myOrder-1))) + mod;
                pEnd = pStart + pSpread-1;
            }
        }
        
        else{
            pStart = interval_min+ (pSpread * (myOrder-1));
            pEnd = pStart + pSpread-1;
        }
        
        
        
        
        
        
        
        
        printf("Interval %d-%d\n",pStart, pEnd);
        
        
            
        RangeData args[nt];
        
        int modThread = ((pEnd-pStart)+1) % nt;
        
        //find interval range for threads
        int threadSpread;
        threadSpread = ((pEnd-pStart)+1) / nt; //thread range
        
                    
        //int newEnd = pStart + threadSpread - 1;
        

        args[0].startVal = pStart;
        args[0].endVal = pStart + threadSpread - 1;
        if(modThread != 0)
            args[0].endVal++;
        args[0].processOrder = myOrder;
        args[0].threadOrder = 1;
        

        for (int x = 1; x < nt; x++)
        {
            /*args[x].startVal = args[x-1].startVal+threadSpread;
            //args[x].endVal = args[x-1].endVal+threadSpread;
            if(x == nt-1)
                args[x].endVal = pEnd;
            else
                args[x].endVal = args[x].startVal +threadSpread-1;*/
            
            
            args[x].startVal = args[x-1].endVal + 1;
            
            if(modThread != 0){
                if(x < modThread){
                    args[x].endVal = args[x].startVal + threadSpread;
                }
                else{
                    args[x].endVal = args[x].startVal +threadSpread-1;
                }
            }
            
            else{
                args[x].endVal = args[x].startVal +threadSpread-1;
            }

            
            
            
            
            args[x].processOrder = myOrder;
            args[x].threadOrder = x+1;

        }
        
        
        //create threads
        pthread_t tids[nt];

        for (int i = 0; i < nt; i++) {

            pthread_attr_t attr;
            pthread_attr_init(&attr);
            
            pthread_create(&tids[i], &attr, Primes, (void *)(args+i));
                
        }

        //join threads
        for (int i = 0; i < nt; i++) {
            pthread_join(tids[i], NULL);
        }
        
        
            
        sem_signal(lock, 1);
        
        
            //  wait a second
        sleep(1);
            
        printf("Slave %d: Done.\n", myOrder);
        
        sleep(2);

        
        
        //  detaching the shared memory segment from the address
        //space of the calling process(child)
        shmdt(globalcp);
        
        //  increase semaphore by 1(synchorinization with parent)
        sem_signal(termSem, 1);
        
        
        
        //  child process is exiting
        exit(0);
    }
    
    return 0;
    }
