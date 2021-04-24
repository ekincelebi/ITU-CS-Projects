//
// Created by ios on 23.12.2020.
//
#include "Binaryheap.h"
#include <iostream>

using namespace std;


void Binaryheap ::print() {
    int i = 0;

    cout << "Priority Queue : ";
    while (i <= size) {
        cout << array[i] << " ";
        i++;
    }
    cout << endl;
}

//each elements value has to be smaller or equal than it's childrens.
void Binaryheap:: minHeapify(int i)
{ //this is min heapify
    int minIndex = i;
    // Left Child
    int l = (2 * i) + 1;
    if (l <= size && array[l] < array[minIndex]) {
        minIndex = l;
    }
    // Right Child
    int r = (2 * i) + 2;
    if (r <= size && array[r] < array[minIndex]) {
        minIndex = r;
    }
    // If i not same as maxIndex
    if (i != minIndex) {
        swap(array[i], array[minIndex]);
        minHeapify(minIndex);
    }
}

//the inserted value is placed as the last leaf and swapped with its parent nodes untill parent's value is higher.
//Complexity O(log N)
void Binaryheap:: insert(double p)
{
    size++;
    array[size] = p;

    //maintain heap property
    int i=size;
    while (i > 0 && array[parent(i)] > array[i]) {
        swap(array[parent(i)], array[i]);
        i = parent(i);
    }
}


//Root is returned, the value at the root is replaced with the last leaf. As replacing the last element violates
//heap minHeapify is performed.
//Complexity O(logN)
double Binaryheap:: extractMin()
{
    double result = array[0];
    array[0] = array[size];
    size = size - 1;
    minHeapify(0);
    return result;
}


//To keep the heap property, untill we get a higher value on parent node, the nodes value is swapped with the parents value.
//Complexity O(log N)
void Binaryheap:: decreaseValue(int i, double p)
{   // Change the value of element
// present at index i with p

    array[i] = p;
    while (i != 0 && array[parent(i)] > array[i])
    {
        swap(array[i], array[parent(i)]);
        i = parent(i);
    }

}

