# Proposta de integração com Assas

## Objetivo

Permitir cobrança e acompanhamento financeiro de agendamentos e consultas, com um fluxo simples e rastreável para integrações futuras com o sistema da Lacrei Saúde.

## Fluxo sugerido

1. O usuário agenda uma consulta pela API.
2. A aplicação cria uma cobrança de pagamento no Assas.
3. O Assas responde com identificador da cobrança, valor e status.
4. O sistema registra a referência da cobrança em uma tabela de pagamentos.
5. Um webhook do Assas atualiza o status da cobrança e pode disparar notificação para o paciente ou para o time operacional.

## Campos sugeridos

- id_consulta
- id_profissional
- id_paciente
- valor
- status_pagamento
- data_vencimento
- descricao
- referencia_externa

## Exemplos de endpoints

- `POST /api/v1/payments/` — criar cobrança
- `GET /api/v1/payments/<id>/` — consultar status
- `POST /api/v1/payments/webhook/` — receber evento do Assas

## Observações de arquitetura

- separar o serviço financeiro do serviço de agendamento
- persistir logs de cobrança e falhas
- processar webhooks com validação de assinatura
- adicionar retry e fila para eventos não processados

## Benefícios

- melhora na gestão financeira
- redução de acoplamento entre API de agendamento e processamento de pagamento
- escalabilidade para novos modelos de cobrança
