//Ekin Celebi
//150160152
#ifndef UNTITLED14_ORDER_H
#define UNTITLED14_ORDER_H

#include "Pizza.h"
using namespace std;


class DrinkNode{
    friend class DrinkList; //LL can use node
    friend class Order;
    string drink;

    DrinkNode *next;
public:
    DrinkNode(string); //constructor
    ~DrinkNode();
    string getDrink(){
        return drink;
    }
    DrinkNode* getNext(){
        return next;
    }
};

class DrinkList{
    DrinkNode *head;
    friend class Order;
public:
    DrinkList();  //constructor
    void add(string);
    void print();
    ~DrinkList();



};

class Order{


    string customer;
    Pizza orderedPizza;
    DrinkList drink;


public:
    Order();
    Order(string customer,Pizza &orderedPizza,DrinkList &drinks);  //constructor
    Order(string customer,Pizza &orderedPizza);

    string getCustomer(){
        return customer;
    }

    void getPrice();
    void printOrder();
    ~Order();

};

#endif //UNTITLED14_ORDER_H
