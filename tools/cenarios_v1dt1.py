"""Cenários da v1dt.1 (mais moradores, visitante, ocupante dormindo, presença incompatível).

Uso, na raiz do repositório da V1:  python tools/cenarios_v1dt1.py
Ambiente: ambiente/residencia-v1-familia.json (a planta da V1 com a família).
"""
from __future__ import annotations

import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ENTRA = {"evento": "CRUZOU_PORTA", "sentido": "ENTRADA"}
INV = {"id": "INV", "nivel": "REQUISITO", "dado": "qualquer controlador", "quando": "o cenário termina",
       "entao": {"tipo": "invariantes"}}
BASE = {"versao": "v1dt.1", "ambiente": "residencia-v1-familia", "modo": "IDEAL",
        "estado_inicial": {"ocupantes_na_sala": [], "luz": "APAGADA"}, "falhas": []}
PORTA = [0.95, 1.0]


def a(t, quem, acao, **kw):
    return {"t_ms": t, "ocupante": quem, "acao": acao, **kw}


def r(id_, n, dado, quando, entao):
    return {"id": id_, "nivel": n, "dado": dado, "quando": quando, "entao": entao}


def sai(t, quem):
    return [a(t, quem, "ANDAR", ate=PORTA), a(t + 8_000, quem, "SAIR")]


CENARIOS = [
    ({**BASE, "id": "P01", "titulo": "A família chega junta e se espalha", "tipo": "NORMAL", "duracao_ms": 480_000,
      "descricao": "Morador, moradora, criança e idoso entram juntos; a moradora e o morador vão para a cozinha; a criança e o idoso ficam na sala. Depois todos saem.",
      "comportamento_ideal": "Cada cômodo acende quando alguém entra e fica aceso enquanto há alguém.",
      "comportamento_referencia": "O SA da porta e o do vão acendem os cômodos; ninguém fica no escuro enquanto se move.",
      "requisitos": ["RF-OPR-01", "RN34"], "regras": ["RN-V1-07", "RN-I0-02"],
      "acoes": [a(5_000, "morador", "ENTRAR"), a(6_000, "moradora", "ENTRAR"), a(7_000, "crianca", "ENTRAR"),
                a(8_000, "idoso", "ENTRAR"), a(15_000, "moradora", "MUDAR_COMODO", para="cozinha"),
                a(10_000, "crianca", "ANDAR_ALEATORIO", duracao_ms=290_000), a(11_000, "idoso", "ANDAR_ALEATORIO", duracao_ms=290_000),
                a(28_000, "moradora", "ANDAR_ALEATORIO", duracao_ms=230_000), a(30_000, "morador", "MUDAR_COMODO", para="cozinha"),
                a(43_000, "morador", "ANDAR_ALEATORIO", duracao_ms=215_000),
                a(260_000, "moradora", "MUDAR_COMODO", para="sala"), a(262_000, "morador", "MUDAR_COMODO", para="sala"),
                *sai(310_000, "crianca"), *sai(312_000, "idoso"), *sai(314_000, "moradora"), *sai(316_000, "morador")]},
     [r("A1", "REQUISITO", "cozinha escura", "a primeira pessoa entra",
        {"tipo": "luz", "comodo": "cozinha", "valor": "ACESA", "apos": ENTRA, "ate_ms": 1_000}),
      r("A2", "REQUISITO", "criança e idoso andando na sala", "o cenário corre",
        {"tipo": "luz_constante", "comodo": "sala", "valor": "ACESA", "entre_ms": [6_000, 300_000]}),
      r("A3", "REQUISITO", "ocupantes se movendo", "o cenário termina",
        {"tipo": "metrica", "nome": "apagamentos_indevidos", "igual": 0}),
      r("A4", "REQUISITO", "entrada em cômodo escuro", "a lâmpada acende",
        {"tipo": "metrica", "nome": "atraso_percebido_ms_max", "max": 1_000})]),

    ({**BASE, "id": "P02", "titulo": "Um sai e outro fica", "tipo": "NORMAL", "duracao_ms": 420_000,
      "descricao": "Morador e moradora estão na sala; o morador sai da casa e a moradora continua andando na sala.",
      "comportamento_ideal": "A sala fica acesa enquanto a moradora está lá.",
      "comportamento_referencia": "O SA da saída não apaga nada; o SP continua vendo a moradora.",
      "requisitos": ["RF-OPR-01", "RN34"], "regras": ["RN-I0-03", "RN-V1-07"],
      "acoes": [a(5_000, "morador", "ENTRAR"), a(6_000, "moradora", "ENTRAR"),
                a(9_000, "moradora", "ANDAR_ALEATORIO", duracao_ms=410_000), a(10_000, "morador", "ANDAR_ALEATORIO", duracao_ms=40_000),
                *sai(60_000, "morador")]},
     [r("A1", "REQUISITO", "a moradora fica na sala", "o morador sai da casa",
        {"tipo": "luz_constante", "comodo": "sala", "valor": "ACESA", "entre_ms": [7_000, 420_000]}),
      r("A2", "REQUISITO", "ocupante sempre presente", "o cenário termina",
        {"tipo": "metrica", "comodo": "sala", "nome": "apagamentos_indevidos", "igual": 0})]),

    ({**BASE, "id": "P03", "titulo": "O idoso lê parado na sala por 20 min", "tipo": "FALSO_NEGATIVO", "duracao_ms": 1_320_000,
      "descricao": "O idoso entra, senta e lê parado por 20 min, com um gesto aos 10 min.",
      "comportamento_ideal": "A luz fica acesa: ele está acordado.",
      "comportamento_referencia": "Limitação conhecida (como o FN01): apaga 60 s depois do último movimento; o gesto aos 10 min acende de novo.",
      "requisitos": ["RF-OPR-01", "CF05"], "regras": ["RN-I0-03", "RN-V1-05"],
      "acoes": [a(5_000, "idoso", "ENTRAR"), a(9_000, "idoso", "ANDAR", ate=[2.0, 3.0]), a(20_000, "idoso", "PARADO"),
                a(620_000, "idoso", "GESTO"), a(621_000, "idoso", "PARADO")]},
     [r("A1", "REQUISITO", "sala escura", "o idoso entra",
        {"tipo": "luz", "comodo": "sala", "valor": "ACESA", "apos": ENTRA, "ate_ms": 1_000}),
      r("A2", "CARACTERIZACAO", "acordado e parado", "60 s sem movimento",
        {"tipo": "metrica", "comodo": "sala", "nome": "escuro_com_ocupante_s", "min": 600}),
      r("A3", "CARACTERIZACAO", "ninguém dormindo", "o cenário termina",
        {"tipo": "metrica", "comodo": "sala", "nome": "luz_com_todos_dormindo_s", "igual": 0})]),

    ({**BASE, "id": "P04", "titulo": "A criança dorme no sofá; os adultos vão para a cozinha", "tipo": "FALSO_NEGATIVO",
      "duracao_ms": 600_000,
      "descricao": "A família entra; a criança deita no sofá e dorme; os três adultos vão para a cozinha e ficam lá.",
      "comportamento_ideal": "A sala apaga com a criança dormindo (RN-V1-05); a cozinha fica acesa.",
      "comportamento_referencia": "A sala apaga T_apagamento depois do último movimento; apagar com a criança dormindo não é indevido.",
      "requisitos": ["RF-OPR-01", "CF05"], "regras": ["RN-V1-05", "RN-I0-03"],
      "acoes": [a(5_000, "morador", "ENTRAR"), a(6_000, "moradora", "ENTRAR"), a(7_000, "crianca", "ENTRAR"),
                a(8_000, "idoso", "ENTRAR"), a(10_000, "crianca", "ANDAR", ate=[1.2, 3.2]), a(25_000, "crianca", "DORMIR"),
                a(40_000, "morador", "MUDAR_COMODO", para="cozinha"), a(42_000, "moradora", "MUDAR_COMODO", para="cozinha"),
                a(44_000, "idoso", "MUDAR_COMODO", para="cozinha"),
                a(60_000, "morador", "ANDAR_ALEATORIO", duracao_ms=540_000), a(62_000, "moradora", "ANDAR_ALEATORIO", duracao_ms=538_000),
                a(64_000, "idoso", "ANDAR_ALEATORIO", duracao_ms=536_000)]},
     [r("A1", "REQUISITO", "criança dormindo na sala", "a sala apaga",
        {"tipo": "metrica", "comodo": "sala", "nome": "apagamentos_indevidos", "igual": 0}),
      r("A2", "REQUISITO", "adultos andando na cozinha", "o cenário corre",
        {"tipo": "luz_constante", "comodo": "cozinha", "valor": "ACESA", "entre_ms": [70_000, 600_000]}),
      r("A3", "CARACTERIZACAO", "criança dormindo", "até o T_apagamento",
        {"tipo": "metrica", "comodo": "sala", "nome": "luz_com_todos_dormindo_s", "max": 120})]),

    ({**BASE, "id": "P05", "titulo": "O visitante chega com a casa vazia", "tipo": "NORMAL", "duracao_ms": 480_000,
      "descricao": "O morador passa em casa e sai; com a casa vazia, o visitante chega pela porta, anda pela sala e vai embora.",
      "comportamento_ideal": "Nada de suspeito: a entrada do visitante é explicada pelo SA da porta.",
      "comportamento_referencia": "O detector vê a casa vazia depois da saída do morador, mas o SA da porta explica a presença do visitante.",
      "requisitos": ["RF-OPR-06", "RN34"], "regras": ["RN-V1-06", "RN-V1-07"],
      "acoes": [a(5_000, "morador", "ENTRAR"), a(8_000, "morador", "ANDAR", ate=PORTA), a(15_000, "morador", "SAIR"),
                a(200_000, "visitante", "ENTRAR"), a(203_000, "visitante", "ANDAR_ALEATORIO", duracao_ms=120_000),
                *sai(330_000, "visitante")]},
     [r("A1", "REQUISITO", "casa vazia", "o visitante entra pela porta",
        {"tipo": "luz", "comodo": "sala", "valor": "ACESA", "apos": {**ENTRA, "ocorrencia": 2}, "ate_ms": 1_000}),
      r("A2", "REQUISITO", "entrada explicada", "o cenário termina",
        {"tipo": "metrica", "nome": "suspeitas_abertas", "igual": 0})]),

    ({**BASE, "id": "P06", "titulo": "Todos saem e o visitante fica dormindo; acorda 15 min depois", "tipo": "FALHA",
      "duracao_ms": 1_400_000,
      "descricao": "O visitante dorme no sofá; morador e moradora saem; a casa fica quieta; 15 min depois o visitante acorda e anda pela casa.",
      "comportamento_ideal": "Presença sem entrada que a explique: suspeita, verificada em 5 min e enviada como \"presença não explicada\", nunca como invasão.",
      "comportamento_referencia": "O detector abre a suspeita no primeiro movimento, confirma na verificação de 5 min e a plataforma registra o evento de fronteira.",
      "requisitos": ["RF-OPR-06", "RNP-MP3-10"], "regras": ["RN-V1-06"],
      "acoes": [a(5_000, "morador", "ENTRAR"), a(6_000, "moradora", "ENTRAR"), a(7_000, "visitante", "ENTRAR"),
                a(10_000, "visitante", "ANDAR", ate=[2.0, 2.0]), a(20_000, "visitante", "DORMIR"),
                a(12_000, "morador", "ANDAR", ate=PORTA), a(25_000, "morador", "SAIR"),
                a(14_000, "moradora", "ANDAR", ate=PORTA), a(27_000, "moradora", "SAIR"),
                a(930_000, "visitante", "ACORDAR"), a(935_000, "visitante", "ANDAR_ALEATORIO", duracao_ms=460_000)]},
     [r("A1", "REQUISITO", "casa vazia por inferência", "o visitante acorda e anda",
        {"tipo": "metrica", "nome": "suspeitas_confirmadas", "igual": 1}),
      r("A2", "REQUISITO", "suspeita confirmada", "a plataforma recebe",
        {"tipo": "evento", "camada": "PLATAFORMA", "evento": "EVENTO_FRONTEIRA", "campos": {"evento": "PRESENCA_NAO_EXPLICADA"}}),
      r("A3", "REQUISITO", "visitante acordado", "ele se mexe",
        {"tipo": "luz", "comodo": "sala", "valor": "ACESA", "apos": {"evento": "ACORDOU"}, "ate_ms": 2_000})]),

    ({**BASE, "id": "P07", "titulo": "O SA falha na entrada do visitante; o morador chega logo depois", "tipo": "FALHA",
      "duracao_ms": 700_000,
      "descricao": "Com a casa vazia, o SA perde a entrada do visitante; 15 s depois o morador entra pela porta e o SA o detecta.",
      "comportamento_ideal": "A passagem pela porta logo depois explica a presença: a suspeita é conciliada e não sai do hub.",
      "comportamento_referencia": "Suspeita aberta no primeiro movimento e conciliada pelo SA do morador (passagem tardia).",
      "requisitos": ["RF-OPR-06", "RNP-MP3-10"], "regras": ["RN-V1-06"],
      "falhas": [{"t_ms": 190_000, "tipo": "SA_PERDE_PROXIMA"}],
      "acoes": [a(5_000, "morador", "ENTRAR"), a(8_000, "morador", "ANDAR", ate=PORTA), a(15_000, "morador", "SAIR"),
                a(200_000, "visitante", "ENTRAR"), a(203_000, "visitante", "ANDAR_ALEATORIO", duracao_ms=480_000),
                a(215_000, "morador", "ENTRAR"), a(218_000, "morador", "ANDAR_ALEATORIO", duracao_ms=470_000)]},
     [r("A1", "REQUISITO", "passagem tardia", "o morador entra",
        {"tipo": "metrica", "nome": "suspeitas_conciliadas", "igual": 1}),
      r("A2", "REQUISITO", "suspeita conciliada", "o cenário termina",
        {"tipo": "metrica", "nome": "suspeitas_confirmadas", "igual": 0})]),

    ({**BASE, "id": "P08", "titulo": "Desconexão com quatro pessoas circulando", "tipo": "GEMEO_DIGITAL", "duracao_ms": 780_000,
      "descricao": "O canal cai por 10 min enquanto a família circula entre a sala e a cozinha.",
      "comportamento_ideal": "A automação local segue; o gêmeo se declara desatualizado e reconcilia ao voltar.",
      "comportamento_referencia": "Fila persistente, estado por cômodo, reconciliação em até 5 s.",
      "requisitos": ["RF-SYN-03", "RF-SYN-04", "RNF-CON-01", "CF06"], "regras": ["RN-DT-03", "RN-DT-04", "RN-V1-04"],
      "falhas": [{"t_ms": 60_000, "tipo": "CANAL_DESCONECTA", "duracao_ms": 600_000}],
      "acoes": [a(5_000, "morador", "ENTRAR"), a(6_000, "moradora", "ENTRAR"), a(7_000, "crianca", "ENTRAR"),
                a(8_000, "idoso", "ENTRAR"), a(20_000, "moradora", "MUDAR_COMODO", para="cozinha"),
                a(22_000, "crianca", "MUDAR_COMODO", para="cozinha"),
                a(35_000, "moradora", "ANDAR_ALEATORIO", duracao_ms=745_000), a(36_000, "crianca", "ANDAR_ALEATORIO", duracao_ms=744_000),
                a(10_000, "morador", "ANDAR_ALEATORIO", duracao_ms=770_000), a(11_000, "idoso", "ANDAR_ALEATORIO", duracao_ms=769_000)]},
     [r("A1", "REQUISITO", "canal caído", "logo depois da queda",
        {"tipo": "gemeo", "comodo": "sala", "em_ms": 61_000, "atualidade": "DESATUALIZADO", "conexao": "DESCONECTADO"}),
      r("A2", "REQUISITO", "canal volta", "o hub reconcilia", {"tipo": "metrica", "nome": "reconciliacao_ms_max", "max": 5_000}),
      r("A3", "REQUISITO", "fila persistente", "o cenário termina", {"tipo": "metrica", "nome": "eventos_nao_entregues", "igual": 0}),
      r("A4", "REQUISITO", "família se movendo", "o cenário termina",
        {"tipo": "metrica", "nome": "apagamentos_indevidos", "igual": 0})]),
]
FAMILIAS = {"P01": "F1", "P02": "F8", "P03": "F2", "P04": "F9", "P05": "F10", "P06": "F10", "P07": "F10", "P08": "F5"}


def main() -> int:
    for rot, asserc in CENARIOS:
        rot = {**rot, "acoes": sorted(rot["acoes"], key=lambda x: x["t_ms"])}
        for sub, doc in (("roteiros", rot), ("esperado", {"cenario": rot["id"], "modo": "IDEAL", "semente_referencia": 42,
                                                          "requisitos": rot["requisitos"], "assercoes": asserc + [INV]})):
            p = RAIZ / "cenarios" / sub / f"{rot['id']}.json"
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    fp = RAIZ / "experimentos" / "familias.json"
    fam = json.loads(fp.read_text(encoding="utf-8"))
    for cid, f in FAMILIAS.items():
        fam["familias"][f] = sorted(set(fam["familias"].get(f, [])) | {cid})
    fp.write_text(json.dumps(fam, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{len(CENARIOS)} cenários gravados")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
