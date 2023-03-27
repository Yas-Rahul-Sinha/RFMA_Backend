import pandas as pd

clientEsc = pd.read_excel('WM Manager Dashboard Data SetV2.xlsx', sheet_name='Client Escalation', usecols=[0, 4, 10, 11, 12])
rows, columns = clientEsc.shape
print(clientEsc.to_dict()['Investor Name'])