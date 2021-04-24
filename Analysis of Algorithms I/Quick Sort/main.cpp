/*
 Ekin Çelebi
 150160152
 10.12.2020
 */
#include<iostream>
#include<fstream>
#include<string>
#include <time.h>

using namespace std;

class GlobalSales{

public:
    string country,itemType,orderID;
    long int unitsSold;
    double totalProfit;
    GlobalSales(string country="", string itemType="", string orderID="");
    void print(){
        cout << this->country << " " << this->itemType << " " << this->orderID << " " <<this->unitsSold << " " << this->totalProfit << endl;
    };



};
GlobalSales::GlobalSales(string country, string itemType, string orderID) {
    this->country=country;
    this->itemType=itemType;
    this->orderID=orderID;
}

void writeToFile(GlobalSales *array, int itemNum, string header){
    ofstream writeFile("sorted.txt");
    writeFile << header << endl;
    for(int i=0; i<itemNum; i++){
        writeFile << array[i].country << "\t" << array[i].itemType << "\t" << array[i].orderID  << "\t" << array[i].unitsSold << "\t" << array[i].totalProfit << endl;
    }
    writeFile.close();
}

void swap(GlobalSales *sale1,GlobalSales *sale2){
    GlobalSales temp = *sale1;
    *sale1 = *sale2;
    *sale2 = temp;
}

int partition(GlobalSales a[], int l, int r){

    GlobalSales pivot = a[l]; //pivot is the first unsorted element
    int smallerIndex = l;
    for(int biggerIndex = l+1; biggerIndex <= r; biggerIndex++){
        //bigger index iterates untill the last element

        if (a[biggerIndex].country < pivot.country){
            //alphabetically smaller countries placed to the left side
            smallerIndex++;
            swap(&a[smallerIndex], &a[biggerIndex]);
            //swap to collect smaller than pivot elements to the left
        }
        if (a[biggerIndex].country == pivot.country){
            if(a[biggerIndex].totalProfit >= pivot.totalProfit){
                //if same country the ones with the higher profit are placed to the left side.
                smallerIndex++;
                swap(&a[smallerIndex], &a[biggerIndex]);
                //swap to collect smaller than pivot elements to the left
            }
        }
    }
    //last swap carries pivot so that left side elements are smaller
    swap(&a[l], &a[smallerIndex]);
    return smallerIndex;
}

void quickSort(GlobalSales a[], int l, int r){

    if(l < r){
        int p = partition(a, l, r);
        //p is the index coming from partition result
        quickSort(a, l, p-1);
        quickSort(a, p+1, r);
    }
}

int main(int argc, char *argv[]){
    string headerLine;

    ifstream file;
    file.open("sales.txt");

    if (!file){
        cerr << "File cannot be opened!";
        exit(1);
    }

    int N =  atoi(argv[1]);; //you should read value of N from command line
    //int N =  1000;

    GlobalSales *sales = new GlobalSales[N];

    string line;
    clock_t t;

    getline(file, line); //this is the header line
    headerLine = line;
    for(int i = 0; i<N; i++){

        getline(file, line, '\t'); //country (string)
        sales[i].country = line;
        getline(file, line, '\t'); //item type (string)
        sales[i].itemType = line;
        getline(file, line, '\t'); //order id (string)
        sales[i].orderID = line;

        file >> line; //units sold (integer)
        sales[i].unitsSold = stol(line);
        file >> line; //total profit (float)
        sales[i].totalProfit = stof(line);
        getline(file, line, '\n'); //this is for reading the \n character into dummy variable.

    }

    t = clock();
    quickSort(sales, 0, N-1);
    t = clock() - t;
    cout <<"N: "<< N << endl;
    //cout <<"exec time: "<< t << endl;
    cout <<"exec time: "<< ((float)t)/CLOCKS_PER_SEC << endl;





    writeToFile(sales, N, headerLine);
    return 0;
}
