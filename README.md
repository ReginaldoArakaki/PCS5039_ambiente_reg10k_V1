# Reg10k — versão V1: sala e cozinha, com família, visitante e gêmeo digital

Repositório de versão do ambiente de simulação Reg10k (PCS5039, EPUSP).
Linha de pesquisa: Laboratório de Digital Twin de Arquitetura de Sistemas de Software (EPUSP) e GLIP USP.

O código (motor, hub, plataforma, oráculo, página) fica no **núcleo**, na subpasta `nucleo/`,
fixado numa tag. Esta pasta guarda só o que é da versão:

| Pasta | Conteúdo |
|---|---|
| `ambiente/` | `residencia-v1.json` (morador e Rex) e, desde a v1dt.1, `residencia-v1-familia.json` (morador, moradora, criança, idoso, Rex e visitante) |
| `cenarios/` | Roteiros e resultados esperados: 38 cenários (M01–M14 da v1dt; 16 G* gerados por planta, famílias F1–F9; P01–P08 da v1dt.1) |
| `alunos/` | Controladores dos alunos (um pacote por grupo) |
| `experimentos/familias.json` | Famílias do protocolo de experimentos e os cenários de cada uma |
| `dados/` | CSV dos experimentos, manifestos e assinaturas de regressão |
| `docs/` | Planos e entregas das versões v1dt, v1dta, v1dtc e v1dt.1 |
| `tools/cenarios_v1dt1.py` | Gera os cenários P01–P08 da v1dt.1; os G* vêm de `python nucleo/reg10k.py gerador --ambiente residencia-v1 --versao v1dtc` |
| `site/` | Página gerada |

## Como usar

```
git clone --recurse-submodules <endereço deste repositório>
cd <pasta>
pip install -r nucleo/requirements.txt
python nucleo/reg10k.py catalogo            # catálogo e site/index.html
python nucleo/reg10k.py sim --cenario M01
python nucleo/reg10k.py experimentos --sementes 30
```

Para trocar a versão do núcleo: `cd nucleo && git fetch --tags && git checkout <tag>`, depois
`cd ..`, `git add nucleo` e um commit. Dados de artigo são gerados só com o núcleo numa tag
(o manifesto registra o commit).

Exercícios da versão: E12 (coordenar os cômodos) e E14 (quem lê parado × quem dorme), no roteiro dos alunos do núcleo (`nucleo/docs/roteiro-alunos.md`).

Resultados de simulação, não de medição.

Licenças: código MIT (`LICENSE`); dados e documentos CC BY 4.0 (`LICENSE-dados.md`).
