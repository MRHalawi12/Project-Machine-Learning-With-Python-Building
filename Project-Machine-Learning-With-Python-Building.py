import pandas as pd
import numpy as np
#reading dataset
movie_df = pd.read_csv('https://dqlab-dataset.s3-ap-southeast-1.amazonaws.com/title.basics.tsv', sep='\t') #untuk menyimpan title_basics.tsv
rating_df = pd.read_csv('https://dqlab-dataset.s3-ap-southeast-1.amazonaws.com/title.ratings.tsv', sep='\t') #untuk menyimpan title.ratings.ts

print(movie_df.head())
print(movie_df.info())

print(movie_df.isnull().sum())
#Analyze column for null data part 1
print(movie_df.loc[(movie_df['primaryTitle'].isnull()) | (movie_df['originalTitle'].isnull())])
#clean out data with null value

#updating movie_df by cleaning out data with null value
movie_df = movie_df.loc[(movie_df['primaryTitle'].notnull()) & (movie_df['originalTitle'].notnull())]

#displaying total data after cleaning out null value
print(len(movie_df))
print(movie_df.loc[movie_df['genres'].isnull()])

#clean out data with null value

#updating movie_df by cleaning out data with null value
movie_df = movie_df.loc[movie_df['genres'].notnull()]

#displaying total data after cleaning out null value
print(len(movie_df))
#altern value of '\\N'

#altern value of  '\\N' on startYear to np.nan and cast column to float64
movie_df['startYear'] = movie_df['startYear'].replace('\\N',np.nan)
movie_df['startYear'] = movie_df['startYear'].astype('float64')
print(movie_df['startYear'].unique()[:5])

#altern value of  '\\N' on endYear to np.nan and cast column to float64
movie_df['endYear'] = movie_df['endYear'].replace('\\N',np.nan)
movie_df['endYear'] = movie_df['endYear'].astype('float64')
print(movie_df['endYear'].unique()[:5])

#altern value of  '\\N' on runtimeMinutes to np.nan and cast kolomnya to float64
movie_df['runtimeMinutes'] = movie_df['runtimeMinutes'].replace('\\N',np.nan)
movie_df['runtimeMinutes'] = movie_df['runtimeMinutes'].astype('float64')
print(movie_df['runtimeMinutes'].unique()[:5])
def transform_to_list(x):
    if ',' in x: 
    #ubah menjadi list apabila ada data pada kolom genre
        return x.split(',')
    else: 
    #jika tidak ada data, ubah menjadi list kosong
        return []

movie_df['genres'] = movie_df['genres'].apply(lambda x: transform_to_list(x))
print(rating_df.head())
print(rating_df.info())

#join for two table
movie_rating_df = pd.merge(movie_df,rating_df, on='tconst', how='inner')

print(movie_rating_df.head())

#displaying type data
print(movie_rating_df.info())

#shrinking table size
movie_rating_df = movie_rating_df.dropna(subset=['startYear','runtimeMinutes'])

#checking out null value
print(movie_rating_df.info())
#printing C value
C = movie_rating_df['averageRating'].mean()
print(C)
#printing mM value
m = movie_rating_df['numVotes'].quantile(0.8)
print(m)
#weighted formula function

def imdb_weighted_rating(df, var=0.8):
    v = df['numVotes']
    R = df['averageRating']
    C = df['averageRating'].mean()
    m = df['numVotes'].quantile(var)
    df['score'] = (v/(m+v))*R + (m/(m+v))*C #Rumus IMDb 
    return df['score']
    
imdb_weighted_rating(movie_rating_df)

#checking dataframe
print(movie_rating_df.head())
def simple_recommender(df, top=100):
    df = df.loc[df['numVotes'] >= m]
    df = df.sort_values(by='score',ascending=False) #urutkan dari nilai tertinggi ke terendah
    
    #taking top 100 data
    df = df[:top]
    return df
    
#printing top 25 data     
print(simple_recommender(movie_rating_df, top=25))
#Making simple recommender system of user preferences?

df = movie_rating_df.copy()

def user_prefer_recommender(df, ask_adult, ask_start_year, ask_genre, top=100):
    #ask_adult = yes/no
    if ask_adult.lower() == 'yes':
        df = df.loc[df['isAdult'] == 1]
    elif ask_adult.lower() == 'no':
        df = df.loc[df['isAdult'] == 0]

    #ask_start_year = numeric
    df = df.loc[df['startYear'] >= int(ask_start_year)]

    #ask_genre = 'all' atau yang lain
    if ask_genre.lower() == 'all':
        df = df
    else:
        def filter_genre(x):
            if ask_genre.lower() in str(x).lower():
                return True
            else:
                return False
        df = df.loc[df['genres'].apply(lambda x: filter_genre(x))]

    df = df.loc[df['numVotes'] >= m] #Mengambil film dengan m yang lebih besar dibanding numVotes
    df = df.sort_values(by='score', ascending=False)
    
    #jika kamu hanya ingin mengambil 100 teratas
    df = df[:top]
    return df

print(user_prefer_recommender(df,
                       ask_adult = 'no',
                        ask_start_year = 2000,
                       ask_genre = 'drama'
                       ))

