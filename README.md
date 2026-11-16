### Jogo de turno

###### Nomes

Davi Honorio Cardoso Bottegga (1280279)

João Mateus Ferreira Martins (1935185)

João Pedro de Oliveira Valentim (1473466)

###### Email

davi.honorio@unisantos.br

joaomartins@unisantos.br

jpvalentim@unisantos.br

###### Descrição

O objetivo do projeto Coliseu é desenvolver um RPG de combate em turnos em Python, com interface gráfica em Pygame,
utilizando os princípios da Programação Orientada a Objetos (POO) para criar classes, raças, equipamentos, técnicas, 
magias e itens, ou seja, sendo estruturado com classes abstratas, heranças, polimorfismo e encapsulamentos. Dessa 
forma, o projeto é dividido em vários arquivos para melhor organização e serapação de responsabilidades. Ele conta
também com um arquivo 'test_jogo.py' para testar possíveis mecânicas com praticidade usando Pytest e método de 
salvamento e carregamento de saves utilizando JSON.

###### Execução

#### Pré-requisitos
Python 3.10+ instalado
Bibliotecas necessárias: 'Pygame', 'Pytest'

### 1. Clonar ou baixar o repositório main.py
### 2. Configurar o ambiente virtual (opcional)
**Criar o ambiente virtual:** python -m venv venv
**Ativar o ambiente (Windows):** venv\Scripts\activate
**Ativar o ambiente (MacOS/Linux):** source venv/bin/activate
### 3. Na pasta do projeto instale as dependências do arquivo 'requirements.txt': 
pip install -r requirements.txt
### 4. Para rodar o jogo execute 'arena.py'
### 5. Para testar o 'test_jogo.py' execute 'Pytest' no terminal

###### **Idéias**

###### PARA FAZER

Desenvolver a lógica para buff e debuff

Last stand vida = 1
Você tem 50% de chance de matar o inimigo independente da vida dele ao ter 1HP

Quando ficar com HP < 10% ter uma chance de liberar fúria
Item que desbloqueia mana para o player

Talvez um atributo carisma, pois o loot após batalha vai ser aleatorizado já que a platéia que vai
dar os itens ou não (chance de ganhar algo ou de n ganhar, e afetar a qualidade do item caso ganhe)
