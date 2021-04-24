//Ekin Celebi
//150160152
#ifndef UNTITLED14_PIZZA_H
#define UNTITLED14_PIZZA_H

#include <iostream>
#include <string>
using namespace std;

class IndegrientNode{


    friend class PizzaLinkedList; //LL can use node
    int index;
    string Indegrient;

    IndegrientNode *next;
public:
    IndegrientNode(string,int); //constructor
    ~IndegrientNode();
};

class PizzaLinkedList{


    IndegrientNode *head;
public:
    PizzaLinkedList();  //constructor
    void add(string,int);
    void print();
    void remove(int);
    ~PizzaLinkedList();
    void printInline();
};

class Pizza{
    //friend class Order;
    string name;
    string size; //size: “small”, “medium”, “big”
    string crust_type; // crust_type: “thick”, “normal”, “thin”
    PizzaLinkedList indegrients; //artik ne kadar icerik varsa




    public:

        Pizza();
        Pizza(string, string, int);
        Pizza(const Pizza& object_in);
        //Pizza& operator=(Pizza& object_in) {};
        string getSize();
        string getName();
        string getCrust();
        string getSizeConst() const{
            return size;
        };
        string getNameConst() const{
            return name;
        };
        string getCrustConst()const{
            return  crust_type;
        };

        void printIndegrients(){
            indegrients.print();
        }

        void printIndegrientsInline(){
            indegrients.printInline();
        }
        void setSize(string size){
          this->size = size;
        };
        void setCrust(string crust){
            this->crust_type = crust;
        };
        void setName(string name){
            this->name = name;
        };
        ~Pizza();




};

#endif //UNTITLED14_PIZZA_H
