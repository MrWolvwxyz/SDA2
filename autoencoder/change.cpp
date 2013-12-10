#include <iostream>
#include <string>
#include <cstring>
#include <cctype>

using namespace std;

int CountWords(char* str);
int CountWords( char* str)
{
          bool inSpaces = true;
             int numWords = 0;

                while (*str != '\0')
                       {
                                 if (std::isspace(*str))
                                           {
                                                        inSpaces = true;
                                                              }
                                       else if (inSpaces)
                                                 {
                                                              numWords++;
                                                                       inSpaces = false;
                                                                             }

                                             ++str;
                                                }

                   return numWords;
}










int main() {

    string sentence;
    while(getline(cin, sentence)) {
        char *cstr = new char[sentence.length() + 1];
        strcpy(cstr, sentence.c_str());
        if(CountWords(cstr) > 2) {
            cout << sentence <<  endl;
        }
    }
    return 0;

}
