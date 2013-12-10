#include <iostream>
#include <string>
#include <cstring>
#include <cctype>
#include <deque>
#include <sstream>

using namespace std;

#define SENTENCE_LENGTH = 3

int CountWords( char* str)
{
    bool inSpaces = true;
    int numWords = 0;
    while (*str != '\0') {
        if (std::isspace(*str)) {
            inSpaces = true;
        }
        else if (inSpaces) {
            numWords++;
            inSpaces = false;
        }
        ++str;
    }
    return numWords;
}

/*
 *
 *  This file performs a moving window extraction on sentences being fed in.
 *  We are asuuming sentences are of length >=3
 *  For example, if a sentence is "i am a boy", we obtain "i am a" and "am a boy"
 *  as output
 *
 */
int main() {

    string sentence;
    while(getline(cin, sentence)) {
        char *cstr = new char[sentence.length() + 1];
        strcpy(cstr, sentence.c_str());
        if(CountWords(cstr) == 3) {
            cout << sentence <<  endl;
        }
        else {
            istringstream iss(sentence);
            deque<string> words;
            string temp;
            string tempSentence;
            while(iss) {
                iss >> temp;
                words.push_back(temp);
            }
            for(int j=0; j<words.size(); j++) {
                bool to_break = false;
                for( int i=0; i<SENTENCE_LENGTH; i++) { 
                     if((words.size() - j-1)/SENTENCE_LENGTH == 0) {
                         to_break = true;
                     } else {
                         if(tempSentence.length() != 0) {
                             tempSentence += " ";
                         }
                         tempSentence += words[j+i];
                         if(i==2) {
                             cout << tempSentence << endl;
                             tempSentence = ""; 
                         }
                     }
                }
                if(to_break) break;
            }

        }
    }
    return 0;

}
