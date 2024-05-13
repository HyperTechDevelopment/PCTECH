# PCTECH

## Descrição do Projeto
PCTECH é um sistema web desenvolvido em Python utilizando o framework Flask, destinado ao gerenciamento de reparo de equipamentos de TI. O sistema permite o login de usuários, cadastro e edição de usuários, cadastro e consulta de reparos, visualização de histórico de reparos, e impressão de comprovantes.

## Funcionalidades Principais
- **Login**
- **Cadastro de Usuários**
- **Edição de Usuários**
- **Cadastro de Reparo**
- **Consulta de Reparo**
- **Histórico de Reparos**
- **Impressão de Comprovante**

## Como Executar

### Pré-requisitos
- Python 3.x
- Flask
- Flask-SQLAlchemy
- Flask-Login
- psycopg2-binary
- uuid
- reportlab

### Instalação

1. Clone o repositório:
    ```bash
    git clone https://github.com/seu-usuario/pctech.git
    cd pctech
    ```

2. Crie um ambiente virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\\Scripts\\activate
    ```

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

4. Configure o banco de dados:
    - O sistema utiliza SQLite, que não requer configuração adicional.

5. Inicie a aplicação:
    ```bash
    flask run
    ```

6. Acesse o sistema no navegador:
    http://127.0.0.1:5000

## Dependências
As dependências do projeto estão listadas no arquivo `requirements.txt` e incluem:
- Flask
- Flask-SQLAlchemy
- Flask-Login
- psycopg2-binary
- uuid
- reportlab

## Autores
HyperTech
"""