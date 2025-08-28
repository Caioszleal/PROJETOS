import requests

API_KEY = "de9c5fa909a84cf382849bdba550d676"  # cole sua chave da CurrencyFreaks aqui
BASE_URL = "https://api.currencyfreaks.com/latest"

def converter_moeda(valor: float, de: str, para: str) -> float:
    """
    Converte valor entre duas moedas usando a API CurrencyFreaks
    """
    params = {"apikey": API_KEY}
    try:
        resposta = requests.get(BASE_URL, params=params, timeout=10)
        resposta.raise_for_status()
        dados = resposta.json()

        taxas = dados.get("rates", {})
        base = dados.get("base", "USD")

        # Normaliza códigos
        de, para = de.upper().strip(), para.upper().strip()

        if de not in taxas or para not in taxas:
            raise ValueError(f"Moeda não suportada: {de} ou {para}")

        # Se a moeda de origem não for a base (USD), convertemos primeiro para USD
        valor_em_base = valor if de == base else valor / float(taxas[de])

        # Depois convertemos para a moeda de destino
        convertido = valor_em_base * float(taxas[para])
        return convertido
    except Exception as e:
        raise RuntimeError(f"Erro ao converter moeda: {e}")

if __name__ == "__main__":
    print("=== Conversor de Moedas (CurrencyFreaks) ===")
    try:
        valor = float(input("Digite o valor: ").replace(",", "."))
        moeda_origem = input("De qual moeda? (ex: USD, EUR, BRL): ").upper()
        moeda_destino = input("Para qual moeda? (ex: USD, EUR, BRL): ").upper()

        convertido = converter_moeda(valor, moeda_origem, moeda_destino)
        print(f"\n💱 {valor:.2f} {moeda_origem} = {convertido:.2f} {moeda_destino}")

    except Exception as erro:
        print("❌ Não foi possível realizar a conversão.")
        print("Detalhes:", erro)
