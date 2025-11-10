import pandas as pd
from bs4 import BeautifulSoup
import os

file_path = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'index.html')


if not os.path.exists(file_path):
    print(f"Erro: O arquivo HTML não foi encontrado em '{file_path}'")
    exit()


with open(file_path, 'r', encoding='utf-8') as f:
    html_content = f.read()
    print("Arquivo HTML carregado com sucesso.")

soup = BeautifulSoup(html_content, 'html.parser')
print("HTML analisado pelo BeautifulSoup.")

feedbacks_data = []

feedback_cards = soup.find_all('div', class_='padrao-card')

if not feedback_cards:
    print("Nenhum card de feedback encontrado. Verifique as classes do HTML.")
else:
    print(f"Encontrados {len(feedback_cards)} feedbacks. Extraindo dados...")
    
    for card in feedback_cards:
        try:
            nome = card.find('h2', class_='nome-feedback').text.strip()
            funcao = card.find('p', class_='funcao').text.strip()
            comentario = card.find('p', class_='comment').text.strip()
            
            # Contar o número de estrelas (ícones de estrela)
            estrelas = len(card.find('div', class_='clissificacao').find_all('i', class_='fa-star'))
            
            feedbacks_data.append({
                'nome': nome,
                'funcao': funcao,
                'comentario': comentario,
                'estrelas': estrelas
            })
        except AttributeError as e:
            print(f"Aviso: Erro ao processar um card. Pode haver um card mal formatado. Detalhes: {e}")
            continue

# --- 4. Criar um DataFrame com o Pandas ---
if feedbacks_data:
    df = pd.DataFrame(feedbacks_data)
    
    # --- 5. Salvar os dados em um arquivo CSV ---
    # Salvar na raiz do projeto para ser fácil de acessar pelo dashboard
    output_path = os.path.join(os.path.dirname(__file__), '..', 'feedbacks.csv')
    
    try:
        df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"\nDados extraídos com sucesso e salvos em '{output_path}'")
        print("\nAmostra dos dados extraídos:")
        print(df.head())
    except Exception as e:
        print(f"Erro ao salvar o arquivo CSV: {e}")
else:
    print("\nNenhum dado de feedback foi extraído. O arquivo CSV não foi gerado.")