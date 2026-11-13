# Exercício 9 — Tráfego DHCP

Arquivos neste diretório: `captura_dhcp.pcapng` e `captura_dhcp.png`.

## Como foi feito
1. Captura iniciada no Wireshark na interface Wi-Fi.
2. Execução de `ipconfig /release` (libera o IP) e depois `ipconfig /renew` (pede um novo).
3. Captura parada e filtro aplicado: `dhcp`.

## Resultados
- Release (pacote nº 5776): o cliente 192.168.1.8 devolveu o IP ao roteador 192.168.1.1
- Discover (nº 6431): origem 0.0.0.0, destino 255.255.255.255 (broadcast). Houve um Discover anterior (nº 6326), sem resposta
- Offer (nº 6454): servidor 192.168.1.1 ofereceu o IP 192.168.1.8
- Request (nº 6455): cliente aceitou a oferta
- Ack (nº 6462): IP concedido 192.168.1.8, tempo de concessão (lease) de 86400 s (24 horas)

## Descrição
Depois do release, o computador ficou sem IP e iniciou uma nova negociação DHCP. A captura mostra as quatro
mensagens do processo DORA: o Discover foi enviado em broadcast (de 0.0.0.0 para 255.255.255.255) porque o
cliente ainda não tinha endereço; o roteador 192.168.1.1 respondeu com um Offer do IP 192.168.1.8; o cliente
confirmou com um Request e o servidor finalizou com um ACK, concedendo o IP por 24 horas, com máscara
255.255.255.0, gateway 192.168.1.1 e DNS 177.74.225.22. Houve duas mensagens Discover, pois a primeira
não obteve resposta e o cliente tentou novamente.