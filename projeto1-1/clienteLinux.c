#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <pthread.h>

#define PORT 8922

int clientSocket;
char user[256];

void *SendMessageThread(void *arg) {
    printf("Digite o nick desejado: ");
    scanf("%s", user);
    if (send(clientSocket, user, strlen(user), 0) < 0) {
        printf("Erro ao enviar dados ao servidor\n");
        pthread_exit(NULL);
    }

    while (1) {
        char message[256];
        fgets(message, sizeof(message), stdin);
        if (send(clientSocket, message, strlen(message), 0) < 0) {
            printf("Erro ao enviar dados ao servidor\n");
            break;
        }
    }
    pthread_exit(NULL);
}


void *ReceiveMessageThread(void *arg) {
    while (1) {
        char buffer[1024];
        memset(buffer, 0, sizeof(buffer));
        int bytesReceived = recv(clientSocket, buffer, sizeof(buffer), 0);

        if (bytesReceived < 0) {
            printf("Erro ao receber dados do servidor\n");
            close(clientSocket);
            exit(1);
        } else if (bytesReceived == 0) {
            printf("Servidor encerrou a conexão\n");
            close(clientSocket);
            exit(1);
        } else if (strcmp(buffer, "code:0") == 0) {
            printf("Nome de usuário já em uso. Por favor, escolha outro nome.\n");
            close(clientSocket);
            exit(1);
        }

        printf("%s\n", buffer);
    }
}

int main() {
    char ip[40];
    printf("Digite o IP do server desejado: ");
    scanf("%s", ip);

    int namePort; 
    printf("Digite a porta do server desejado: ");
    scanf("%d", &namePort);

    clientSocket = socket(AF_INET6, SOCK_STREAM, 0);
    if (clientSocket == -1) {
        printf("Erro ao criar o socket\n");
        return 1;
    }

    struct sockaddr_in6 serverAddress;
    memset(&serverAddress, 0, sizeof(serverAddress));
    serverAddress.sin6_family = AF_INET6;
    serverAddress.sin6_port = htons(namePort); 
    inet_pton(AF_INET6, ip, &(serverAddress.sin6_addr));

    // Conectar ao servidor
    if (connect(clientSocket, (struct sockaddr*)&serverAddress, sizeof(serverAddress)) < 0) {
        printf("Erro ao conectar ao servidor\n");
        close(clientSocket);
        return 1;
    }

    // Criar threads para envio e recebimento de mensagens
    pthread_t sendThread, receiveThread;
    pthread_create(&sendThread, NULL, SendMessageThread, NULL);
    pthread_create(&receiveThread, NULL, ReceiveMessageThread, NULL);

    // Aguardar pelo término das threads
    pthread_join(sendThread, NULL);
    pthread_join(receiveThread, NULL);

    // Fechar o socket
    close(clientSocket);

    return 0;
}
