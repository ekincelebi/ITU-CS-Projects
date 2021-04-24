//-----------------------------------------------------
//Ekin Çelebi
//150160152
//g++ main.cpp -std=c++11 -o main && ./main "input1.txt"
//------------------------------------------------------
#include <iostream>
#include <fstream>
#include <string>
#include "neuronInstructions.h"



int main(int argc, char* argv[]) {
    
    if (argc > 1) {
        
    } else {
        cout << "No file name entered. Exiting...";
        return -1;
    }


    int size;

    int *neuronLayer;

    int *neuronType;

    float *inputVal;

    fstream file(argv[1]);  //open the file
    
    int str;

    int word_count = 0;
    int layer_counter = 0;
    int type_counter = 0;
    int in_counter = 0;

    while (file >> str) {


        if(word_count == 0){
            size = str;
            //cout <<"size "<< size << endl;
            neuronLayer = new int[size];
            neuronType = new int[size];
            inputVal = new float[size];
            word_count++;
        }
        else if(word_count == 1 || word_count <= (size)){
            neuronLayer[layer_counter] = str;
            word_count++;
            layer_counter++;
        }

        else if(word_count == (size+1) || word_count <= (size*2)){
            try {
                if(str <= 2 && str >= 0 ){
                    neuronType[type_counter] = str;
                    word_count++;
                    type_counter++;}
                else {
                    throw(str);
                }
            }

            catch(...) {
                cout << "Unidentified activation function!" << endl;
                exit(1);

            }

        }

        else if(word_count >= ((size*2)+1)){
            inputVal[in_counter] = str;
            word_count++;
            in_counter++;
        }
    }


    try{
        if(in_counter > size) throw(str);
    }

    catch(...) {
        cout << "Input shape does not match!" << endl;
        exit(1);

    }

    Network mynetwork;

    Layers *allLayers = new Layers[size]; //create layers

    for(int i=0; i<size; i++){
         //set neuron type and neuron numbers for layers

        if(i == size-1){(allLayers+i)->setFunc(neuronType[i],neuronLayer[i],i,0);}
        else{(allLayers+i)->setFunc(neuronType[i],neuronLayer[i],i,neuronLayer[i+1]);}

        if(i == 0){

            allLayers->setInputs(inputVal);
        }
        else{

            (allLayers+i)->setInputs((allLayers+(i-1))->returnOutArray()); //last layers output is next layers input;
        }

        (allLayers+i)->makeNodes();
        (allLayers+i)->observeOutArray();
        mynetwork.add2end(allLayers+i);

    }

    mynetwork.print();

    delete[] neuronLayer;

    delete[] neuronType;

    delete[] inputVal;

    

}

