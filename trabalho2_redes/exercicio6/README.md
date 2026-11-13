# Exercício 6 — Estabelecimento e encerramento de conexão TCP

Arquivos neste diretório: `captura_tcpp.pcapng`.

## Como foi feito
1. Captura iniciada no Wireshark na interface Wi-Fi.
2. No PowerShell: `telnet neverssl.com 80`, seguido do envio manual de `GET / HTTP/1.1` e `Host: neverssl.com`.
3. Captura parada e filtro aplicado: `tcp.port == 65508` (porta de origem usada pelo telnet).

## Resultados
- Three-way handshake: SYN (pacote nº 26299, retransmitido nos nº 26549, 27082 e 28071), SYN-ACK (nº 28129), ACK (nº 28130)
- Encerramento: FIN/ACK do servidor (nº 35193), ACK do cliente (nº 35194), FIN/ACK do cliente (nº 35196) e RST do servidor (nº 35247)

## Descrição
Foi aberta uma conexão TCP com neverssl.com (IPv6) na porta 80 usando telnet. O primeiro SYN não recebeu
resposta e foi retransmitido três vezes; o servidor respondeu com SYN-ACK e o cliente confirmou com ACK,
concluindo o three-way handshake cerca de 7 segundos após a primeira tentativa. Depois foi digitado um
GET HTTP e o servidor respondeu com 403 Forbidden no mesmo pacote em que enviou o FIN. O cliente
confirmou com ACK e enviou seu próprio FIN, e o servidor encerrou a conexão com um RST.