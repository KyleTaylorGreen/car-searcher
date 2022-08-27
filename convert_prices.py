import pandas as pd

df = pd.read_csv('all_cars.csv')

df = df[df.price != '\n']
df.price = df.price.apply(lambda x: int(x.replace(',', '')))

print(df.price)
df.to_csv('all_cars.csv', index=False)