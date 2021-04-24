//
// Created by ios on 23.12.2020.
//

#ifndef UNTITLED57_BINARYHEAP_H
#define UNTITLED57_BINARYHEAP_H


class Binaryheap{
    double *array;
    int size;
public:
    Binaryheap()
    {
        array = new double[500];
        size = -1;
    }
    Binaryheap(int n)
    {
        array = new double[n];
        size = -1;
    }
    void print();
    double distance_by_index(int i){return array[i];};
    int getSize(){ return size;}
    int parent(int i){ return (i - 1) / 2;}
    void minHeapify(int i);
    void insert(double p);
    double extractMin();
    void decreaseValue(int i, double p);
};
#endif //UNTITLED57_BINARYHEAP_H
