# Treino e teste de Modelo de deeplearning para identificar alunos com chance de evasão em academias, geração de relatório e envio por email.

- O treino utiliza uma planilha com 50 pessoas inscritas em uma academia e usa as colunas: Nivel, Recomendacao_Medica, Lesoes, Objetivo e Sexo para avaliar evasão.
  
- O arquivo config.env tem as informações do email remetente, destinatário e senha do app para uso do smtplib.

- Após rodar TestarModelo.py ele criará um relatório em PDF com os nomes de quem tem probabilidade de evadir.

- "enviar_relatorio.bat" deve ser configurado no agendador de tarefas do windows para automação


