#include <string>
#include "client.h"

Client::Client(std::string host_url, std::string user, std::string pass) :
username(user), password(pass) {
    connection = new RestClient::Connection(host_url);

    RestClient::HeaderFields headers;
    headers["Accept"] = "application/json";
    connection->SetHeaders(headers);
    connection->AppendHeader("Content-Type", "text/json");
}

std::string Client::create_json(std::string card_key) {
    std::string json = "{";
    json += "\"username\": \"" + username + "\"";
    json += "\"password\": \"" + password + "\"";
    json += "\"card_key\": \"" + card_key + "\"";
    json += "}";

    return json;
}

RestClient::Response Client::login(std::string card_key) {
    std::string message = create_json(card_key);
    RestClient::Response response = connection->post("/attendance/login/", message);

    return response;
}

RestClient::Response Client::logout(std::string card_key) {
    std::string message = create_json(card_key);
    RestClient::Response response = connection->post("/attendance/logout/", message);

    return response;
}
