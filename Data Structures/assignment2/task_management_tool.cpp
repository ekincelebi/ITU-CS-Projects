/*
PLEASE, DO NOT CHANGE void display(bool verbose, bool testing), int getUsableDay() and int getUsableTime() FUNCTIONS.
YOU HAVE TO WRITE THE REQUIRED  FUNCTIONS THAT IS MENTIONED ABOVE. YOU CAN ADD NEW FUNCTIONS IF YOU NEED.
*/

#include <iostream>
#include <stdlib.h>
#include <string.h>
#include <iomanip>

#include "task_management_tool.h"

using namespace std; 


void WorkPlan::display(bool verbose,bool testing)
{
	string inone="***";
	if (head!=NULL)
	{
		Task *pivot =new Task;
		Task *compeer =new Task;
			
		pivot=head;
		do
		{
			if(testing)
				inone+=" ";
			else
				cout << pivot->day <<". DAY"<< endl;
			compeer=pivot;
			while(compeer!=NULL)
			{
				string PREV= compeer->previous!=NULL?compeer->previous->name:"NULL";
				string NEXT=compeer->next!=NULL?compeer->next->name:"NULL";
				string CONT=compeer->counterpart!=NULL?compeer->counterpart->name:"NULL";
				if (testing)
					inone+=compeer->name;
				else
					if(verbose)
						cout<<"\t"<<setw(2)<< compeer->time <<":00\t"<< PREV<<"\t<- "<< compeer->name <<"("<< compeer->priority <<")->\t"<<NEXT <<"\t |_"<<CONT<<endl;
					else
						cout<<"\t"<<setw(2)<< compeer->time <<":00\t"<< compeer->name <<"("<< compeer->priority <<")"<<endl;				
				compeer=compeer->counterpart;
			}
			pivot=pivot->next;
		}while(pivot!=head);
		if(testing)
		{
			cout<<inone<<endl;
			cout<<"(checking cycled list:";
			if (checkCycledList())
				cout<<" PASS)"<<endl;
			else
				cout<<" FAIL)"<<endl;
		}
	}
	else
		cout<<"There is no task yet!"<<endl;
}

int WorkPlan::getUsableDay()
{
	return usable_day;
}

int WorkPlan::getUsableTime()
{
	return usable_time;
}


void WorkPlan::create()
{
    head = NULL;
}

void WorkPlan::close()
{//works
    Task *traverse, *trav_in,*tail;

    if(head == NULL)
        cout << "list ist already empty!!" << endl;



    else{
        tail = head->previous;

        while(tail != head){
            traverse= head->next;


            while(head->counterpart){
                trav_in = head->counterpart;
                delete head;
                head = trav_in;
            }
            delete head;
            head = traverse;
        }

        while(head->counterpart){
            trav_in = head->counterpart;
            delete head;
            head = trav_in;
        }

        delete head;
        head = NULL;
        

    }
}

void WorkPlan::add(Task *task)
{
    Task *newnode;
    Task *traverse;
    Task *behind;


    traverse = head;


    newnode = new Task; //allocate newtask

    newnode->name = task->name;
    newnode->day = task->day;
    newnode->time = task->time;
    newnode->priority = task->priority;
    newnode->previous = NULL;
    newnode->next = NULL;
    newnode->counterpart = NULL;
    //new task is filled now


    if (head == NULL){ //first node is being added
        head = newnode;
        head->next = head;
        head->previous = head;

        return;
    }
    if (newnode->day < head->day){ //add to head of list
        newnode->next = head;
        newnode->previous = head->previous;
        head = newnode;
        (head->next)->previous = head;
        (head->previous)->next = head;

        return;
    }

    while (newnode->day > traverse->day){
        //newnode's name comes after traverse's


        if(traverse->next == head)
            break;
        traverse = traverse->next;
    }

    if(traverse->day == newnode->day){
        //this day was added before;just add time
        if(newnode->time < traverse->time){
            //new task has earliest time of the day
            newnode->counterpart = traverse;
            if(traverse->next != traverse){
                newnode->next = traverse->next;
                newnode->previous = traverse->previous;
                (newnode->previous)->next = newnode;
                (newnode->next)->previous = newnode;
                if(traverse == head){
                    head=newnode;
                    return;
                }



            }

            else if(traverse->next == traverse){
                //then traverse is head
                newnode->next = newnode;
                newnode->previous = newnode;
                head = newnode;

            }

            traverse->previous = NULL;
            traverse->next = NULL;

            return;
        }

        while (traverse && (newnode->time > traverse->time)){
            //newnode's time comes after traverse's
            behind = traverse;
            traverse = traverse->counterpart;
        }

        if (traverse && newnode->time == traverse->time){
            //delay of one

            checkAvailableNextTimesFor(newnode);

            if(newnode->priority <= traverse->priority ){
                newnode->day = getUsableDay();
                newnode->time = getUsableTime();
                add(newnode);

                return;
            }

            else{
                remove(traverse);
                add(newnode);
                traverse->day = getUsableDay();
                traverse->time = getUsableTime();
                add(traverse);
                return;
            }

        }
        else{
            //insert time to middle
            if (traverse){ //inserting new name in between
                newnode->counterpart = traverse;
                behind->counterpart = newnode;
                return;
            }
            else {//insert to the end
                behind->counterpart = newnode;
                return;
            }


        }


    }

    else {
        if (traverse->next != head ){ //insert in between
            newnode->next = traverse;
            newnode->previous = traverse->previous;
            (traverse->previous)->next = newnode;
            traverse->previous = newnode;
            return;
        }
        else{
            if(newnode->day > traverse->day){
                (head->previous)->next = newnode;

                newnode->next = head;

                newnode->previous = head->previous;
                head->previous = newnode;
                return;
            }

            else if(newnode->day < traverse->day){
                newnode->next = traverse;
                newnode->previous = traverse->previous;
                (newnode->next)->previous = newnode;
                (newnode->previous)->next = newnode;
            }
        }

    }
}

Task * WorkPlan::getTask(int day, int time)
{
    // return adress of given date if not available return NULL

    Task *traverse;
    traverse = head;

    if(head == NULL){
        return NULL;
    }

    else if(head->next == head){
        //only one day of task
        if( day != head->day )
            return NULL;

        while(traverse && (traverse->time != time)){
            traverse = traverse->counterpart;

        }

        if(traverse == NULL)
            return NULL;

        return traverse;

    }

    while(traverse->day != day){
        traverse = traverse->next;

        if((traverse->next == head) && traverse->day != day )
            return NULL;

    }



    while(traverse && (traverse->time != time)){
        traverse = traverse->counterpart;

    }

    if(traverse == NULL)
        return NULL;


    return traverse;
}


void WorkPlan::checkAvailableNextTimesFor(Task *delayed){

    /*check sequentially for either the next hour of the given day or the earliest time for the following days*/
    Task *newTask;
    Task *traverse;
    int dDay = delayed->day;  //day and time of the delayed task
    int check_delay_time = 0;
    int dTime = delayed->time;
    if(getTask(dDay,dTime) == NULL){
        usable_day = dDay;
        usable_time = dTime;
        return;
    }

    traverse = getTask(dDay,dTime);


    while(traverse->counterpart){
        traverse = traverse->counterpart;
    }

    check_delay_time = traverse->time;
    //to check available time


    while(dDay){




        for(int i = dTime ; i <check_delay_time ; i++){

            newTask = getTask(dDay,i+1);
            if(newTask == NULL){
                usable_day = dDay;
                usable_time = i+1;
                return;
            }


        }



        dTime = 7;

        dDay++;


        traverse = getTask(dDay,8);




        if(traverse != NULL){
            while(traverse->counterpart){
                traverse = traverse->counterpart;
            }
            check_delay_time = traverse->time;

        }

        else
            check_delay_time = 8;
    }
}

void WorkPlan::remove(Task *target)
{

    Task *traverse;
    Task *tail;


    traverse = head;

    if(head == NULL){
        cout << "list is already empty!" << endl;
        return;
    }

    if(traverse->next == traverse){
        //delete one and only head column
        if(target->time == traverse->time){
            //it is the head at this point
            head = head->counterpart;
            if(head != NULL){
                head->next = head;
                head->previous = head;

            }
            delete traverse;
            return;
        }

        return;
    }

    while((traverse->next != traverse) && (traverse->day != target->day)){
        //tail = traverse;
        traverse = traverse->next;
    }//ttraversed untill target day



    while((traverse->time != target->time) && traverse->counterpart){
        tail = traverse;
        traverse = traverse->counterpart;
    }//traversed untill target time

    if((traverse == head) && target->time == head->time){
        if(head->counterpart == NULL){
            // head moves to next
            head = head->next;
            head->previous = traverse->previous;
            (head->previous)->next = head;
            delete traverse;
            return;
        }
        else{
            head = head->counterpart;
            head->previous = traverse->previous;
            head->next = traverse->next;
            (head->previous)->next = head;
            (head->next)->previous = head;
            delete traverse;
            return;

        }
    }

    else{
        if(traverse->next != NULL){
            //it is the first appointment of the day
            if(traverse->counterpart == NULL){
                //it is the only appointment
                (traverse->previous)->next = traverse->next;
                (traverse->next)->previous = traverse->previous;
                delete traverse;
                return;
            }
            (traverse->counterpart)->next = traverse->next;
            (traverse->counterpart)->previous = traverse->previous;
            (traverse->next)->previous = traverse->counterpart;
            (traverse->previous)->next = traverse->counterpart;
            delete traverse;
            return;
        }
        else{
            //intermediate node
            if(traverse->counterpart == NULL){
                //remove last appointment
                tail->counterpart = NULL;
                delete traverse;
                return;
            }
            else{
                tail->counterpart = traverse->counterpart;
                delete traverse;
                return;
            }
        }
    }



}


void WorkPlan::delayAllTasksOfDay(int day)
{   Task *traverse;
    Task *trav_counter;

    int day_next;
    day_next = day+1;
    //the day has to be valid

    if(head==NULL)
        return;

    traverse = head;
    while((traverse->next != traverse) && (traverse->day != day)){
        //traverse untill we come to the day
        traverse = traverse->next;
    }

    while(traverse){

        trav_counter = traverse->counterpart;
        remove(traverse);

        traverse->day = day_next;
        traverse->time = 8;
        checkAvailableNextTimesFor(traverse);

        traverse->time = getUsableTime();
        traverse->day = getUsableDay();
        add(traverse);
        traverse = trav_counter;


    }
}



bool WorkPlan::checkCycledList()
{				
	Task *pivot=new Task();
	pivot=head;
	int patient=100;
	bool r=false;
	while (pivot!=NULL&&patient>0)
	{		
		patient--;
		pivot=pivot->previous;
		if(pivot==head)
		{
			r=true;
			break;
		}
	}
	cout<<"("<<100-patient<<")";
	patient=100;
	bool l=false;
	while (pivot!=NULL&&patient>0)
	{		
		patient--;
		pivot=pivot->next;
		if(pivot==head)
		{
			l=true;
			break;
		}
	}
	return r&l;
}
