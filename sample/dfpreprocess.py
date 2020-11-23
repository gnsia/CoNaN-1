import pandas as pd
import json

df = pd.read_csv('85.180.217.131.csv')
# df_json = df.to_dict(orient=records)
# df_json = df.to_dict(orient=records)

# df_json['Timestamp']
# print(df_json.Timestamp)
# parsed = json.loads(df_json)
# print(json.dumps(df_json, indent=4))
# print(json_data['Timestamp'])
# data = json.dumps(df_json, indent=4)
#
# print(df_json)
# print(data)
js = {
    'timestamp':df.Timestamp.to_list(),
    'status': df.Status.to_list()
}

timestamp = df.Timestamp.to_list()
print(len(js['timestamp']), len(js['status']))