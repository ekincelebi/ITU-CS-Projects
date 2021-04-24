//Ekin Celebi
//150160152

#include <iostream>
#include <string>
#include "Order.h"
using namespace std;

void DrinkList::print(){
    if(head == NULL)
        cout << "No drink";
    DrinkNode *tmp=head;
    while (tmp != NULL){
        cout << " "<< tmp->getDrink() ;
        if(tmp->next != NULL)
            cout << ",";
        tmp = tmp->next;
    }
    cout << endl;

}

DrinkList::DrinkList(){
    head = NULL;
} //for each linked list head must be NULL

DrinkList::~DrinkList() {

}

void DrinkList::add(string drink){
    if (head == NULL)
        head = new DrinkNode(drink);
    else{
        DrinkNode *nptr = new DrinkNode(drink);
        nptr->next=head;
        head = nptr;
    }

}


DrinkNode::DrinkNode(string drink){
    this->drink = drink;
    next = NULL;
}
DrinkNode::~DrinkNode() {}



void Order::getPrice() {
    float priceDrink = 0;
    int pricePizza;


    if(orderedPizza.getSize() == "small") pricePizza = 15;
    else if(orderedPizza.getSize() == "medium") pricePizza = 20;
    else if(orderedPizza.getSize() == "big") pricePizza = 25;


    DrinkNode *tmp= drink.head;
    while (tmp != NULL){
        if(tmp->drink == "Cola") priceDrink += 4;
        else if(tmp->drink == "Soda") priceDrink += 2;
        else if(tmp->drink == "Ice tea") priceDrink += 3;
        else if(tmp->drink == "Fruit juice") priceDrink += 3.5;
        tmp = tmp->next;
    }
    cout << endl;

    float price = static_cast<float>(pricePizza) + priceDrink;

    cout << "price: " << price << endl;
    cout << "Do you have promotion code? (yes/no)" << endl;
    string yesOrNo;
    cin >> yesOrNo;
    if(yesOrNo == "yes"){
        string promo;
        cout << "enter your promo code" << endl;
        
        cin.ignore();
        getline(cin,promo);
        if( promo == "I am a student"){
            cout << "promotion code is valid, you get %10 discount" << endl;
            price = (price*9)/10;
            cout << "price: " <<  price << endl;
            return;

        }

        else{
            cout << "promotion code not valid" << endl;
            cout << "price: " << price << endl;
            return;

        }
    }
    else{
        cout << "no promotion code entered" << endl;
        cout << "price: " << price << endl;
        return;

    }



}

Order::Order(string customer,Pizza &orderedPizza,DrinkList &drinks) {

    this->customer = customer;
    this->orderedPizza = orderedPizza;


    this->drink = drinks;


}

Order::Order(string customer,Pizza &orderedPizza){
    this->customer = customer;
    this->orderedPizza = orderedPizza;

}

Order::Order(){

}

Order::~Order() {}

void Order::printOrder() {
    //this function prints the order as customer name, ordered pizzas and
    //drinks.
    cout << "Name: " << customer << endl;
    cout << orderedPizza.getName();
    orderedPizza.printIndegrientsInline();

    cout << "Size: " << orderedPizza.getSize() << endl;
    cout << "Crust: " << orderedPizza.getCrust() << endl;
    cout << "Drinks: ";
    this->drink.print();
}
