#pragma once

#include <cstring>
#include <iostream>



using byte = unsigned char;

using namespace std;


struct packet
{
    u_int8_t content[512];
    packet* next = nullptr;

};


class List {

    packet* head;

    u_int8_t retarray[512];

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

        // fügt den inhalt eines Arrays in die Linked list:
        void insert(int conten[]){
            packet* newPack = new packet;
            std::cout << "in insert" << std::endl;
            try {
                for (int i = 0; i<512; i++) {
                    newPack->content[i] = conten[i];
                }
            }catch (const std::exception& e){
                std::cout << "Error in der übertragung von content" << std::endl;
            }
            //memcpy(newPack->content, conten, 512);
           
            packet* n = head;
            try{
                if (head == nullptr) {
                    head = newPack;
                    return;
                }else{
                    while(n->next != nullptr){
                        n = n->next;
                    }
                    n->next = newPack;  
                }
            }catch (const std::exception& e){
                std::cout << "Error in der suche nach dem letzten element" << std::endl;
            }
            
        };

        // gibt den head der list zurück und löscht diesen. setzt das nächste element der lists auf den head.
        u_int8_t* get() {
            if (head == nullptr) {
                //cout << "List is already empty!" << endl;
                return retarray;
            }else{
                for (int i = 0; i<512; i++) {
                    retarray[i] = head->content[i];
                }
                packet* toDelete = head;
                head = head->next;
                delete toDelete;
                return retarray;  
            }

            
        }

        //gibt den head zuück:
        packet* getHead() {
            return head;
        }
};


        