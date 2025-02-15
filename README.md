# API de Geração Automática de Provas Personalizadas

### Repositório para o projeto final da disciplina de Construção de APIs para Inteligência Artificial da Especialização em Sistemas e Agentes Inteligentes UFG.

<p align="center">
  <a href="https://shields.io/">
    <img src="https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow" alt="Status do Projeto">
  </a>
  <a href="https://opensource.org/licenses/MIT">
    <img src="https://img.shields.io/badge/Licença-MIT-green" alt="Licença">
  </a>
</p>

Esta API RESTful, construída com Django REST Framework e Python, permite a criação de provas personalizadas com base em critérios como tema, nível de dificuldade (usando a Taxonomia de Bloom Revisada) e formato das questões. A geração das questões é feita utilizando a API do Groq, que fornece acesso a modelos de linguagem de grande escala (LLMs).

## ✨ Funcionalidades

*   **Geração de Questões:** Cria questões de múltipla escolha, dissertativas e verdadeiro/falso com base nos critérios especificados.
*   **Personalização de Provas:** Permite a criação de provas com diferentes temas, níveis de dificuldade e formatos de questões.
*   **Gabarito Automático:** Gera automaticamente o gabarito para cada prova criada.
*   **Integração com LLM (Groq):** Utiliza a API do Groq para gerar questões de alta qualidade.
*   **Autenticação JWT:** Protege a API com autenticação usando JSON Web Tokens (JWT).
*   **Documentação Interativa (Swagger/Redoc):** Fornece documentação completa e interativa da API, permitindo testar os endpoints diretamente no navegador.
*   **Testes Automatizados:** Inclui testes unitários e de integração para garantir a qualidade do código e o funcionamento correto da API.


## 🛠️ Tecnologias Utilizadas

*   **Linguagem:** Python 3.12.6
*   **Framework Web:** Django 4+
*   **Framework API:** Django REST Framework (DRF)
*   **Autenticação:** djangorestframework-simplejwt (JWT)
*   **Documentação:** drf-yasg (Swagger/Redoc)
*   **LLM:** Groq API
*   **Banco de Dados (Desenvolvimento):** SQLite
*   **Banco de Dados (Produção):** SQLite
*   **Testes:** unittest, mock
*   **Versionamento:** Git
*   **Outros:** requests, python-dotenv

## ⚙️ Pré-requisitos

*   **Python 3.12.6** ( *exatamente* esta versão)
*   pip
*   virtualenv
*   Git
*   Chave de API do Groq

## 🚀 Instalação e Execução (Local)

1.  **Clone o Repositório:**

    ```bash
    git clone <URL_DO_SEU_REPOSITORIO>
    cd <NOME_DA_PASTA_DO_PROJETO>
    ```

2.  **Crie e Ative o Ambiente Virtual (com Python 3.12.6):**

    ```bash
    python3.12 -m venv venv  # Use python3.12
    venv\Scripts\activate  # No Windows
    # source venv/bin/activate # No Linux/macOS
    ```

3.  **Instale as Dependências:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Crie o Arquivo `.env`:**

    *   Crie um arquivo `.env` na raiz do projeto.
    *   Adicione as seguintes variáveis (substituindo pelos seus valores):

        ```
        DJANGO_SETTINGS_MODULE=geradorprovas.settings
        SECRET_KEY=<SUA_SECRET_KEY_GERADA>
        GROQ_API_KEY=<SUA_CHAVE_API_DO_GROQ>
        ```

5.  **Execute as Migrações:**

    ```bash
    python manage.py makemigrations  # Use python, pois manage.py chama o interpretador configurado no ambiente virtual.
    python manage.py migrate
    ```

6.  **Crie um Superusuário:**

    ```bash
    python manage.py createsuperuser
    ```

7.  **Execute o Servidor de Desenvolvimento:**

    ```bash
    python manage.py runserver
    ```

8.  **Acesse a API:**

    *   A API estará disponível em `http://localhost:8000/`.
    *   A documentação (Swagger UI) estará disponível em `http://localhost:8000/swagger/`.
    *   A documentação (Redoc) estará disponível em `http://localhost:8000/redoc/`.

## 🧪 Testes

Para executar os testes:

```bash
python manage.py test
```
## 🗺️ Endpoints

| Método | Endpoint                      | Descrição                                                                                                                                                              |
| :----- | :---------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| POST   | `/api/gerar-prova/`          | Cria uma nova prova com base nos critérios fornecidos (tema, dificuldade, quantidade de questões, tipos de questões). Usa a API do Groq para gerar as questões.           |
| GET    | `/api/provas/{id}/`           | Retorna os detalhes de uma prova específica (incluindo as questões).                                                                                                          |
| GET    | `/api/gabarito/{prova__id}/` | Retorna o gabarito de uma prova específica.                                                                                                                                  |
| POST   | `/api/token/`               | Recebe o nome de usuário e a senha, e retorna um *access token* JWT e um *refresh token* JWT.                                                                               |
| POST   | `/api/token/refresh/`          | Recebe um *refresh token* JWT e retorna um novo *access token* JWT.                                                                                                          |

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir *issues* (para relatar problemas, sugerir melhorias, etc.) e *pull requests* (para enviar suas próprias contribuições de código).  Antes de enviar um *pull request*, por favor, discuta a alteração proposta em uma *issue*.

## 📝 Licença

Este projeto está licenciado sob a licença MIT - consulte o arquivo [LICENSE](LICENSE) para obter detalhes.  A licença MIT é uma licença permissiva de código aberto, que permite o uso, modificação e distribuição do código, inclusive para fins comerciais.
