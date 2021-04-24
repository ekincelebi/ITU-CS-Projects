/* @Author
 Student Name: EKIN CELEBI
 Student ID: 150160152
 Date: 19.12.2019 */

#include <iostream>
#include <iomanip>
#include <string>
#include <fstream>


using namespace std;
struct element{
    //struct used for path finds
    int num;
    element *next;
};
struct mobile{
    //struct for mobile hosts
    int id;
    mobile *next;
};

struct node{
    //struct for bases
    int base;
    node* child; //point to children of this node
    node* sibling; //point to next node at same level
    
    mobile* q_head; //bases holds queue for their hosts
    mobile* q_tail;
};

struct mystack{
    //will be used for path finds
    element *head;
    element *create_El(int number); //create element
    void create(); //create stack
    void push(element *pushed);
    void pop();
    bool isEmpty(); //check if stack is empty
    void push_to_stack(node *ptr); //pushes tree to stack recursively
};

int find_parent_flag;
int flag; //flag for print_untill func
int host_find; //flag of the founded host
node *return_base;

struct tree{
    node *root;
    void create_tree();
    node* create_node(int data);
    mobile* create_host(int id);
    void insert(node *nptr, int data, int base); //insert bases
    void add_queue(node *nptr,int id, int base); //adds hosts
    void print_untill(node *ptr,int data); //prints bases untill the given base
    void print_all(node *ptr); //prints all bases in the tree
    void base_of_host(node *ptr, int hostnum); //finds bases of the given host and updates return_base
    void find_node(node *ptr, int leaf); //finds the parent of a node and returns
    node *return_node;
};

typedef tree Datastructure;


void mystack::push_to_stack(node *ptr){
    if(ptr){
        push(create_El(ptr->base));
        push_to_stack(ptr->child);
        push_to_stack(ptr->sibling);
    }
}


void tree::print_all(node *ptr) {
    if(ptr){
        cout << ptr->base << " ";
        print_all(ptr->child);
        print_all(ptr->sibling);
    }
    
}

void tree::print_untill(node *ptr,int data) {
    
    if(!ptr)return;
    
    if(ptr->base == data){
        cout << ptr->base << " ";
        flag = 1; //base is reached, update flag
        return;
    }
    if(flag == 0){ //recurse untill null ptr or base is reached
        cout << ptr->base << " ";
        print_untill(ptr->child,data);
        print_untill(ptr->sibling,data);
    }
}

void tree::find_node(node *ptr, int number) {
    //takes tree updates return_node as node with the number base
    if(!ptr)
        return;
    if (ptr->base == number){
        return_node = ptr;
        return;
    }
    
    find_node(ptr->child, number);
    find_node(ptr->sibling, number);
    
    
}


void tree::base_of_host(node *ptr, int hostnum) {
    
    //first traverse in the host queue
    mobile *temp;
    if (host_find == 0 && ptr) {
        temp = ptr->q_head;
        while (temp) {
            if (temp->id == hostnum) {
                host_find = 1; //flag that host is found
                
                return_base = ptr; //if host is found update return_base with host' base
                return;
            }
            temp = temp->next;
        }
        
        base_of_host(ptr->child, hostnum); //recurse untill the host is bfound
        base_of_host(ptr->sibling, hostnum);
        
    }
}

void tree::create_tree() {
    root = create_node(0);
    flag = 0;
    host_find = 0;
    //root->parent = NULL;
}
node * tree::create_node(int data) {
    node *nn = new node;
    nn->base = data;
    nn->child = NULL;
    nn->sibling = NULL;
    
    nn->q_tail = NULL;
    nn->q_head = NULL;
    
    
    return nn;
}

mobile * tree::create_host(int id) {
    mobile *mh = new mobile;
    mh->id = id;
    mh->next = NULL;
    return mh;
}


void tree::insert(node *nptr, int data, int base) {
    
    if(nptr->base == base){
        node *nn;
        nn = create_node(data);
        
        if(nptr->child == NULL){
            nptr->child = nn;
        }//if base has no child insert its first child
        
        else{
            nptr = nptr->child;
            while(nptr->sibling != NULL){
                nptr = nptr->sibling;
            }
            nptr->sibling = nn;
        }//if base has child add as sibling
        
        return; //exit condition
    }
    
    
    if(nptr->child) //recurse to find the base
        insert(nptr->child,data,base);
    
    if(nptr->sibling)
        insert(nptr->sibling,data,base);
}

void tree::add_queue(node *nptr, int id, int base) {
    //find the base where the host belongs
    //add the host id to to the last elemen t of the queue
    
    if(nptr->base == base){
        
        if(nptr->q_head == NULL){
            nptr->q_head = create_host(id);
            nptr->q_tail = nptr->q_head;
            
        }
        
        else{
            
            mobile *temp = create_host(id);
            nptr->q_tail->next = temp;
            nptr->q_tail = temp;
        }
        
        return;  //exit condition
    }
    
    
    if(nptr->child)
        add_queue(nptr->child,id,base);
    
    if(nptr->sibling)
        add_queue(nptr->sibling,id,base);
}

element* mystack::create_El(int number) {
    element *temp = new element;
    temp->num = number;
    temp->next = NULL;
    return temp;
}
void mystack::create() {
    head = NULL;
}

void mystack::push(element *pushed) {
    if(head == NULL){
        head = pushed;
    }
    else{
        pushed->next = head;
        head = pushed;
    }
}

void mystack::pop() {
    element *temp;
    temp = head;
    head = head->next;
    //return temp;
}

bool mystack::isEmpty() {
    if(head == NULL){
        return true;
    }
    else
        return false;
}

typedef mystack ADatastructure;
typedef mystack ASecondDatastructure;

int main()
{   ADatastructure mainStack;
    ASecondDatastructure printStack;
    
    Datastructure mytree;
    
    ifstream in("Network.txt");
    
    if(!in.is_open())
        cout<<"ERROR:  Network file could not been open"<<endl;
    
    mytree.create_tree();
    
    string BS = "BS";
    string type, own, base;
    int int_own, int_base;
    while(true )
    {
        if(in.eof())
            break;
        
        getline(in,type,' ');
        getline(in,own,' ');
        getline(in,base,'\n');
        
        int_own = stoi(own);
        int_base = stoi(base);
        
        
        
        if(type.compare(BS)==0){
            mytree.insert(mytree.root,int_own,int_base);
        }
        
        else{
            mytree.add_queue(mytree.root,int_own,int_base);
        }
    }
    in.close(); //tree is constructed
    
    mainStack.create(); //a Stack that keeps every node of a tree
    printStack.create();    //a Stack that keeps full path to a tree node
    
    ifstream in2("Messages.txt");
    if(!in2.is_open())
        cout<<"ERROR: Messages file could not been open"<<endl;
    
    
    string message, target;
    
    int int_target;
    
    
    
    while(1)
    {
        getline(in2,message,'>');
        
        
        getline(in2,target,'\n');
        
        if(in2.eof())
            break;
        
        int_target = stoi(target);
        
        mytree.base_of_host(mytree.root,int_target);
        
        if(host_find == 1){
            //if host belongs to a base
            mainStack.push_to_stack(mytree.root);
            //push tree to stack
            host_find = 0; //reset the host_find flag
            int var = return_base->base;
            cout << "Traversing:";
            mytree.print_untill(mytree.root,var);
            flag = 0; //reset the flag
            cout << endl;
            
            
            node *finder;
            while(!mainStack.isEmpty()){
                //after this used to find path to a target node
                while(mainStack.head->num!= var){
                    mainStack.pop(); //pop untill target node
                    if(mainStack.isEmpty()){
                        printStack.push(mainStack.create_El(0));
                        break;
                    }
                    
                }
                
                if(!mainStack.isEmpty()){
                    printStack.push(mainStack.create_El(var)); //every parent of target to printStack
                    mainStack.pop();//first element after var
                    
                    if(mainStack.isEmpty())
                        break;
                    while(true){
                        mytree.find_node(mytree.root,mainStack.head->num);
                        finder = mytree.return_node;
                        
                        node *tempfinder;
                        tempfinder = finder->child;
                        while(tempfinder){
                            
                            if(tempfinder->base == var)
                                break;
                            tempfinder = tempfinder->sibling;
                        }
                        
                        if(tempfinder && tempfinder->base == var){
                            var = mainStack.head->num;
                            printStack.push(mainStack.create_El(var));
                            
                            mainStack.pop();
                            break;
                        }
                        
                        
                        mainStack.pop();
                    }
                }
            }
            cout << "Message:"<< message << " To:";
            
            
            while(!printStack.isEmpty()){
                cout << printStack.head->num;
                cout << " ";
                printStack.pop();
                
            }
            
            cout << "mh_"<< int_target << endl;
            
            
            find_parent_flag = 0;
            
            
        }
        else {
            //print all nodes
            cout << "Traversing:";
            mytree.print_all(mytree.root);
            cout << endl;
            cout << "Can not be reached the mobile host mh_" << int_target << " at the moment" << endl;
        }
    }
    in2.close();
    
    return 0;
    
}

