import pandas as pd


df = pd.read_csv("csv/Statistiche_Fantacalcio_2020-21.csv")
df.columns = ['Id', 'Ruolo', 'Nome', 'Squadra', 'Partite giocate', 'Media voto',
              'Media Fantavoto', 'Goal fatti', 'Goal subiti',
              'Rigori parati', 'Rigori calciati', 'Rigori segnati',
              'Rigori sbagliati', 'Assist', 'Assist da fermo', 'Ammonizioni',
              'Espulsioni', 'Autogoal']
tot_goals = df["Goal fatti"] + df["Rigori segnati"]
tot_ass = df['Assist'] + df['Assist da fermo']
df.insert(7, "Goals tot", tot_goals, True)
df.insert(8, "Assists tot", tot_ass, True)

df.to_csv('stats2020.csv', index=False)
