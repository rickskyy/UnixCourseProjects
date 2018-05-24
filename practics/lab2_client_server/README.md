# Lab 2 Client-Server

## Task 7
Сервер доступу. Клієнт при вході у зв’язок із сервером передає своє ім’я та пароль. 
Якщо зроблено три спроби передачі, а правильний пароль не отримано, то сервер блокує IP-адресу клієнта на 5 хвилин.

### Requirements
    - python 3

### Running
server: `python simple_auth_server.py [port] [username:password]`

client: `python client.py`

