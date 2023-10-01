#include <stdio.h>
#include <winsock2.h>
#include <ws2tcpip.h>
#include <stdlib.h>
#include <string.h>
#include <process.h>

#pragma comment(lib, "ws2_32.lib")

SOCKET clientSocket;
char user[256];

// Função para envio de mensagens
void SendMessageThread() {
    // Enviar dados ao servidor
    printf("Digite o nick desejado: ");
    scanf("%s", user);
    if (send(clientSocket, user, strlen(user), 0) < 0) {
        printf("Erro ao enviar dados ao servidor\n");
    }
    while (1) {
        // Enviar dados ao servidor
        char message[256];
        fgets(message, sizeof(message), stdin);
        if (send(clientSocket, message, strlen(message), 0) < 0) {
            printf("Erro ao enviar dados ao servidor\n");
            break;
        }
    }
}

// Função para recebimento de mensagens
void ReceiveMessageThread() {
    while (1) {
        // Receber resposta do servidor
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
    char ip[40];  // O tamanho aumentou para acomodar endereços IPv6
    printf("Digite o IP do server desejado: ");
    scanf("%s", ip);

    int PORT;
    printf("Digite a porta do server desejado: ");
    scanf("%d", &PORT);

    // Criar o socket
    clientSocket = socket(AF_INET6, SOCK_STREAM, 0);  // Usamos AF_INET6 para IPv6
    if (clientSocket == INVALID_SOCKET) {
        printf("Erro ao criar o socket\n");
        WSACleanup();
        return 1;
    }

    // Definir o endereço do servidor
    struct sockaddr_in6 serverAddress;  // Usamos sockaddr_in6 para IPv6
    memset(&serverAddress, 0, sizeof(serverAddress));  // Inicializamos a estrutura com zeros
    serverAddress.sin6_family = AF_INET6;
    serverAddress.sin6_port = htons(PORT);
    inet_pton(AF_INET6, ip, &(serverAddress.sin6_addr));  // Convertemos o endereço IPv6 de texto para binário

    // Conectar ao servidor
    if (connect(clientSocket, (struct sockaddr*)&serverAddress, sizeof(serverAddress)) < 0) {
        printf("Erro ao conectar ao servidor\n");
        closesocket(clientSocket);
        WSACleanup();
        return 1;
    }

    // Criar threads para envio e recebimento de mensagens
    _beginthread(SendMessageThread, 0, NULL);
    _beginthread(ReceiveMessageThread, 0, NULL);

    // Aguardar pelo término das threads
    while (1) {
        // Espera infinita
    }

    // Fechar o socket e finalizar o Winsock
    closesocket(clientSocket);
    WSACleanup();

    return 0;
}
