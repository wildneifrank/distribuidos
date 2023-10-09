#include <stdio.h>
#include <winsock2.h>
#include <stdlib.h>
#include <string.h>
#include <process.h>

#pragma comment(lib, "ws2_32.lib")
SOCKET clientSocket;
char user[256];

void SendMessageThread() {
    printf("Digite o nick desejado: ");
    scanf("%s", user);
        if (send(clientSocket, user, strlen(user), 0) < 0) {
            printf("Erro ao enviar dados ao servidor\n");
        }
    while (1) {
        char message[256];
        fgets(message, sizeof(message), stdin);
        if (send(clientSocket, message, strlen(message), 0) < 0) {
            printf("Erro ao enviar dados ao servidor\n");
            break;
        }
    }
}

void ReceiveMessageThread() {
    while (1) {
        char buffer[1024];
        memset(buffer, 0, sizeof(buffer));
        int bytesReceived = recv(clientSocket, buffer, sizeof(buffer), 0);
        
        if (bytesReceived < 0) {
            printf("Erro ao receber dados do servidor\n");
            closesocket(clientSocket);
            WSACleanup();
            exit(0);
        } else if (bytesReceived == 0) {
            printf("Servidor encerrou a conexão\n");
            closesocket(clientSocket);
            WSACleanup();
            exit(0);
        } else if (strcmp(buffer, "code:0") == 0) {
            printf("Nome de usuário já em uso. Por favor, escolha outro nome.\n");
            closesocket(clientSocket);
            WSACleanup();
            exit(0);
        }
                
        printf("%s\n", buffer);
    }
}


int main() {
    WSADATA wsaData;
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        printf("Erro ao inicializar o Winsock\n");
        return 1;
    }
    char ip[20];
    printf("Digite o ip do server desejado: ");
    scanf("%s", ip);
    char ip2[20] = "127.0.0.1";
    ip[strcspn(ip, "\n")] = '\0'; 

    int PORT;
    printf("Digite a porta do server desejado: ");
    scanf("%d", &PORT);
    PORT = 8922;

    // Criar o socket
    clientSocket = socket(AF_INET, SOCK_STREAM, 0);
    if (clientSocket == INVALID_SOCKET) {
        printf("Erro ao criar o socket\n");
        WSACleanup();
        return 1;
    }

    // Definir o endereço do servidor
    struct sockaddr_in serverAddress;
    serverAddress.sin_family = AF_INET;
    serverAddress.sin_port = htons(PORT);
    serverAddress.sin_addr.s_addr = inet_addr(ip2);  // Coloque o IP do servidor aqui

    // Conectar ao servidor
    if (connect(clientSocket, (struct sockaddr*)&serverAddress, sizeof(serverAddress)) < 0) {
        printf("Erro ao conectar ao servidor\n");
        closesocket(clientSocket);
        WSACleanup();
        return 1;
    }

    _beginthread(SendMessageThread, 0, NULL);
    _beginthread(ReceiveMessageThread, 0, NULL);


    while (1) {

    }

    closesocket(clientSocket);
    WSACleanup();

    return 0;
}
