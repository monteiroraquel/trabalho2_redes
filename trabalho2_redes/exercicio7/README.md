
# Exercício 7 — Resolução de nomes via DNS

Arquivos neste diretório: `captura_dns.pcapng`, `captura_dns_queries.png` e `captura_dns_answers.png`.

## Como foi feito
1. Captura iniciada no Wireshark na interface Wi-Fi.
2. Acesso a `www.google.com` no navegador.
3. Captura parada e filtro aplicado: `dns`.

## Resultados
- Tipos de registro consultados: A (IPv4) e HTTPS (tipo 65), enviados em pares para cada nome
- Servidor DNS utilizado: 177.74.224.29 (porta 53/UDP)
- Registros retornados para www.google.com (consulta nº 2339, resposta nº 2346): 8 registros A:
  142.251.150.119, .151.119, .152.119, .153.119, .154.119, .155.119, .156.119 e .157.119
- Tempo de resposta: 4,86 ms

## Descrição
Ao acessar www.google.com, o computador (192.168.1.8) enviou consultas DNS ao servidor 177.74.224.29.
Para cada nome o navegador fez duas consultas ao mesmo tempo, uma do tipo A e outra do tipo HTTPS, e cada
uma recebeu uma resposta com o mesmo identificador da consulta (por exemplo, 0xd74e). A consulta A de
www.google.com retornou oito endereços IPv4 sem erro, em cerca de 4,9 ms. Também apareceram consultas para
domínios auxiliares do Google, como fonts.gstatic.com e accounts.google.com.
