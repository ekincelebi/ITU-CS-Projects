//Ekin Celebi
//150160152

#include <iostream>
#include <string>
#include "OrderList.h"
#include "Pizza.h"
#include "Order.h"

using namespace std;



Node::Node(){
    next = NULL;
}

Node::~Node() {

}

Node::Node(Order &comingOrder) {
    this->comingOrder = comingOrder;
    next = NULL;
}

OrderList::OrderList() {
    numberOfOrders = 0;
    head = NULL;
}

void OrderList::takeOrder() {
    /*Print the pizza types. Take the first pizza order, create Pizza. Ask the customer
    the amount of the pizzas. If it is more than 1, then for each extra pizza create a
    copy of first pizza using copy constructor of Pizza class. Keep the pizzas in a
    suitable data structure (i.e. linked list).*/

    int pizzaType;
    string pizzaSize;
    string pizzaCrust;
    string customerName;

    int toDrink; //they will be link list soon for different drink orders

    //int pizzaAmount = 0;

    cout << "Pizza Menu" << endl;
    cout << "1. Chicken Pizza" << endl;
    cout << "2. Broccoli Pizza" << endl;
    cout << "3. Sausage Pizza" << endl;
    cout << "0. Back to main menu" << endl;
    //cin >> pizzaType;



    while(true) {
        cin >> pizzaType;
        if (pizzaType == 0 || pizzaType == 1 || pizzaType == 2 || pizzaType == 3)
            break;

        cout << "Invalid choice, choose again!" << endl;
    }


    if(pizzaType==0) return; //back to main menu



    cout << "Select size: small, medium, big" << endl;

    while(true) {
        cin >> pizzaSize;
        if (pizzaSize == "small" || pizzaSize == "medium" || pizzaSize == "big")
            break;

        cout << "Invalid choice, choose again!" << endl;
    }

    cout << "Select crust type: thin, normal, thick" << endl;
    while(true) {
        cin >> pizzaCrust;
        if (pizzaCrust == "thin" || pizzaCrust == "normal" || pizzaCrust == "thick")
            break;

        cout << "Invalid choice, choose again!" << endl;
    }

    //Pizza(string size, string crust_type, int pizza_type)
    Pizza newPizza(pizzaSize,pizzaCrust,pizzaType);


    

    Pizza copy_pizza = newPizza;




    



    DrinkList drinksPicked;

    cout << "What do you want to drink?" << endl;
    cout << "0.No drink" << endl;
    cout << "1.Cola" << endl;
    cout << "2.Soda" << endl;
    cout << "3.Ice tea" << endl;
    cout << "4.Fruit juice" << endl;
    cout << "Press -1 to save it." << endl;
    int selector;
    


    while(true){

        while(true) {
            cin >> selector;
            if (selector == 0 || selector == 1 || selector == 2 || selector == 3 || selector == 4 || selector == -1)
                break;

            cout << "Invalid choice, choose again!" << endl;
        }

        if(selector == -1 || selector == 0) break;
       


        else{
            if(selector == 1) drinksPicked.add("Cola");
            else if(selector == 2) drinksPicked.add("Soda");
            else if(selector == 3) drinksPicked.add("Ice tea");
            else if(selector == 4) drinksPicked.add("Fruit Juice");

        }


    }
    //cin >> toDrink;


    cout << "Please enter your name" << endl;
    cin >> customerName;

    numberOfOrders++;

    cout << "Your order is saved, it will be delivered when it is ready..." << endl;
//**************************************
//add order to a linklist process start
    if(selector == 0){
        Order newOrder(customerName,copy_pizza); //ifin icinde yaratildi cozumu var midir
        if (head == NULL) head = new Node(newOrder);
        else{
            Node *nptr = new Node(newOrder);
            nptr->next=head;
            head = nptr;
        }
    }
    else {
        Order newOrder(customerName, copy_pizza, drinksPicked);
        if (head == NULL) head = new Node(newOrder);
        else {
            Node *nptr = new Node(newOrder);
            nptr->next = head;
            head = nptr;
        }
    }

    //**************************************
//add order to a linklist process finish
return;
}

void OrderList::listOrders() {

    Node *tmp=head;
    while (tmp != NULL){
        cout << "-------------------------" << endl;
        tmp->comingOrder.printOrder();
        tmp = tmp->next;
    }
    cout << endl;
    cout << "-------------------------" << endl;
}

void OrderList::deliverOrders() {

    //list all of the orders
    listOrders();
    //user picks which order to be delivered by customer name
    cout << "Please write the customer name in order to deliver his/her order: ";
    string pickName;
    cin >> pickName;

    //the order list will be searched through the customer names
    // related order will be delivered


    Node *temp, *temp1;
    temp = head;

    if(pickName == head->comingOrder.getCustomer()){

        head->comingOrder.getPrice();
        cout << "Order will be delivered, order information" << endl;
        head->comingOrder.printOrder();
        head = head->next;
        free(temp);
        return;

    }

    else{
        while(temp->next->comingOrder.getCustomer() != pickName){
            temp = temp->next;
        }
        temp1 = temp->next;

        temp1->comingOrder.getPrice();


        cout << "Order will be delivered, order information" << endl;
        temp1->comingOrder.printOrder();
        temp->next = temp1->next;

        free(temp1);
        return;
    }


}

OrderList::~OrderList() {


}
