# 🧠 Data Translator API

API REST desenvolvida em **FastAPI** com banco de dados **Supabase (PostgreSQL)**, responsável pela camada de persistência do sistema de self-service de dados via chat.

Esta API é o núcleo do Back-end do projeto **Self-Data**, permitindo salvar e recuperar os Dicionários de Dados gerados no processo de "Batismo" — onde tabelas técnicas como `TB_FAT_001` são mapeadas para nomes amigáveis como `Vendas Totais`.

---

## 🏗️ Arquitetura do Projeto

Usuário (Chat)
↓
Front-end (Next.js) ──► Back-end (Esta API) ──► Supabase (PostgreSQL)
↓
AI Engineer (LangChain)
↓
Data Engineer (PySpark)
↓
Relatório Excel por E-mail



---

## 🚀 Stack

| Tecnologia | Uso |
|---|---|
| Python 3.13 | Linguagem principal |
| FastAPI | Framework da API REST |
| Supabase | Banco de dados PostgreSQL na nuvem |
| Pydantic | Validação de dados |
| Docker | Containerização |

---

## 📁 Estrutura de Arquivos

self_data/
├── main.py # Código principal da API
├── requirements.txt # Dependências do projeto
├── Dockerfile # Receita do container
├── docker-compose.yml # Orquestrador do container
├── .env # Credenciais (não vai pro GitHub)
└── .gitignore # Arquivos ignorados pelo Git

---

## ⚙️ Pré-requisitos

- [Python 3.13+](https://www.python.org/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Conta no [Supabase](https://supabase.com/)

---

## 🗄️ Configuração do Banco de Dados

No painel do Supabase, acesse **SQL Editor** e execute:

```sql
-- Tabela que guarda os Dicionários de cada cliente
CREATE TABLE app_metadata (
    id         UUID        DEFAULT uuid_generate_v4() PRIMARY KEY,
    client_id          NOT NULL,
    dictionary JSONB       NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabela que guarda os Logs de cada operação
CREATE TABLE operation_logs (
    id        UUID        DEFAULT uuid_generate_v4() PRIMARY KEY,
    action            NOT NULL,
    user_id           NOT NULL,
    timestamp TIMESTAMPTZ DEFAULT NOW()
);
```
🔧 Instalação e Execução
1. Clone o repositório
bash
git clone https://github.com/seu-usuario/self-data.git
cd self-data
2. Configure as variáveis de ambiente
Crie um arquivo .env na raiz do projeto:


SUPABASE_URL=https://xxxxxxxxxxxxxxxx.supabase.co
SUPABASE_KEY=sua_secret_key_aqui
3. Suba com Docker
bash
docker compose up --build
4. Acesse a documentação interativa

http://localhost:8000/docs
📡 Endpoints
POST /save-dictionary
Salva o Dicionário de Dados de um cliente no banco.

Body:

json
{
  "client_id": "cliente-001",
  "user": "nicolas",
  "dictionary_data": {
    "TB_FAT_001": "Vendas Totais",
    "CD_FIL_02": "Filial",
    "DT_VND": "Data da Venda"
  }
}
Resposta:

json
{
  "status": "success",
  "message": "Dictionary saved and logged successfully"
}
GET /get-dictionary/{client_id}
Busca o Dicionário mais recente de um cliente.

Exemplo:

GET /get-dictionary/cliente-001
Resposta:

json
{
  "client_id": "cliente-001",
  "dictionary_data": {
    "TB_FAT_001": "Vendas Totais",
    "CD_FIL_02": "Filial",
    "DT_VND": "Data da Venda"
  }
}
🛑 Comandos úteis
bash
# Subir o container
docker compose up --build

# Subir em background (sem travar o terminal)
docker compose up -d --build

# Parar o container
docker compose down

# Ver logs em tempo real
docker compose logs -f

👤 Autor
Nicolas — Back-end Engineer
Projeto: Self-Data — Democratizando o acesso a dados via chat
