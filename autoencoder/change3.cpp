#include <iostream>
#include <string>
#include <cstring>
#include <sstream>
#include <unordered_map>

using namespace std;

int main() {


    string temp;
    string sentence;
    while(getline(cin, sentence)) {
        istringstream iss(sentence);
        iss >> temp;
        iss >> temp;
        iss >> temp;

        if(temp.length() == 1) {
            continue;
        } else {
            cout << sentence << endl;
        }

    }



    /*
    unordered_map<string, int> exists;
    string sentence;
    while(getline(cin, sentence)) {
        if(exists.find(sentence) == exists.end()) {
            exists[sentence] = 1;
        } 
    }

    for(auto it = exists.begin(); it != exists.end(); ++it) {
        cout << it->first << endl;
    }*/
   /* int count = 0;
    string sentence;
    while(getline(cin, sentence)) {
        
        if(count == 50000) break;
        cout << sentence << endl;
        ++count;

    }*/

}
