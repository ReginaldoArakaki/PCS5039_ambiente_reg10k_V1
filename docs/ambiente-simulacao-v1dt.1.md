# Ambiente de simulação Reg10k — v1dt.1: mais moradores, visitante e ocupante dormindo

**Versão do documento:** v02 | **Data:** 29/10/2026 | **Situação:** entregue
**Responsável:** Reginaldo Arakaki (EPUSP)
**Disciplina:** PCS5039 — Engenharia de Software Orientada a IoT (EPUSP)
**Linha de pesquisa:** Laboratório de Digital Twin de Arquitetura de Sistemas de Software (EPUSP) e GLIP USP
**Base:** núcleo `nucleo-v1.2`; V1 (`v1dtc`); plano das versões paralelas v05; plano do ambiente v02 (§2.1, incremento 2: "mais pessoas e um visitante"); v1dt (D1-05: PI-01 e presença incompatível adiadas para a v1dt.1); V1 Business Drivers v02 (RN03, RN09, RN17, RN34); V2/V3 v05 (RF-OPR-06, OC-03)

| Versão | Data | Mudança |
|---|---|---|
| v01 | 29/10/2026 | Plano para aprovação, com a rodada de dúvidas (§10) |
| v02 | 29/10/2026 | Entregue: as propostas da §10 valeram (aprovadas em 29/10/2026); resultados na §11 e ajustes (◆) na §12 |

---

## 1. Objetivo

Mudar **uma variável**, os ocupantes, mantendo a casa da V1 (sala, cozinha e vão). Entram:

1. **Mais moradores, de tipos diferentes**: ocupação múltipla e "um sai e outro fica".
2. **Visitante**: é ocupante para a automação (RN34), mas não tem papel no app.
3. **Ocupante dormindo** (PI-01, pendente desde o incremento 0).
4. **Presença incompatível** (RF-OPR-06): presença detectada sem entrada que a explique. É uma suspeita, nunca uma invasão (RN03), verificada a cada 5 min (RN17) e conciliada com uma passagem tardia antes de virar evento de fronteira.

A v1dt.1 prepara a casa de moradores diversos da V4.0 (R3, plano das versões paralelas §4.1): os tipos de morador nascem aqui, e a V4 apenas os reutiliza.

## 2. O que muda, onde

| Entrega | Onde | O que é |
|---|---|---|
| `nucleo-v1.3` | Núcleo | Tipos de ocupante, ação `DORMIR`, métricas de sono, detector de presença incompatível no hub, famílias F8 e F9 no gerador, normalização por cômodo no comparador |
| `v1dt.1` | Repositório da V1 | Ambiente `residencia-v1-familia` (a mesma planta com a nova família), cenários próprios (P01–P08), cenários gerados F8 e F9, dados |

Os cenários atuais da V1 (M01–M14 e G*) continuam no ambiente `residencia-v1`, com morador e Rex, e não mudam.

## 3. Ocupantes

| Ocupante | Tipo | O que muda na simulação | Proposta |
|---|---|---|---|
| Morador | Pessoa | Como hoje | — |
| Moradora | Pessoa | Como o morador | DQ11-02 |
| Criança | Pessoa | Anda mais rápido (1,2 m/s) e fica menos tempo parada | DQ11-03 |
| Idoso | Pessoa | Anda mais devagar (0,6 m/s) e fica mais tempo parado | DQ11-03 |
| Rex | Cachorro | Como hoje | — |
| Visitante | Pessoa, sem papel no app | Entra e sai pela porta; para os sensores, é igual a um morador (RN09) | DQ11-04 |

Os sensores **não distinguem** tipo, idade nem identidade (RN09). As diferenças acima são só de movimento: o controlador não as vê, apenas sente o efeito.

## 4. Ocupante dormindo (PI-01)

A dúvida de fundo, aberta desde o incremento 0: com alguém dormindo, a luz deve ficar acesa ou apagar? Proposta (DQ11-01): **o ideal é apagar**.

- Ação nova `DORMIR` (diferente de `PARADO`): o ocupante fica imóvel, com microgestos raros. O FN05 (Rex deitado, `PARADO`) não muda.
- Métrica nova `luz_com_todos_dormindo_s`: tempo com a luz acesa e todos os ocupantes do cômodo dormindo (o ideal é zero).
- `escuro_com_ocupante_s` e `apagamentos_indevidos` não contam quem está dormindo: apagar com todos dormindo não é indevido.
- A tensão didática é que o controlador **não distingue** "lendo parado" (FN01, deve ficar acesa) de "dormindo" (deve apagar), porque os sensores não veem a diferença (RN09). É matéria do E14.

## 5. Presença incompatível (RF-OPR-06)

| Item | Proposta |
|---|---|
| Quando | O cômodo (ou a casa) estava vazio por inferência e o SP detecta movimento **sem** passagem que o explique (nenhum SA na porta externa nem nas passagens do cômodo nos últimos 10 s) |
| Quem detecta | Um componente novo do hub, fora do controlador: o **detector de presença incompatível** (OC-03 da V2/V3). O controlador continua acendendo normalmente (RN-I0-02) |
| Verificação | A suspeita é verificada a cada 5 min (RN17); um SA que chega atrasado e explica a presença concilia a suspeita, que é descartada |
| Saída | Persistindo após a verificação, o hub registra `SUSPEITA_PRESENCA` (SISTEMA) e a plataforma recebe um **evento de fronteira** para ocorrências, com o texto "presença não explicada", **nunca "invasão"** (RN03) |
| Invariante nova | **OR-15:** nenhum evento rotula invasão; todo evento de fronteira é precedido de uma verificação; uma suspeita conciliada nunca é enviada (DQ11-05) |

Exemplos: o visitante que ficou dormindo no sofá quando todos saíram e depois acorda; o SA que falha numa entrada rápida (FN04).

## 6. Cenários

**Próprios da v1dt.1** (ambiente `residencia-v1-familia`, asserções com janela relativa):

| ID | Cenário | Família |
|---|---|---|
| P01 | Família chega junta e se espalha pela casa | F1 |
| P02 | Um sai e outro fica (a sala não pode apagar com alguém dentro) | F8 |
| P03 | Idoso lê parado na sala por 20 min | F2 |
| P04 | Criança dorme no sofá; os adultos vão para a cozinha | F9 |
| P05 | Visitante chega com a casa vazia (entrada normal, nada de suspeito) | F1 |
| P06 | Todos saem e o visitante fica dormindo; acorda 15 min depois (presença incompatível, sem passagem) | F10 |
| P07 | Entrada rápida com o SA falhando; o SA atrasado chega e concilia a suspeita | F10 |
| P08 | Desconexão com quatro pessoas circulando | F5 |

**Famílias novas no protocolo:** F8 (ocupação múltipla: um sai e outro fica), F9 (dormir) e F10 (presença incompatível). F8 e F9 são geradas por planta, por cômodo, para todas as versões quando subirem de núcleo. F10 fica, por enquanto, só com cenários próprios, porque depende de falha de sensor ou de alguém que ficou para trás.

## 7. Regressão

| O quê | Garantia |
|---|---|
| Conjunto de regressão do núcleo (46 cenários) | Assinaturas de decisões e atuações iguais às da `nucleo-v1.2` |
| V0, V1 e V2 | Ficam na `nucleo-v1.2` até subirem; os cenários atuais não usam `DORMIR` nem os ocupantes novos |
| Detector de presença incompatível | Roda em todos os cenários. Pode registrar suspeitas em cenários antigos (por exemplo, FN04), mas só nas camadas SISTEMA e PLATAFORMA, e por isso as assinaturas não mudam. Os casos serão listados na entrega |

## 8. Dentro × fora

| Dentro (v1dt.1) | Fora | Entra em |
|---|---|---|
| Moradores de tipos diferentes, visitante, `DORMIR`, presença incompatível, F8 e F9, normalização por cômodo | Hora do dia (noite e dia) e aprendizado de hábitos | v3dt (V3) |
| | Várias residências na plataforma | V4.0 |
| | Contagem de pessoas | Fora do escopo (RN09) |

## 9. Diferenças didáticas e exercício

- O aluno vê que "parado" pode ser alguém lendo (luz acesa) ou dormindo (luz apagada), e que os sensores não separam os dois casos.
- **E14 (novo).** Com P03 (idoso lendo) e P04 (criança dormindo), medir o compromisso entre escuro com ocupante acordado e luz acesa com todos dormindo; propor uma política e justificá-la com os dados. Pesos sugeridos: análise 40%, política e medição 40%, discussão 20%.

## 10. Rodada de dúvidas

| ID | Pergunta | Opções | Proposta |
|---|---|---|---|
| **DQ11-01** (bloqueante, PI-01) | Com o ocupante dormindo, a luz deve ficar acesa ou apagar? | (a) apagar é o ideal; (b) ficar acesa, como hoje no FN05 | **(a)**: quem dorme quer escuro. A dificuldade passa a ser distinguir quem lê de quem dorme, que é o ponto didático |
| **DQ11-02** (bloqueante) | Composição da família | (a) morador, moradora, criança, idoso e Rex, mais visitante ocasional; (b) só mais um adulto e o visitante | **(a)**: é a mesma casa diversa da V4.0 (R3) |
| DQ11-03 | Diferenças entre os tipos de pessoa | Só velocidade e tempo parado; ou também sensibilidade do PIR | Só movimento: nenhuma "física" de sensor sem fonte |
| DQ11-04 | O visitante tem algum papel no app? | Não; ou membro temporário | Não: é ocupante para a automação (RN34), sem acesso ao app |
| DQ11-05 | Numeração da invariante nova | OR-15 aqui e OR-16 para o isolamento da V4; ou o contrário | OR-15 aqui (vem primeiro); o plano das versões paralelas passa a usar OR-16 para a V4 |
| DQ11-06 | Famílias novas F8, F9 e F10 no protocolo | F8 e F9 no gerador agora; ou só cenários próprios | F8 e F9 no gerador agora, para a V0 e a V2 também as terem quando subirem; F10 só com cenários próprios |
| DQ11-07 | Normalização por cômodo no comparador | Junto com a v1dt.1; ou depois | Junto: é pequena e corrige o cuidado da §14.4 do plano das versões paralelas |

Sem objeção, as propostas valem.

**Duração de referência:** núcleo `nucleo-v1.3`, 1 a 2 dias; v1dt.1, 1 dia.

## 11. Resultados

### 11.1 Entregas

| Onde | Commit | O que entrou |
|---|---|---|
| Núcleo `nucleo-v1.3` | `7077d3c` | Perfis de pessoa e visitante; `DORMIR` e `ACORDAR`; `luz_com_todos_dormindo_s`; detector de presença incompatível no hub e evento de fronteira na plataforma; OR-15 e métricas de suspeitas; F8 e F9 no gerador, F10 no protocolo; comparador por ambiente e por cômodo; página com uma cor por pessoa e sinal de sono; RN-V1-05 a 07; E14 |
| V1 `v1dt.1` | ver a tag | Ambiente `residencia-v1-familia`; P01–P08; G08 e G09 na residência; 76 assinaturas; primeira rodada de dados da v1dt.1 |

### 11.2 Verificação

- Núcleo: 259 testes em 3.12 e 3.9; as 92 assinaturas do conjunto de regressão são iguais às da `nucleo-v1.2`. **Nenhum dos 46 cenários antigos abre suspeita** de presença incompatível.
- V1: as 52 assinaturas anteriores (M01–M14 e G01–G07) são iguais; catálogo com 30 sementes sem problemas; JSON válidos; página aberta no navegador nas 76 execuções, sem erros.
- Testes novos que precisam falhar quando devem: a OR-15 reprova um evento de fronteira sem verificação e um rótulo de "invasão".

### 11.3 Primeira rodada de dados (30 sementes, referência e grupo_exemplo)

| Família | Medida (média) | Referência | grupo_exemplo |
|---|---|---|---|
| F8 Um sai e outro fica | Requisitos atendidos | 100% | 100% |
| F9 Dormir | Requisitos atendidos | 100% | 66,7% |
| F9 Dormir | Luz acesa com todos dormindo (s) | 61,8 | 61,8 |
| F2 Parado | Escuro com ocupante acordado (s) | 470 | 471 |
| F10 Presença incompatível | Suspeitas abertas / confirmadas / conciliadas por execução | 0,67 / 0,33 / 0,33 | idem |

- **Dormir × ler parado (E14).** Com T_apagamento de 60 s, quem dorme fica cerca de 60 s com a luz acesa (o custo pequeno), e quem lê parado fica em média 470 s no escuro na F2 (o custo grande). Os dois custos vêm da mesma regra, porque os sensores não separam os dois casos.
- **O detector se comporta igual em todas as sementes:** P05 não abre suspeita (a porta explica a entrada), P06 confirma uma e a envia como "presença não explicada", P07 concilia uma com a passagem tardia. É do hub, não do controlador, por isso os dois controladores têm os mesmos números.
- A única falha da referência (F1, 99,6%) é o M01 com a semente 25, o caso conhecido da janela absoluta (plano das versões paralelas, §11.3).

## 12. Ajustes feitos na construção (◆)

| Item | Motivo |
|---|---|
| ◆ Movimento contínuo conta como evidência na verificação | O PIR avisa o início e o fim do movimento, não cada passo: um visitante andando sem parar gerava um único MOVIMENTO, e a verificação descartava a suspeita |
| ◆ P05 na família F10, não na F1 | O cenário testa o detector (entrada explicada pela porta), não a iluminação |
| ◆ Perfis mudam só a velocidade | "Menos ou mais tempo parado" ficou nos roteiros (P03, P04), e não no motor |
| ◆ Os G* da V1 continuam só na residência original | Os cenários gerados existem para comparar plantas; a família é testada pelos P* |
