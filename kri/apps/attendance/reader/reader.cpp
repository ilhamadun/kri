#include <iostream>
#include "restclient-cpp/restclient.h"
#include "client.h"

/**
    Baca kartu dengan RFID reader

    TODO: Implementasi baca kartu

    Implementasinya bebas, yang penting mengembalikan string id dari kartunya.

    @return id kartu
*/
std::string read_card() {
    std::string card_key = "03X537"; // Dummy data

    return card_key;
}


/**
    Loop untuk membaca kartu

    TODO: Implementasi loop
    
    Loop ini memanggil client.login() atau client.logout() setiap kali kartu dibaca.

    @param client   HTTP client ke server KRI
    @param mode     Mode reader, antara "login" atau "logout"
    @return status
*/
int start_reader(Client client, std::string mode) {
    for (int i = 0; i < 1; i++) // Dummy loop
    {
        std::string card_key = read_card();

        if (mode == "login") {
            RestClient::Response response = client.login(card_key);
            std::cout << response.code << std::endl;
        } else {
            RestClient::Response response = client.logout(card_key);
            std::cout << response.code << std::endl;
        }
    }

    return 0;
}


/**
    Main program

    Menginisialisasi hubungan ke host dan memulai reader.

    Cara penggunaan:
        ./reader [login|logout] USERNAME PASSWORD [host]
*/
int main(int argc, char *argv[]) {
    std::string mode = argv[1];
    std::string username = argv[2];
    std::string password = argv[3];
    std::string host;

    if (argc > 4) {
        host = argv[4];
    } else {
        host = "https://kri2017.ugm.ac.id";
    }

    Client client(host, username, password);
    int status = start_reader(client, mode);

    return status;
}
