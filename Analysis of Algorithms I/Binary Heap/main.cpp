/*my program first insert 5 taxis in to the heap to overcome update conflicts
 * later starts to count for 100 operations, in my implementation first taxi is called at 105 and it goes as 205 305... */
//g++ main.cpp Binaryheap.cpp
//Ekin Çelebi
#include <iostream>
#include <fstream>
#include "Binaryheap.h"
#include <cstdlib>
#include <ctime>
#include <cmath>
#include <time.h>       /* time */
#include <queue>

using namespace std;



int random_generator(int max=100){
    /* generate secret number between 1 and 100: */
    int random = rand() % max + 1;
    //cout << random << endl;
    return random;
}


int main(int argc, char* argv[]){
    //A new taxi can become available in the city
    //Some taxis’ distances to the hotel location can be updated
    //If an operation is an update, a random taxi’s distance value will be decreased by 0,01.
    //The hotel desk clerk may call the current nearest taxi

    //The closest taxi to the hotel location will be removed after every 100 operations
    //If an is an addition, new information will be read from the provided file, and the distance value of the new taxi will be added to the PQ.
    //Simulation stops after m operations

    /* initialize random seed: */
    srand(time(0));
    int random;

    
    int m = atoi(argv[1]);
    double p = atof(argv[2]);




    //insert lines to the locations queue
    queue<double> locations;
    double longtitude, latitude, distance;
    ifstream file;
    file.open("locations.txt");

    if (!file){
        cerr << "File cannot be opened!";
        exit(1);
    }

    string line;

    getline(file, line); //this is the header line
    for(int i = 0; i<m; i++){
        file >> line; //longtitude
        longtitude = stod(line);
        file >> line; //latitude
        latitude = stod(line);
        getline(file, line, '\n'); //this is for reading the \n character into dummy variable.
        distance = sqrt((longtitude*longtitude)+(latitude*latitude));
        locations.push(distance);

    }
    //Binaryheap simulation;
    //Binaryheap<double> *simulation = new Binaryheap<double>(m);
    Binaryheap *simulation = new Binaryheap(m);

    double taxi;
    int random_taxi_index;
    double nearest_taxi;

    int addCount = 0;
    int updateCount = 0;

    clock_t t;
    t = clock();

    
    //insert 5 taxis to heap to overcome update conflicts
    for(int start=0;start<5;start++){
        taxi = locations.front();
        locations.pop();
        simulation->insert(taxi);
        addCount++;
    }
    m-=5;


    int outer = m/100;
    int mod = m % 100;



    for(int i=0; i<outer; i++){
        for(int j=0; j<99; j++){
            //taxi insert or update with probability
            random = random_generator();
            if (random <= int(p*100.0) ){
                //a random taxi’s distance value will be decreased by 0,01.
                random_taxi_index = random_generator(simulation->getSize());
                taxi = simulation->distance_by_index(random_taxi_index);
                taxi -= 0.01;
                simulation->decreaseValue(random_taxi_index,taxi);
                updateCount++;
            }
            else{
                //get taxi location
                taxi = locations.front();
                locations.pop();
                simulation->insert(taxi);
                addCount++;
            }
        }
        nearest_taxi = simulation->extractMin();
        cout << "clerk called the nearest taxi, the distance is: " << nearest_taxi << endl;

    }

    for(int k=0; k<mod; k++){
        random = random_generator();
        if (random <= int(p*100.0) ){
            //a random taxi’s distance value will be decreased by 0,01.
            random_taxi_index = random_generator(simulation->getSize());
            taxi = simulation->distance_by_index(random_taxi_index);
            taxi -= 0.01;
            simulation->decreaseValue(random_taxi_index,taxi);
            updateCount++;
        }
        else{
            //get taxi location
            taxi = locations.front();
            locations.pop();
            simulation->insert(taxi);
            addCount++;
        }
    }
    t = clock() - t;
    cout <<"exec time: "<< ((float)t)/CLOCKS_PER_SEC << endl;
    cout << "p: " << p << endl;
    cout << "update count: " << updateCount << endl;
    cout << "add count: " << addCount << endl;
    //simulation->print();


}
