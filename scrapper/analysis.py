import pandas as pd
from leia import SentimentIntensityAnalyzer
import os

# --- 1. Carregar os dados do arquivo CSV ---
file_path = os.path.join(os.path.dirname(__file__), '..', 'feedbacks.csv')

if not os.path.exists(file_path):
    print(f"Erro: O arquivo 'feedbacks.csv' não foi encontrado em '{file_path}'.")
    print("Por favor, execute o script de scraping (scrapper/scrapper.py) primeiro.")
    exit()

try:
    df = pd.read_csv(file_path)
    print("Arquivo 'feedbacks.csv' carregado com sucesso.")
except Exception as e:
    print(f"Erro ao carregar o arquivo CSV: {e}")
    exit()


analyzer = SentimentIntensityAnalyzer()

# --- Bloco de Depuração ---
comments_to_debug = [
    "O material de marketing prometido nunca chegou. Fica difícil vender sem apoio da marca.",
    "É um bom sorvete, mas não tem nada de excepcional que o diferencie dos outros no mercado."
]
print("\n--- Depurando Comentários Específicos ---")
for comment in comments_to_debug:
    try:
        scores = analyzer.polarity_scores(comment)
        print(f"Comentário: {comment}")
        print(f"Scores: {scores}")
        print("-" * 20)
    except Exception as e:
        print(f"Não foi possível processar o comentário: {comment}. Erro: {e}")
print("----------------------------------------\n")


def get_sentiment(text):
    if isinstance(text, str):
        scores = analyzer.polarity_scores(text)
        
        # Lógica customizada (Proposta B)
        compound_score = scores['compound']
        pos_score = scores['pos']
        neg_score = scores['neg']
        
        # Critério: O sentimento deve ser claro (diferença > 0.1) e o compound score deve concordar
        if compound_score >= 0.05 and (pos_score - neg_score) > 0.1:
            return 'Positivo'
        elif compound_score <= -0.05 and (neg_score - pos_score) > 0.1:
            return 'Negativo'
        else:
            return 'Neutro'
    return 'Neutro'

print("\nRealizando análise de sentimento com LeIA nos comentários...")
# Aplicar a nova função
df['sentimento'] = df['comentario'].apply(get_sentiment)

# --- 4. Salvar o DataFrame atualizado de volta para CSV ---
try:
    df.to_csv(file_path, index=False, encoding='utf-8')
    print(f"\nAnálise de sentimento concluída e dados atualizados salvos em '{file_path}'")
    print("\nAmostra dos dados após a nova análise de sentimento:")
    print(df.head())
    print("\nContagem de sentimentos:")
    print(df['sentimento'].value_counts())
except Exception as e:
    print(f"Erro ao salvar o arquivo CSV atualizado: {e}")
