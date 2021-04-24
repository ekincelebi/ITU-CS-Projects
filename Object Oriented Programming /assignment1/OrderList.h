//Ekin Celebi
//150160152
#ifndef UNTITLED14_ORDERLIST_H
#define UNTITLED14_ORDERLIST_H


#include "Order.h"

using namespace std;

class Node{
    friend class OrderList; //LL can use node
    Order comingOrder;
    Node *next;
public:
    Node();
    Node(Order &); //constructor
    ~Node();



};

class OrderList{
    int numberOfOrders;
    Node *head;

public:
    OrderList();

    void takeOrder();
    void listOrders();
    void deliverOrders();
    ~OrderList();
};

#endif //UNTITLED14_ORDERLIST_H
