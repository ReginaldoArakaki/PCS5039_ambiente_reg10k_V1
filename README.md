# Reg10k — versão V1: sala e cozinha, com gêmeo digital e espelho

Repositório de versão do ambiente de simulação Reg10k (PCS5039, EPUSP).
Linha de pesquisa: Laboratório de Digital Twin de Arquitetura de Sistemas de Software (EPUSP) e GLIP USP.

O código (motor, hub, plataforma, oráculo, página) fica no **núcleo**, na subpasta `nucleo/`,
fixado numa tag. Esta pasta guarda só o que é da versão:

| Pasta | Conteúdo |
|---|---|
| `ambiente/` | Planta(s): residencia-v1 |
| `cenarios/` | Roteiros e resultados esperados (14 cenários) |
| `alunos/` | Controladores dos alunos (um pacote por grupo) |
| `experimentos/familias.json` | Famílias do protocolo de experimentos e os cenários de cada uma |
| `dados/` | CSV dos experimentos, manifestos e assinaturas de regressão |
| `docs/` | Planos e entregas das versões v1dt e v1dta (cópia do núcleo) |
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

Resultados de simulação, não de medição.

Licenças: código MIT (`LICENSE`); dados e documentos CC BY 4.0 (`LICENSE-dados.md`).
