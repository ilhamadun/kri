#ifndef _CLENT_H_
#define _CLENT_H_

#include <string>
#include "restclient-cpp/connection.h"
#include "restclient-cpp/restclient.h"

/**
    Penghubung program dengan server KRI

    Class ini digunakan untuk login dan logout dengan membuat HTTP request ke server KRI.
*/
class Client {
    private:
        std::string username;
        std::string password;
        RestClient::Connection* connection;

        /**
            Membut pesan untuk request dalam format JSON

            @param card_key     id kartu
            @return pesan dalam JSON
        */
        std::string create_json(std::string card_key);

    public:
        /**
            Inisialisasi koneksi dengan server KRI

            @param host_url     alamat server KRI
            @param user         username admin
            @param pass         password admin
        */
        Client(std::string host_url, std::string user, std::string pass);

        /**
            Login peserta

            TODO: Memperjelas response sebagai status login
        */
        RestClient::Response login(std::string card_key);

        /**
            Logout peserta

            TODO: Memperjelas response sebagai status logout
        */
        RestClient::Response logout(std::string card_key);
};

#endif