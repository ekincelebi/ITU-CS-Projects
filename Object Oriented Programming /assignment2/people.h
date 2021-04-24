/*
Ekin Celebi
150160152
04.05.2020
*/

#include <iostream>
#include<string>
#include <array>

using namespace std;

class Person{
    protected:
        string name;
        string surname;

    public:
        Person();
        Person(const string &,const string &);
        ~Person();

        //set functions
        void setName(const string &in_name){
            name = in_name;
        }
        void setSurname(const string &in_surname){
            surname = in_surname;
        }
        
    //get functions
        string getName() const{
            return name;
        }
        string getSurname() const{
            return surname;
        }
};
Person::Person() {
    //cout << "Person Default Constructor" << endl;
}
Person::Person(const string &p_name, const string &p_surname):
                                        name(p_name),
                                        surname(p_surname){
    //cout << "Person Constructor" << endl;
}

Person::~Person() {
    //cout << "Person Destructor" << endl;
}

class Owner:public Person{
    int ownership;

    public:
    
    Owner();
    Owner(const string &,const string &);
    ~Owner();
    

    int getOwnership() const{
        return ownership;
    }
    void setOwnership(const int &param_owner){
        ownership = param_owner;
    }
};
Owner::Owner() {
    //cout << "Owner Default Constructor" << endl;
}
Owner::Owner(const string &o_name, const string &o_surname):
                                                    Person(o_name,o_surname){
    //cout << "Owner Constructor" << endl;
}

Owner::~Owner() {
    //cout << "Owner Destructor" << endl;
}


class Courier:public Person{
    string vehicle;
    int trans_capacity;

    public:
        Courier();
        Courier(const string &,const string &,const string &);
        ~Courier();
        
    string getVehicle() const{
            return vehicle;
        }
        int getTransCap() const{
            return trans_capacity;
        }
    
        // == overload
        bool operator==(const Courier&) const;
};

Courier::Courier(){
    //cout << "Courier Default Constructor" << endl;

}
Courier::Courier(const string &c_name, const string &c_surname, const string &c_vehicle):
                                                                        Person(c_name,c_surname) {
    if(c_vehicle != "car" && c_vehicle != "motorcycle" && c_vehicle != "bicycle"){
        cout << "Vehicle should be either car, motorcycle or bicycle" << endl;
        //check for vehicle type
    }

    else {
        //cout << "Courier Constructor" << endl;
        vehicle = c_vehicle;
        if(c_vehicle=="car") trans_capacity = 200;
        else if(c_vehicle=="motorcycle") trans_capacity = 35;
        else if(c_vehicle=="bicycle") trans_capacity = 10;
    }

}

Courier::~Courier() {
    //cout << "Courier Destructor" << endl;
}

bool Courier::operator==(const Courier &inCourier) const {
    //return true if name surname and vehicle type is equal
    bool isEqual = false;
    if(name == inCourier.name){
        if(surname == inCourier.surname){
            if(vehicle == inCourier.vehicle)
                isEqual = true;
        }
    }
    return isEqual;
}

class Business{
    string business_name;
    string address;

    Owner *businessOwners; //array of owners
    int numOwner; //how many owners

    
    Courier *businessCouriers;

    
    int nextCourierIndex; // hold next index for dynamically allocation operations
    int courierArrLength;//holds the size of courier array length for hire and fire operations

    public:
        Business(const string &, const string &, const Owner*, const int &);
        ~Business();
        void hire_courier(const Courier &);
        void fire_courier(const Courier &);
        void list_owners() const;
        void list_couriers() const;
        int calculate_shipment_capacity();
        void operator()()const;
        const Courier &operator[](int);

};



Business::Business(const string &b_name, const string &b_address, const Owner *in_Owner, const int &in_numOwner):
                                                                    business_name(b_name),address(b_address){

    nextCourierIndex = 0; //no courier is hired at the beginnig
    courierArrLength = 10;//initial value of the courier array is 10
    numOwner = in_numOwner;
    int percentage = 100/numOwner; //ownership percentage for each owner
    businessOwners = new Owner[numOwner];
    businessCouriers = new Courier[courierArrLength];

    for(int i=0; i < numOwner ; i++){

        businessOwners[i] = in_Owner[i];
        //businessOwners[i].setName(in_Owner[i].getName());
        //businessOwners[i].setSurname(in_Owner[i].getSurname());
        businessOwners[i].setOwnership(percentage);
    }

}

void Business::list_owners() const{
    for(int j=0; j < numOwner ; j++){
    
        cout << businessOwners[j].getName() << " " << businessOwners[j].getSurname() << " " << businessOwners[j].getOwnership() << endl;

    }
}


void Business::list_couriers() const {
    for(int j=0; j <nextCourierIndex ; j++){
    
        cout << businessCouriers[j].getName() << " " << businessCouriers[j].getSurname() << " "  << businessCouriers[j].getVehicle() << endl;

    }
}

int Business::calculate_shipment_capacity() {
    int acc = 0;
    for(int j=0; j <nextCourierIndex ; j++){
      
        acc += businessCouriers[j].getTransCap();

    }
    return acc;
}


Business::~Business() {
    //cout << "Business Destructor" << endl;
    delete[] businessOwners;
    delete[] businessCouriers;
}

void Business::hire_courier(const Courier &param_courier) {


    if(param_courier.getVehicle() == "car" || param_courier.getVehicle() == "motorcycle" || param_courier.getVehicle() == "bicycle"){
        
        //check if array size if enough, if not create bigger array with +10 size
        if(nextCourierIndex < courierArrLength){
            businessCouriers[nextCourierIndex] = param_courier;
            nextCourierIndex++;
        }

        else{

            Courier *newBC;
            newBC = new Courier[courierArrLength+10];
            for (int i = 0; i < courierArrLength; i++)
                newBC[i] = businessCouriers[i];
            courierArrLength = courierArrLength+10;

            newBC[nextCourierIndex] = param_courier;
            delete[] businessCouriers;
            businessCouriers = newBC;
            nextCourierIndex++;
        }
    }
}

void Business::fire_courier(const Courier &courIn) {
    int errorFlag = 1;
    for(int i=0; i< nextCourierIndex; i++){
        if(businessCouriers[i] == courIn){
            
            //remove courier
            //shrink size by one and decrease index by one
            Courier *newArray = new Courier[courierArrLength-1];
            for(int j=0; j<i; j++){
               newArray[j] = businessCouriers[j];
            }

            for(int k=i+1;k<nextCourierIndex;k++){
                newArray[k-1] = businessCouriers[k];
            }

            delete[] businessCouriers;
            businessCouriers = newArray;
            nextCourierIndex--;

            errorFlag = 0; //if courier found deactivate errorFlag
            break;
        }
    }
    if(errorFlag == 1)
        cout << "Can not fire, Courier does not exist" << endl;
}

void Business::operator()() const {
    cout << business_name << " ";
    cout << address << endl;
    list_owners();
    list_couriers();

}

const Courier& Business::operator[](int index) {
    if(index<0 || index>= nextCourierIndex){
        Courier *ptr;
        cout<<"No courier with this index" << endl;
        return *ptr;
    }
    else{
        return *(businessCouriers+index);

    }

}
