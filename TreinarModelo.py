import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

# Carregar a planilha
df = pd.read_excel("planilha_treinamento.xlsx")

# Garantir que os nomes das colunas estejam limpos
df.columns = df.columns.str.strip()

# Colunas categóricas (exceto a target 'Evadiu')
colunas_categoricas = ["Sexo", "Objetivo", "Lesoes", "Recomendacao_Medica", "Nivel"]

# Pré-processamento robusto
for col in colunas_categoricas:
    # Converter para string, remover espaços e manter case original
    df[col] = df[col].astype(str).str.strip()
    
    # Tratar valores nulos/vazios
    df[col] = df[col].replace(['nan', 'null', '', ' '], pd.NA)

# Tratar a coluna target 'Evadiu' separadamente
df["Evadiu"] = df["Evadiu"].astype(str).str.strip().str.lower()
df["Evadiu"] = df["Evadiu"].replace({'sim': 1, 'não': 0, 'nao': 0, 'n': 0, 's': 1})

# Remover linhas com valores nulos
df = df.dropna(subset=colunas_categoricas + ["Evadiu"])

# Codificar colunas categóricas
label_encoders = {}
for col in colunas_categoricas:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le
    print(f"Classes para {col}: {list(le.classes_)}")  # Debug: ver classes

# Separar features e rótulo
X = df.drop(["Evadiu", "Nome"], axis=1)
y = df["Evadiu"].astype(int)  # Agora deve funcionar

# Verificar balanceamento das classes
print("\nDistribuição das classes:")
print(y.value_counts())

# Separar treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Treinar modelo
modelo = RandomForestClassifier(n_estimators=100, random_state=42)
modelo.fit(X_train, y_train)

# Avaliação
y_pred = modelo.predict(X_test)
print("\nRelatório de Classificação:")
print(classification_report(y_test, y_pred))

# Salvar modelo e encoders (apenas para features)
joblib.dump(modelo, "modelo_evasao.pkl")
joblib.dump(label_encoders, "encoders.pkl")

print("\nModelo e encoders salvos com sucesso!")