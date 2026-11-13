# Exercício 5 — Tráfego HTTP

Arquivos neste diretório: `captura_http.pcapng`, `captura_http.png` (requisição GET) e
`captura_http_resposta.png` (resposta 200 OK).

## Como foi feito
1. Captura iniciada no Wireshark na interface Wi-Fi.
2. Acesso a `http://neverssl.com` no navegador (site sem HTTPS, por isso os cabeçalhos aparecem em texto).
3. Captura parada e filtro aplicado: `http`.

## Resultados
- Método da requisição: GET
- URL acessada: http://neverssl.com/
- Código de status: 200 OK
- Content-Type: text/html
- Server: Apache/2.4.68

## Descrição
Foi capturado o acesso a http://neverssl.com. O filtro `http` mostrou dois pacotes: a requisição
(pacote 4439), que usou o método GET para o recurso "/" com o cabeçalho Host: neverssl.com, e a resposta
(pacote 5708), com código 200 OK, Content-Type text/html e Server Apache/2.4.68. Como o HTTP não é
criptografado, todos os cabeçalhos aparecem legíveis. A resposta, de 2273 bytes, veio dividida em dois
segmentos TCP que o Wireshark remontou. A comunicação ocorreu sobre IPv6, na porta 80 do servidor.