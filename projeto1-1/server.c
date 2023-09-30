#include <stdio.h>
#include <winsock2.h>
#include <stdlib.h>
#include <string.h>
#include <process.h>

#pragma comment(lib, "ws2_32.lib")
#define PORT 8922

SOCKET clientSockets[100];  // Array para armazenar os sockets dos clientes
int numClients = 0;  // Contador de clientes conectados

typedef struct {
    SOCKET clientSocket;
    int id;
    int isConnected;
    // Outros argumentos que você precisa passar para a função de thread
} ThreadArgs;
ThreadArgs* threadArgs[100];
// Função para envio de mensagens a todos os clientes
void BroadcastMessage(char* message, int id) {
    for (int i = 0; i < numClients; i++) {
        if (i != id) {
            if (send(clientSockets[i], message, strlen(message), 0) < 0) {
                printf("Erro ao enviar mensagem para o cliente\n");
                threadArgs[id]->isConnected = 0;
            }
        }
    }
}

// Função para tratamento de um cliente individual
// Função para tratamento de um cliente individual
void ClientHandler(void* Args) {
    ThreadArgs* args = (ThreadArgs*)Args;
    SOCKET clientSocket = args->clientSocket;
    int id = args->id;
    char clientMessage[256];
    int isConnected = args->isConnected;

    while (1) {
        memset(clientMessage, 0, sizeof(clientMessage));
        if (recv(clientSocket, clientMessage, sizeof(clientMessage), 0) <= 0 && args->isConnected == 1) {
            printf("Cliente desconectado: %d\n", id);
            args->isConnected = 0;
        }
        else if (args->isConnected == 1) {
            char result [200];
            sprintf(result, "Cliente[%d]: %s", id, clientMessage);
            if (args->isConnected == 1) {
                BroadcastMessage(result, id);
            }
        }
    }

    closesocket(clientSocket);
    free(Args);
}



int main() {
    WSADATA wsaData;
    SOCKET serverSocket;
    struct sockaddr_in serverAddress, clientAddress;
    int addrlen = sizeof(clientAddress);

    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        printf("Erro ao inicializar o Winsock\n");
        return 1;
    }

    serverSocket = socket(AF_INET, SOCK_STREAM, 0);
    if (serverSocket == INVALID_SOCKET) {
        printf("Erro ao criar o socket\n");
        WSACleanup();
        return 1;
    }

    serverAddress.sin_family = AF_INET;
    serverAddress.sin_port = htons(PORT);
    serverAddress.sin_addr.s_addr = INADDR_ANY;

    if (bind(serverSocket, (struct sockaddr*)&serverAddress, sizeof(serverAddress)) == SOCKET_ERROR) {
        printf("Erro na associação do socket\n");
        closesocket(serverSocket);
        WSACleanup();
        return 1;
    }

    if (listen(serverSocket, SOMAXCONN) == SOCKET_ERROR) {
        printf("Erro na espera por conexões\n");
        closesocket(serverSocket);
        WSACleanup();
        return 1;
    }

    printf("Servidor aguardando conexões...\n");

    while (1) {
        SOCKET clientSocket = accept(serverSocket, (struct sockaddr*)&clientAddress, &addrlen);
        if (clientSocket == INVALID_SOCKET) {
            printf("Erro na aceitação da conexão\n");
            continue;
        }

        // Novo cliente conectado
        clientSockets[numClients] = clientSocket;
        ThreadArgs* threadArg = (ThreadArgs*)malloc(sizeof(ThreadArgs));
        threadArg->clientSocket = clientSocket;
        threadArg->id = numClients;
        threadArg->isConnected = 1; // Defina o status de conexão como conectado
        printf("Novo cliente conectado: %d\n", numClients);
        threadArgs[numClients] = threadArg;

        _beginthread(ClientHandler, 0, (void*)threadArg);
        numClients++;
    }

    closesocket(serverSocket);
    WSACleanup();

    return 0;
}
