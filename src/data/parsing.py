# Transform csv to sql
import pandas as pd

df1 = pd.read_csv('src/data/books_data_sample.csv')
df2 = pd.read_csv('src/data/books_rating_sample.csv')

df = pd.merge(df1, df2, on='title')
df.to_sql('books', 'sqlite:///src/data/books.db', index=False)
# Transform csv to sql
