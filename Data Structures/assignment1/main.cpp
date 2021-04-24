/* @Author
Student Name: Ekib Celebi
Student ID: 150160152
Date: 22.10.2019 */

#include <iostream>
#include <iomanip>
#include <fstream>
using namespace std;

struct node
{
    int size;
    int quant;
	node *next; // pointer to another object of the same type
};

struct stock
{
	node *head;
	void create(); 
	void clear(); 
	void add_stock(int); 
	void sell(int);
    void show_stock();
};

typedef stock Datastructure; // declares Datastructure as type stock

void stock::create()
{
	head = NULL; // create empty list  
}

void stock::clear()
{	
/* Move forward from head, temp always point heas next, each time delete the head
*/
	node *temp;
	temp = head;
	while (head){
		head = head->next;
		delete temp;
		temp = head;
	
	}
}


void stock::add_stock(int num)
{	
	node *newnode = new node; //create  new node 

    newnode->size = num;
	newnode->quant = 1;
	newnode->next = NULL;

	if(head == NULL){
		head = newnode;
		return;
	}//if head is null head points to new node

	if(newnode->size == head->size){
		head->quant++;
		return;
	} //if number is equal to head increase head quantity

	if(newnode->size < head->size){
		newnode->next = head;
		head = newnode;
		return;
	} //if number is smaller than head size head becames the the node

	node *traverse,*tail;
	traverse = head;

	while(traverse->next && traverse->next->size < newnode->size){
		traverse = traverse->next;
	}

	if(traverse->next == NULL){
		traverse->next = newnode;
		return;
	}//add to last 
	
	tail = traverse->next;
	if(tail->size == newnode->size){
		tail->quant++;
		return;
	} //increase quantity of immediate node
	newnode->next = tail;
	traverse->next = newnode;
}

void stock::sell(int ordernum)
{   
	if(ordernum < head->size){
		cout << "NO_STOCK" << endl;
		return;
	}
	node *traverse,*tail;

	traverse = head;
	
	if(head->size == ordernum){
		
		if(head->quant == 1){
			head = head->next; //move head if 1 remaining pair of head is sold
			delete traverse;
		} 

		else if(head->quant > 1) head->quant--;

		return;
	} 

	//search for the size 
	while (traverse->next && traverse->next->size != ordernum) traverse = traverse -> next;

	//if no size untill the end print no stock
	if(traverse->next == NULL && traverse->size != ordernum) cout << "NO_STOCK" << endl;
	
	//if only one pair left delete the node
	else if(traverse->next->quant == 1){
		tail = traverse->next->next;
		delete traverse->next;
		traverse->next = tail;
	}
	//decrease quantity
	else if(traverse->next->quant > 1){
		traverse->next->quant--;
	} 


}

void stock::show_stock(){
    node *traverse;
    traverse = head;

    while (traverse -> next) {
            
		cout << traverse->size << ":" << traverse->quant << endl; 
		traverse = traverse->next;
	}
	cout << traverse->size << ":" << traverse->quant << endl; 

}


int main() {
    
    Datastructure my_stock;

    int x;
    ifstream inFile;
    
    inFile.open("input.txt");
    if (!inFile) {
        cout << "Unable to open file";
        exit(1); // terminate with error
    }
    
    my_stock.create();

    while (inFile >> x) {
        //stock operations
        
        if( x > 0 ) my_stock.add_stock(x); //sizes are positive numbers
        else if(x == 0) my_stock.show_stock(); //0 for show stock
        else if(x < 0) my_stock.sell(x*(-1)); //negative numbers are the shoes to be sold

    }
    
    inFile.close();
    my_stock.clear();
    return 0;
}
