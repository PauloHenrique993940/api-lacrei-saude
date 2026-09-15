# Lacrei Saúde API

API RESTful para gestão de profissionais da saúde e consultas médicas, com foco em segurança, validação de dados, documentação automática e prontidão para evolução em produção.

## Visão geral

Este projeto foi desenvolvido para apoiar a organização de profissionais de saúde e agendamentos, com uma API segura, documentação acessível e rotas preparadas para uso real em ambientes internos e de produção.

Além da API, a aplicação expõe uma página inicial em `/` com identidade visual inspirada na Lacrei Saúde e acesso rápido aos endpoints e à documentação.

## Stack

- Python 3.12
- Django 5
- Django REST Framework
- PostgreSQL
- SQLite (para desenvolvimento local)
- Docker / Docker Compose
- Poetry
- GitHub Actions

## Requisitos

- Python 3.12
- Poetry
- Docker (opcional, para ambiente em container)

## Como executar localmente

O projeto usa SQLite por padrão em ambiente local para facilitar o desenvolvimento sem depender de um banco PostgreSQL instalado na máquina. Para usar PostgreSQL, configure as variáveis do arquivo `.env` conforme o exemplo. O arquivo `.env.example` deve ser copiado para `.env` antes da primeira execução.

```bash
poetry env use 3.12
poetry install
poetry run python manage.py migrate
poetry run python manage.py runserver 0.0.0.0:8000
```

No PowerShell, copie o arquivo de ambiente com:

```powershell
Copy-Item .env.example .env
```

Importante: para acessar no navegador, use `http://localhost:8000`, e não `http://0.0.0.0:8000`.

## Acesso rápido

- Página inicial: `http://localhost:8000/`
- Documentação Swagger: `http://localhost:8000/api/docs/`
- Schema OpenAPI: `http://localhost:8000/api/schema/`

A página inicial também possui um painel de teste. Informe a API key no campo indicado e use os botões para consultar profissionais ou consultas diretamente pela interface. Em desenvolvimento, a chave padrão é `lacrei-dev-key`.

Para consultar profissionais pelo navegador, use o Swagger e informe `lacrei-dev-key` em `Authorize`. O endpoint `/api/v1/professionals/` é protegido e não pode ser aberto diretamente como um link comum sem o header de autenticação.

## Autenticação

As rotas de recursos da API exigem autenticação por header `X-API-KEY` ou `Api-Key`. A página inicial, o schema e o Swagger continuam acessíveis para facilitar a exploração local.

Exemplo:

```bash
curl -H "X-API-KEY: lacrei-dev-key" http://localhost:8000/api/v1/professionals/
```

## Endpoints principais

Base da API: `/api/v1`

As rotas em `/api/` também são mantidas como compatibilidade, mas `/api/v1/` é a base recomendada para novos clientes.

- `GET /api/v1/professionals/` — listar profissionais
- `POST /api/v1/professionals/` — criar profissional
- `GET /api/v1/professionals/<id>/` — detalhar profissional
- `PATCH /api/v1/professionals/<id>/` — atualizar profissional
- `DELETE /api/v1/professionals/<id>/` — remover profissional
- `GET /api/v1/appointments/` — listar consultas
- `POST /api/v1/appointments/` — criar consulta
- `GET /api/v1/appointments/<id>/` — detalhar consulta
- `PATCH /api/v1/appointments/<id>/` — atualizar consulta
- `DELETE /api/v1/appointments/<id>/` — remover consulta
- `GET /api/v1/professionals/<professional_id>/appointments/` — consultas por profissional

## Estrutura de dados

### Profissional

Campos principais:

- nome_social
- profissao
- endereco
- contato

### Consulta

Campos principais:

- data
- profissional

O campo `data` é um `DateTimeField` e deve ser enviado em formato ISO 8601, por exemplo: `2026-09-20T14:30:00Z`.

Os campos `created_at` e `updated_at` são gerados automaticamente pela API.

## Exemplos de requisição

Criar profissional:

```bash
curl -X POST http://localhost:8000/api/v1/professionals/ \
	-H "Content-Type: application/json" \
	-H "X-API-KEY: lacrei-dev-key" \
	-d '{"nome_social":"João Silva","profissao":"Cardiologista","endereco":"Rua A, 100","contato":"(11) 99999-9999"}'
```

Criar consulta:

```bash
curl -X POST http://localhost:8000/api/v1/appointments/ \
	-H "Content-Type: application/json" \
	-H "X-API-KEY: lacrei-dev-key" \
	-d '{"data":"2026-09-20T14:30:00Z","profissional":1}'
```

## Respostas e erros

- `200` ou `201` — leitura ou criação concluída
- `204` — exclusão concluída
- `400` — payload inválido ou campo obrigatório ausente
- `403` — API key ausente ou inválida
- `404` — recurso ou profissional sem consultas encontrado

As respostas são JSON, exceto a interface inicial e a documentação Swagger.

## Testes

```bash
poetry run python manage.py test
```

Cobertura atual:

- CRUD de profissionais
- CRUD de consultas
- listagem por profissional
- validação de payloads inválidos
- autenticação e autorização

## Docker

```bash
docker compose up --build
```

Aplicação disponível em:

- API: `http://localhost:8000`
- PostgreSQL: `localhost:5432`

O `docker-compose.yml` inicia a API e o PostgreSQL. A imagem executa as migrações antes de iniciar o servidor.

## Variáveis de ambiente

As principais configurações são:

- `USE_SQLITE=True` — banco local padrão
- `USE_SQLITE=False` — usa PostgreSQL
- `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST` e `POSTGRES_PORT` — conexão PostgreSQL
- `SECRET_KEY` — chave secreta do Django
- `API_KEY` — chave exigida pelas rotas protegidas
- `ALLOWED_HOSTS` — hosts aceitos pela aplicação
- `DEBUG` — deve ser `False` em produção

## CI/CD

O workflow em `.github/workflows/ci-cd.yml` executa:

- lint
- testes automatizados
- build da imagem Docker

As etapas de deploy para staging e produção estão preparadas como pontos de integração e ainda usam comandos placeholder. Para ativá-las, é necessário configurar credenciais, registry e infraestrutura do provedor escolhido.

O fluxo de promoção blue/green, health check e rollback por tag está descrito em [docs/rollback.md](docs/rollback.md). A execução manual do workflow também pode ser iniciada pela opção **Run workflow** no GitHub Actions.

## Decisões técnicas

- Django + DRF para construção rápida e segura de APIs REST
- SQLite como banco local para desenvolvimento e testes
- PostgreSQL para produção e ambientes com maior exigência de persistência
- autenticação por API key para integrações simples e controladas
- DRF Spectacular para documentação interativa
- CORS e logs configurados para observabilidade e integração

## Proposta Assas

A proposta de integração com Assas está detalhada em [docs/assas.md](docs/assas.md). O fluxo contempla:

- cobrança de consultas e agendamentos
- webhook de confirmação de pagamento
- acompanhamento de status e reembolso
- payload com profissional, paciente, valor e referência externa

## Observações finais

O projeto está funcional, documentado e pronto para uso local com autenticação e validações. A aplicação inclui uma página inicial de apresentação, painel de testes, documentação interativa da API e endpoints versionados para facilitar manutenção e evolução futura. Antes de produção, configure `DEBUG=False`, uma `SECRET_KEY` segura, uma `API_KEY` forte, `ALLOWED_HOSTS` restrito e um deploy real no pipeline.
