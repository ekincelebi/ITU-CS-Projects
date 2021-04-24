#include<iostream>
#include<fstream>
#include<string>
#include <time.h>
#include <vector>

using namespace std;

class Scores {
public:
    int assist, rebound, point;
    Scores(int assist, int rebound, int point);
    Scores();
    void add(Scores);
};

Scores::Scores(int assist, int rebound, int point){
    this->assist = assist;
    this->rebound = rebound;
    this->point = point;
}
Scores::Scores() {}

void Scores::add(Scores toAdd) {
    this->rebound += toAdd.rebound;
    this->assist += toAdd.assist;
    this->point += toAdd.point;
}

class Node {
public:
    string player_name;
    Node *parent;
    Node *left;
    Node *right;
    Scores scores;
    char color; //1 red, 0 black

    Node(void);
    Node(string,int,int,int);
};

Node::Node(string name, int assist, int rebound, int point) : player_name(name), scores(assist, rebound, point) {}
Node::Node() : left(NULL), right(NULL), scores(), color(0) {}

typedef Node *Ptr;

class RBT {
private:
    Ptr root;
    Ptr NIL;


    // rotate left at given node
    void rotate_left(Ptr current_node) {
        Ptr right_node = current_node->right;
        current_node->right = right_node->left;
        Ptr father = current_node->parent;
        if (right_node->left != NIL) {
            right_node->left->parent = current_node;
        }
        right_node->parent = current_node->parent;
        if (father == NULL) {
            root = right_node;
        } else if (current_node == father->left) {
            father->left = right_node;
        } else {
            father->right = right_node;
        }
        right_node->left = current_node;
        current_node->parent = right_node;
    }

    // rotate right at given node
    void rotate_right(Ptr current_node) {
        Ptr left_node = current_node->left;
        current_node->left = left_node->right;
        Ptr father = current_node->parent;
        if (left_node->right != NIL) {
            left_node->right->parent = current_node;
        }
        left_node->parent = current_node->parent;
        if (father == NULL) {
            root = left_node;
        } else if (current_node == father->right) {
            father->right = left_node;
        } else {
            father->left = left_node;
        }
        left_node->right = current_node;
        current_node->parent = left_node;
    }
    //fix the tree to maintain the rbt rules
    void fix_tree(Ptr node){
        Ptr uncle;
        while (node->parent->color == 'R') {
            if (node->parent == node->parent->parent->right) {
                uncle = node->parent->parent->left;
                if (uncle->color == 'R') {
                    uncle->color = 'B';
                    node->parent->color = 'B';
                    node->parent->parent->color = 'R';
                    node = node->parent->parent;
                } else {
                    if (node == node->parent->left) {
                        node = node->parent;
                        rotate_right(node);
                    }

                    node->parent->color = 'B';
                    node->parent->parent->color = 'R';
                    rotate_left(node->parent->parent);
                }
            } else {
                uncle = node->parent->parent->right;

                if (uncle->color == 'R') {
                    uncle->color = 'B';
                    node->parent->color = 'B';
                    node->parent->parent->color = 'R';
                    node = node->parent->parent;
                } else {
                    if (node == node->parent->right) {
                        node = node->parent;
                        rotate_left(node);
                    }
                    node->parent->color = 'B';
                    node->parent->parent->color = 'R';
                    rotate_right(node->parent->parent);
                }
            }
            if (node == root) {
                break;
            }
        }
        root->color = 'B';

    }

public:
//constructor
    RBT() {

        NIL = new Node;
        root = NIL;
    }

    Ptr search(Ptr node, string key){
        if (node == NIL || key == node->player_name) {
            return node;
        }

        if (key < node->player_name) {
            return search(node->left, key);
        }

        return search(node->right, key);
    }

    //search available leaf to insert new node as red then fix the tree
    void insert(string key, int assist, int rebound, int point) {
        Ptr node = new Node(key,assist,rebound,point);
        node->left = NIL;
        node->right = NIL;
        node->color = 'R'; // new inserted node is always red

        Ptr y = NULL;
        Ptr temp = root;

        while (temp != NIL) {
            y = temp;
            if (node->player_name < temp->player_name) {
                temp = temp->left;
            } else {
                temp = temp->right;
            }
        }

        node->parent = y;
        if (y == NULL) {
            root = node;
        } else if (node->player_name < y->player_name) {
            y->left = node;
        } else {
            y->right = node;
        }

        if (node->parent == NULL){
            node->color = 'B';
            return;
        }

        if (node->parent->parent == NULL) {
            return;
        }

        fix_tree(node);
    }

    Ptr get_root(){
        return root;
    }

    // print the tree by given rule
    void print(Ptr node, string indent) {

        if (node == NIL)
            return;
        cout<<indent;
        indent += "-";
        string sColor = node->color?"RED":"BLACK";
        //first print data
        cout<<"("<<sColor<<") "<<node->player_name<<endl;
        //recurse left
        print(node->left, indent);
        //recurse right
        print(node->right, indent);

    }

};

int main(int argc, char *argv[]){
    string headerLine;

    ifstream file;
    string file_name = argv[1];
    //file.open("sample.csv");
    file.open(file_name);

    if (!file){
        cerr << "File cannot be opened!";
        exit(1);
    }

    string line;
    string name,team,season;
    int rebound,assist,point;


    getline(file, line); //this is the header line
    headerLine = line;

    RBT bst;

    getline(file,line,',');
    season = line;
    string initial_season = season;
    string season_mem = season;

    int season_switch = 0;

    Scores newScore;
    Ptr node;

    Ptr max_reb = new Node;
    Ptr max_point = new Node;
    Ptr max_assist = new Node;

    do{
        season_mem = season;
        getline(file,line,','); //name
        name = line;
        getline(file,line,','); //team
        team = line;
        getline(file,line,','); //rebound
        rebound = stoi(line);
        getline(file,line,','); //assist
        assist = stoi(line);
        getline(file,line,'\n'); //point
        point = stoi(line);

        node = bst.search(bst.get_root(),name);

        if(node->player_name == ""){
            //insert user if does not plays in previous seasons
            bst.insert(name,assist,rebound,point);
            Ptr root = bst.get_root();
            if (rebound >= max_reb->scores.rebound)
                max_reb = bst.search(root,name);

            if (assist >= max_assist->scores.assist)
                max_assist = bst.search(root,name);

            if (point >= max_point->scores.point)
                max_point = bst.search(root,name);

        }else{

            newScore = Scores(assist,rebound,point);
            node->scores.add(newScore);

            if (node->scores.rebound >= max_reb->scores.rebound)
                max_reb = node;

            if (node->scores.assist >= max_assist->scores.assist)
                max_assist = node;

            if (node->scores.point >= max_point->scores.point)
                max_point = node;

        }

        //update its counts
        getline(file,line,','); //next players season
        season = line; //next players season
        if(season_mem.compare(season) != 0){
            season_switch++;

            cout << "End of the " << season_mem << " Season"<< endl;
            cout << "Max Points: " << max_point->scores.point << " - Player Name: " <<  max_point->player_name << endl;
            cout << "Max Assists: " << max_assist->scores.assist << " - Player Name: " <<  max_assist->player_name << endl;
            cout << "Max Rebs: " << max_reb->scores.rebound << " - Player Name: " <<  max_reb->player_name << endl;
            if(season_switch == 1){
                bst.print(bst.get_root(),"");

            }

        }

    }while(file);



}
