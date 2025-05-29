import pandas as pd
import joblib
from fpdf import FPDF
import numpy as np  # Adicionado para trabalhar com valores NaN

# Carregar modelo e encoders
modelo = joblib.load("modelo_evasao.pkl")
encoders = joblib.load("encoders.pkl")

# Carregar nova planilha de teste
df = pd.read_excel("planilha_teste_20_pessoas.xlsx")

# Guardar os nomes para exibir depois
nomes = df["Nome"].tolist()

# Colunas categóricas a serem transformadas
colunas_categoricas = ['Sexo', 'Objetivo', 'Lesoes', 'Recomendacao_Medica', 'Nivel']

# Etapa CRÍTICA: converter strings 'nan' para valores NaN reais
for col in colunas_categoricas:
    # Converter para string e remover espaços
    df[col] = df[col].astype(str).str.strip()
    # Substituir 'nan' string por NaN real
    df[col] = df[col].replace('nan', np.nan)

# Remover linhas com valores NaN nas colunas categóricas
df = df.dropna(subset=colunas_categoricas)

# Aplicar os encoders
for col in colunas_categoricas:
    le = encoders[col]
    desconhecidos = df[~df[col].isin(le.classes_)][col].unique().tolist()
    
    if desconhecidos:
        print(f"⚠ Ignorando registros com valores desconhecidos em '{col}':\n{desconhecidos}")
        df = df[df[col].isin(le.classes_)]  # remove linhas com valores não vistos

    # Aplicar transformação apenas se ainda houver dados
    if not df.empty:
        df[col] = le.transform(df[col])

# Guardar os nomes restantes após possível remoção
nomes = df["Nome"].tolist()

# Remover colunas desnecessárias
X = df.drop(columns=["Nome"])

if df.empty:
    print("Nenhum dado válido restante após a remoção de registros com valores desconhecidos")
    exit()

# Fazer predição
predicoes = modelo.predict(X)

# Mostrar resultado e preparar lista de quem vai evadir
evasores = []

for nome, pred in zip(nomes, predicoes):
    status = "Evadir" if pred == 1 else "Permanecer"
    print(f"{nome}: {status}")
    if pred == 1:
        evasores.append(nome)

# Exportar relatório em PDF com quem tem chance de evadir
if evasores:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, txt="Relatório de Possíveis Evasores", ln=True, align='C')
    pdf.ln(10)  # Espaço

    for idx, nome in enumerate(evasores, 1):
        pdf.cell(200, 10, txt=f"{idx}. {nome}", ln=True)

    pdf.output("relatorio_evasores.pdf")
    print("\n✅ Relatório PDF 'relatorio_evasores.pdf' gerado com sucesso!")
else:
    print("\n✅ Nenhum possível evasor detectado. PDF não gerado.")