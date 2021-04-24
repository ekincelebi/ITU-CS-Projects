//
//  neuronInstructions.h
//Ekin Çelebi
//150160152
//


#ifndef neuronInstructions_h
#define neuronInstructions_h
#include <iostream>
#include "mathInstructions.h"

using namespace std;

//----------------------------------------------------
//Neurons

class Neuron{// Abstract base class
protected:
    float z,a;
    int type;
public:
    Neuron(){} //default constructor
    virtual void activate() =0;  // pure virtual method
    float getA(){return a;}
    float getZ(){return z;}
    int getType(){return type;}
    void setZ(float z_in){ z = z_in; }
    void setA(float a_in){ a = a_in; }
    virtual ~Neuron(){
        //cout << "Neuron Base Destructor" << endl;
        } // virtual destructor

};

class SigmoidNeuron : public Neuron{
public:
    SigmoidNeuron(){type=0;} //default constructor
    SigmoidNeuron(Neuron &obj) {z = obj.getZ(); a = obj.getA(); type=0;}
    void activate(){a = sigmoid(z);}
    ~SigmoidNeuron(){
        //cout << "Sigmoid Neuron Destructor" << endl;
        }
};

class LReluNeuron : public Neuron{
public:
    LReluNeuron(){type=1;} //default constructor
    void activate(){a = leakyReLu(z);}
    LReluNeuron(Neuron &obj) {z = obj.getZ(); a = obj.getA(); type=1;}
    ~LReluNeuron(){
        //cout << "Leaky Relu Neuron Destructor" << endl;
    }
};

class ReluNeuron : public Neuron{
public:
    ReluNeuron(){type=2;} //default constructor
    ReluNeuron(Neuron &obj) {z = obj.getZ(); a = obj.getA(); type=2;}
    void activate(){a = reLu(z);}
    ~ReluNeuron(){
        //cout << "Relu Neuron Destructor" << endl;
        }
};

//----------------------------------------------------


//----------------------------------------------------
//Layer LinkList construction
class LayerNode{
    friend class Layers;
    Neuron *nptr;
    LayerNode *next;
public:
    LayerNode(Neuron&); //create a node
    ~LayerNode(){
        //cout << "layer node object is deleted" << endl;
        delete nptr;
    }
};

LayerNode::LayerNode(Neuron &nobj){
    if(nobj.getType() == 0 ){
        nptr = new SigmoidNeuron(nobj);
    }

    else if(nobj.getType() == 1 ){
        nptr = new LReluNeuron(nobj);
    }

    else if(nobj.getType() == 2 ){
        nptr = new ReluNeuron(nobj);
    }
    next = NULL;
}

//######################################################

class Layers{
    LayerNode *head;
    int type; //add neurons according to type
    int neuronNum; //we have to know neuron number;
    int next_neuron_num; //if we know the next neuron number we can derive out array
    int layerIndex;

    float **w_array;
    float *b_array;

    float *inArray; //input array
    float *outArray; //this layers output will be next layers input
    float *activatedArray; //to make matrix multiplication

public:
    Layers();
    ~Layers();
    void setFunc(int in_type, int in_num, int index, int next_neuron);
    void setInputs(const float param[]);
    void makeNodes();
    void observeOutArray();
    float* returnOutArray();
    void add2end(Neuron *nptr);
    void print() const;
    
};
Layers::Layers(){
    head=NULL;
}
Layers::~Layers(){

    //cout << "Layer Destructor " << endl;
    delete[] inArray;
    delete[] outArray;
    delete[] activatedArray;

    //Free each sub-array
    for(int i = 0; i < next_neuron_num; ++i) {
        delete[] w_array[i];
    }
    //Free the array
    delete[] w_array;

    delete[] b_array;

    LayerNode *d;
    while(head!=NULL){
        d = head;
        delete d;
        head=head->next;
    }
}
void Layers::setFunc(int in_type, int in_num, int index, int next_neuron){
    //initialization function for a layer
    //type, neuron number, layer number, next layers neuron number
    type = in_type;
    neuronNum = in_num;
    layerIndex = index;
    next_neuron_num = next_neuron;

    //space allocation for arrays
    inArray = new float[neuronNum];
    activatedArray = new float[neuronNum];
    outArray = new float[next_neuron_num];

    b_array = new float[next_neuron_num];
    
    w_array = new float*[next_neuron_num];
    for(int i=0; i<next_neuron_num; i++){
        w_array[i] = new float[neuronNum];
    } // create w_array

    for(int k=0; k<next_neuron_num; k++){
        for(int j=0; j<neuronNum; j++){
            w_array[k][j] = 0.1; //fill w_array with 0.1
        }
    }

    for(int l=0; l<next_neuron_num; l++){
        b_array[l] = 0.1; //fill b_array with 0.1
    }
}
void Layers::setInputs(const float param[]){
    //set input array
    for(int i=0;i<neuronNum; i++){
        inArray[i] = param[i];
    }
}
void Layers::makeNodes() {
    //initialize z values with respect to inArray
    Neuron *nptr;
    if(type==0)

        nptr = new SigmoidNeuron[neuronNum];

    else if(type==1)

        nptr = new LReluNeuron[neuronNum];

    else if(type==2)

        nptr = new ReluNeuron[neuronNum];

    for(int i=0; i<neuronNum; i++){
        (nptr+i)->setZ(inArray[i]);

        if(layerIndex == 0)
            (nptr+i)->setA(inArray[i]); //same value for only the very first layer


        else if(layerIndex != 0)
            (nptr+i)->activate();

        activatedArray[i] = (nptr+i)->getA(); //initialize activated array

        add2end(nptr+i); //add neurons to layer

    }
    
    
}
void Layers::observeOutArray() {
    //matrix multiplications
    //multiply with w & add to b
    float temp = 0;
    for(int k=0; k<next_neuron_num; k++){
        for(int j=0; j<neuronNum; j++){
            temp += (w_array[k][j]*activatedArray[j]);
        }
        temp += b_array[k];
        outArray[k] = temp; //initialize result to out array
        temp = 0; //temp
    }
}
float* Layers::returnOutArray() {
    return outArray;
}
void Layers::add2end(Neuron *nptr){
    if(nptr==NULL) return;
    LayerNode *newNode = new LayerNode(*nptr);
    if(head == NULL){
        head = newNode;
        return;
    }
    LayerNode *tmp;
    tmp = head;
    while(tmp->next)
        tmp = tmp->next;

    tmp->next = newNode;
}
void Layers::print() const{
    cout <<"Layer " << layerIndex << ":"<< endl;
    LayerNode *tmp = head;
    while(tmp!=NULL){
        //cout << "z value " << tmp->nptr->getZ() << endl;
        cout << tmp->nptr->getA() << endl;
        tmp = tmp->next;
    }
}

//----------------------------------------------------



//----------------------------------------------------
//Network LinkList construction

class NetworkNode{
    friend class Network;
    Layers *lptr;
    NetworkNode *next;
public:
    NetworkNode(Layers&);
    ~NetworkNode(){
        //cout << "network node object is deleted" << endl;
        delete lptr;
    }
};

NetworkNode::NetworkNode(Layers &lobj) {
    lptr = new Layers(lobj);
    next = NULL;
}

//######################################################

class Network{
    NetworkNode *head;
public:
    Network();
    void add2end(Layers &lobj);
    void add2end(Layers *lptr);
    void print() const;
    ~Network() {
        //cout << "network destructor" << endl;
        NetworkNode *n;
        while (head != NULL) {
            n = head;
            delete n;
            head = head->next;
        }
    }
};

Network::Network() {
    head = NULL;
}

void Network::add2end(Layers *lptr) {
    //if(lobj==NULL) return;
    NetworkNode *newNode = new NetworkNode(*lptr);
    if(head== NULL){
        head = newNode;
        return;
    }
    NetworkNode *tmp;
    tmp = head;
    while(tmp->next)
        tmp = tmp->next;

    tmp->next = newNode;
    return;
}


void Network::add2end(Layers &lobj) {
    //if(lobj==NULL) return;
    NetworkNode *newNode = new NetworkNode(lobj);
    if(head== NULL){
        head = newNode;
        return;
    }
    NetworkNode *tmp;
    tmp = head;
    while(tmp->next)
        tmp = tmp->next;

    tmp->next = newNode;
    return;
}


void Network::print() const {
    NetworkNode *tmp;
    tmp = head;
    while(tmp){
        tmp->lptr->print();
        tmp = tmp->next;
    }
    return;
}

//----------------------------------------------------

#endif /* neuronInstructions_h */
