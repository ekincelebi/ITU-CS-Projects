//Ekin Celebi
//150160152
#include <iostream>
#include "OrderList.h"

using namespace std;

int main(){


    bool exitFlag = true;

    OrderList newList; //a new Link list for orders is created
    while(exitFlag){
        cout << "Welcome to Unicorn Pizza!" << endl;
        int chooseItem;
        cout << "1. Add an order" << endl;
        cout << "2. List orders" << endl;
        cout << "3. Deliver order" << endl;
        cout << "4. Exit" << endl;

        cout << "Choose what to do: ";
        cin >> chooseItem;

        if(chooseItem == 1){
            newList.takeOrder(); //adds an order to the already created newList LinkList

        }

        else if(chooseItem == 2){
            newList.listOrders();
        }

        else if(chooseItem == 3){
            newList.deliverOrders();
        }

        else if(chooseItem == 4){
            exitFlag = false;
        }
        else{
            cout << "Invalid choice, choose again" << endl;

        }
    }








    return 0;
}
