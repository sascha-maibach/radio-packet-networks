#pragma once

#include <cstring>
#include <iostream>

using byte = unsigned char;

using namespace std;


struct packet
{
    int content[512];
    packet* next;

};


class List {

    packet* head;

    int retarray[512];

    public:

        List(): head(nullptr) {}

        ~List() {
            packet* current = head;
            while (current != nullptr) {
                packet* toDelete = current;
                current = current->next;
                delete toDelete;
            }
        }

        void insert(int conten[]){
            packet* newPack = new packet;
            memcpy(newPack->content, conten, 512);

            packet* n = head;
            if (head == nullptr) {
                head = newPack;
                return;
            }else{
                while(n->next != nullptr){
                    n = n->next;
                }
                n->next = newPack;  
            }
        };

        int* get() {
            copy(head->content, head->content + 512, retarray);
            if (head == nullptr) {
                cout << "List is already empty!" << endl;
                return retarray;
            }else{
                packet* toDelete = head;
                head = head->next;
                delete toDelete;
                return retarray;  
            }

            
        }

        packet* getHead() {
            return head;
        }
};


        