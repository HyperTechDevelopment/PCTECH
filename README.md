# PCTECH
![background_with_text](https://github.com/HyperTechDevelopment/PCTECH/assets/155833544/de29fc6d-4c10-4c79-a202-0bab8cc0231c)

## Descrição do Projeto
PCTECH é um sistema web desenvolvido em Python utilizando o framework Flask, destinado ao gerenciamento de reparo de equipamentos de TI. O sistema permite o login de usuários, cadastro e edição de usuários, cadastro e consulta de reparos, visualização de histórico de reparos, e impressão de comprovantes.

## Funcionalidades Principais
- **Login**
- **Cadastro de Usuários**
- **Edição de Usuários**
- **Cadastro de Reparo**
- **Histórico de Reparos**
- **Impressão de Comprovante**

## Tela de Login (lembre-se de inserir a logo da sua empresa no header):
![image](https://github.com/HyperTechDevelopment/PCTECH/assets/155833544/cc034b35-eb3a-4a40-b031-e31715d5b5b1)

## Página de Administrador:
![image](https://github.com/HyperTechDevelopment/PCTECH/assets/155833544/b20a48af-0d0c-4c37-9587-b187b8d6a051)

## Página de Técnico:
![image](https://github.com/HyperTechDevelopment/PCTECH/assets/155833544/6af0cc09-5c06-4c21-bf23-b82776ce1bbf)

## Cadastro de Reparo:
![image](https://github.com/HyperTechDevelopment/PCTECH/assets/155833544/cb82d815-516e-40b7-a4f9-e5715767559a)

## Histórico de Reparos:
![image](https://github.com/HyperTechDevelopment/PCTECH/assets/155833544/fb09a3e2-fada-435c-9332-be84766516ce)



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

7. Se optar por hospedar em um servidor, será necessário configurá-lo para tal, através do NGINX ou APACHE.

## Dependências
As dependências do projeto estão listadas no arquivo `requirements.txt` e incluem:
- Flask
- Flask-SQLAlchemy
- Flask-Login
- psycopg2-binary
- uuid
- reportlab

Sistema foi desenvolvido especificamente para uma equipe de T.I nas empresas.

## Autores
HyperTech
"""
