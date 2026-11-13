# Exercício 8 — Tráfego ICMP (ping)

Arquivos neste diretório: `captura_icmp.pcapng` e `captura_icmp.png`.

## Como foi feito
1. Captura iniciada no Wireshark na interface Wi-Fi.
2. No terminal: `ping 192.168.1.1` (roteador da rede local).
3. Captura parada e filtro aplicado: `icmp`.

## Resultados
| Seq | Request (nº) | Reply (nº) | RTT |
|-----|--------------|------------|-----|
| 11  | 28629        | 28630      | 1,107 ms |
| 12  | 28913        | 28914      | 1,058 ms |
| 13  | 29215        | 29216      | 1,045 ms |
| 14  | 29474        | 29475      | 1,027 ms |

## Descrição
Foi enviado um ping de 192.168.1.8 para o roteador 192.168.1.1. A captura mostra quatro pares de
mensagens ICMP: Echo (ping) request e Echo (ping) reply, com o mesmo identificador (id=0x0001) e
números de sequência de 11 a 14. O RTT de cada pacote, medido entre o request e o reply, ficou
em torno de 1 ms, o que é esperado em uma rede local. Os requests têm TTL 128 (origem Windows)
e as respostas têm TTL 64 (origem roteador).