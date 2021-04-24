
//Ekin Celebi
//150160152

#include "Pizza.h"
#include <iostream>
#include <string>

using namespace std;

IndegrientNode::IndegrientNode(string Indegrient,int index){
    this->Indegrient = Indegrient;
    this->index = index;
    next = NULL;
}

void PizzaLinkedList::print() {

    IndegrientNode *tmp=head;
    while (tmp != NULL){
        cout << tmp->index << ". "<<tmp->Indegrient << endl;
        tmp = tmp->next;
    }
    cout << endl;

}

void PizzaLinkedList::printInline() {

    IndegrientNode *tmp=head;
    cout << " ( ";
    while (tmp != NULL){
        cout <<tmp->Indegrient;
        if(tmp->next != NULL)
            cout << ", ";
        tmp = tmp->next;
    }
    cout << " )"<< endl;

}

PizzaLinkedList::~PizzaLinkedList() {

}

PizzaLinkedList::PizzaLinkedList(){
    head = NULL;
} //for each linked list head must be NULL

void PizzaLinkedList::remove (int position) {

        IndegrientNode *temp, *temp1;
        temp = head;

        if(position == head->index){
            head = head->next;
            free(temp);
            return;
        }

        while(temp->next->index != position && temp->next->index != 0){
            temp = temp->next;
        }
        temp1 = temp->next;
        temp->next = temp1->next;

        free(temp1);
        return;

    }

void PizzaLinkedList::add(string Indegrient,int index){
    if (head == NULL)
        head = new IndegrientNode(Indegrient,index);
    else{
        IndegrientNode *nptr = new IndegrientNode(Indegrient,index);
        nptr->next=head;
        head = nptr;
    }

}



Pizza::Pizza()
{
    // creates pizza with medium size, normal crust and mozarella as the ingredient
    indegrients.add("mozarella",1);
    crust_type = "normal";
    size = "medium";

}

Pizza::Pizza(string size, string crust_type, int pizza_type)
{
    this->size = size;
    this->crust_type = crust_type;

    switch (pizza_type)
    {
        case 1:
            name = "Chicken Pizza";
            indegrients.add("tomato",7);
            indegrients.add("onion",6);
            indegrients.add("olive",5);
            indegrients.add("corn",4);
            indegrients.add("mushroom",3);
            indegrients.add("chicken",2);
            indegrients.add("mozarella",1);
            break;
        case 2:
            name = "Broccoli Pizza";
            indegrients.add("onion",6);
            indegrients.add("corn",5);
            indegrients.add("olive",4);
            indegrients.add("pepperoni",3);
            indegrients.add("broccoli",2);
            indegrients.add("mozarella",1);
            break;
        case 3:
            name = "Sausage Pizza";
            indegrients.add("corn",6);
            indegrients.add("mushroom",5);
            indegrients.add("olive",4);
            indegrients.add("tomato",3);
            indegrients.add("sausage",2);
            indegrients.add("mozarella",1);
            break;

    }

}

Pizza::Pizza(const Pizza& object_in){
    //my copy constructor



     if(object_in.getNameConst() == "Chicken Pizza"){
         name = "Chicken Pizza";
         indegrients.add("tomato", 7);
         indegrients.add("onion", 6);
         indegrients.add("olive", 5);
         indegrients.add("corn", 4);
         indegrients.add("mushroom", 3);
         indegrients.add("chicken", 2);
         indegrients.add("mozarella", 1);
     }

     else if(object_in.getNameConst() == "Broccoli Pizza"){
         name = "Broccoli Pizza";
         indegrients.add("onion", 6);
         indegrients.add("corn", 5);
         indegrients.add("olive", 4);
         indegrients.add("pepperoni", 3);
         indegrients.add("broccoli", 2);
         indegrients.add("mozarella", 1);
     }


     else if(object_in.getNameConst() == "Sausage Pizza"){

         name = "Sausage Pizza";
         indegrients.add("corn", 6);
         indegrients.add("mushroom", 5);
         indegrients.add("olive", 4);
         indegrients.add("tomato", 3);
         indegrients.add("sausage", 2);
         indegrients.add("mozarella", 1);


    }

    cout << "Please enter the number of the indegrient you want to remove from your pizza." << endl;

    printIndegrients();

    cout << "Press 0 to save it." << endl;

    int toRemove;



    while(true){

        cin >> toRemove;

        if(toRemove == 0){
            

            break;
        }

        indegrients.remove(toRemove);

    }

    size = object_in.getSizeConst();
    crust_type = object_in.getCrustConst();




    


    }


string Pizza::getSize(){
    return size;
}

string Pizza::getName(){
    return name;
}

string Pizza::getCrust(){
    return crust_type;
}

Pizza::~Pizza() {
    //Destructor
}
