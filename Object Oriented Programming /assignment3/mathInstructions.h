//
//  mathInstructions.h
//Ekin Çelebi
//150160152
//

#ifndef mathInstructions_h
#define mathInstructions_h
#include <iostream>
#include <math.h>

using namespace std;

//----------------------------------------------------
//Neuron Operations Blocks

float sigmoid(const float x)
{
    float exp_value;
    exp_value = exp((double) -x);
    return 1 / (1 + exp_value);
}

float leakyReLu(const float x){
    return fmax((double)(0.1 * x) ,(double) x);
}
float reLu(const float x){
    return fmax(0,(double) x);
}
//----------------------------------------------------


#endif /* mathInstructions_h */
