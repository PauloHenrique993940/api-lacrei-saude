# Deploy e rollback

## Objetivo

Cada release deve usar uma imagem Docker imutável identificada pelo SHA do commit. A versão nova é iniciada como uma segunda unidade, validada por health check e promovida somente depois da validação.

## Fluxo blue/green com Docker Compose

No servidor de deploy, defina a versão que será promovida:

```bash
export IMAGE_TAG=<sha-do-commit>
export COMPOSE_PROJECT_NAME=lacrei-green
```

Construa a imagem da nova versão e suba o serviço com o banco já disponível:

```bash
docker compose build web
docker compose up -d --no-build web
```

Valide a aplicação antes de trocar o tráfego:

```bash
curl --fail http://localhost:8000/
curl --fail \
  -H "X-API-KEY: ${API_KEY}" \
  http://localhost:8000/api/v1/professionals/
```

Depois da validação, direcione o proxy ou load balancer para a nova unidade. A unidade anterior permanece disponível durante a janela de observação.

## Rollback

Mantenha a tag da versão anterior, por exemplo `PREVIOUS_IMAGE_TAG`. Em caso de erro, suba novamente a versão estável:

```bash
export IMAGE_TAG=${PREVIOUS_IMAGE_TAG}
docker compose up -d --no-build web
curl --fail http://localhost:8000/
```

Após confirmar a recuperação, remova a unidade que apresentou problema:

```bash
docker compose down
```

Em AWS ECS, o mesmo fluxo deve ser aplicado criando uma nova task definition para cada tag, deslocando o tráfego pelo target group e restaurando a task definition anterior no rollback.

## Revert no GitHub Actions

O workflow aceita execução manual pelo GitHub Actions. Para um revert de código, crie um commit que reverta a release problemática e faça push para `main`. O pipeline executará lint, testes e build novamente antes da promoção.

Para um rollback de infraestrutura sem alterar o código, use a tag anterior da imagem e execute o procedimento acima. As etapas de deploy do workflow ainda dependem das credenciais e do provedor escolhidos para o ambiente.

## Critérios de sucesso

- health check HTTP retorna `2xx`;
- endpoint protegido responde com a API key correta;
- logs não apresentam erros de inicialização;
- tráfego retorna à versão anterior em caso de falha;
- banco de dados permanece em volume persistente.
