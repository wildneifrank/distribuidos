# Projeto de Sistemas Distribuídos - Universidade Federal do Ceará

## Gateway de Comunicação para Objetos Inteligentes

Este projeto foi desenvolvido como parte do curso de Sistemas Distribuídos na Universidade Federal do Ceará. Foi elaborado por cinco alunos:

- Wildnei Frank
- Carlos Matheus
- Matheus Sá
- Gabriela Ponciano
- Bruna Stefanie

O objetivo principal deste projeto é criar um gateway de comunicação que se conecta com softwares de objetos inteligentes, permitindo a interação com sensores de temperatura, lâmpadas e condicionadores de ar.

## Descrição do Projeto

O gateway de comunicação é uma parte crucial de sistemas de Internet das Coisas (IoT) que permitem a interação entre dispositivos físicos e software. Neste projeto, o gateway foi desenvolvido para facilitar a comunicação entre diferentes tipos de dispositivos de objetos inteligentes.

O projeto inclui os seguintes componentes principais:

- **Sensor de Temperatura:** Este dispositivo monitora a temperatura ambiente e envia dados de temperatura para o gateway.

- **Lâmpada:** O gateway permite que os usuários controlem o estado da lâmpada, ligando ou desligando-a.

- **Condicionador de Ar:** O gateway também permite controlar o condicionador de ar, incluindo ligar/desligar e ajustar a temperatura desejada.

## Como Usar

Para utilizar o gateway e interagir com os dispositivos de objetos inteligentes, siga as instruções fornecidas nos respectivos códigos-fonte e execute os programas correspondentes.

**Para executar o projeto de Objetos Inteligentes, você precisará rodar os seguintes programas:**
- True_gateway.py
- lampada.py
- sensor.py
- ArCondicionado.py

## Projeto de Chat usando TCP

A primeira parte do trabalho consiste em implementar um Chat usando TCP. O Chat deve suportar múltiplos clientes e um servidor. Todos os clientes devem estar na mesma sala do chat (i.e., as mensagens enviadas por um cliente devem ser recebidas por todos os clientes). A sala do Chat deve suportar no máximo 4 pessoas conectadas. Comandos que o usuário (i.e., cliente) pode enviar:

- /ENTRAR: ao usar esse comando, ele é requisitado a digitar IP, porta do servidor e apelido que deseja usar no chat (não pode haver apelidos repetidos). O servidor deve aceitar a conexão ou negar (por já ter atingido o máximo de clientes conectados ou já haver alguém usando o mesmo apelido).
- Uma vez conectado, o cliente pode enviar mensagens para a sala do chat (todos devem receber, menos quem enviou);
- /USUARIOS: ao enviar esse comando, o cliente recebe a lista de usuários atualmente conectados ao chat;
- /NICK: com esse comando, o cliente pode trocar seu apelido. Todos os usuários conectados ao chat devem ser notificados da mudança.
- /SAIR: ao enviar esse comando, uma mensagem é enviada à sala do chat informando que o usuário está saindo e encerra a participação no chat.

É papel do servidor receber as requisições dos clientes e encaminhar as mensagens recebidas para todos eles. Descreva o formato para cada tipo de mensagem. Não pode usar comunicação em grupo.

## Pré-requisitos

Antes de executar o projeto, você precisará ter os seguintes pré-requisitos instalados:

- [Python](https://www.python.org/) (versão 3.10.12 ou superior)
- [Compilador C](https://gcc.gnu.org/) (para a parte do cliente em C)
- Bibliotecas Python adicionais, conforme especificado nos códigos-fonte
