import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Cargar datos de productos
metadata = pd.read_csv('products.csv', low_memory=False)

# Calcular media de calificacion
C = metadata['Qualification'].mean()

# Calcular el número mínimo de votos necesarios para estar en la tabla
m = metadata['Votes'].quantile(0.80)

# Filtrar todos los productos calificadas en un nuevo DataFrame
q_products = metadata.copy().loc[metadata['Votes'] >= m]

# Función que calcula la calificación ponderada de cada producto
def weighted_rating(x, m=m, C=C):
    v = x['Votes']
    R = x['Qualification']
    # Cálculo basado en la fórmula IMDB
    return (v/(v+m) * R) + (m/(m+v) * C)

q_products['score'] = q_products.apply(weighted_rating, axis=1)

q_products = q_products.sort_values('score', ascending=False)

# print(q_products[['Title', 'Votes', 'Qualification', 'score']].head(5))

# print(metadata['Description'].head())

tfidf = TfidfVectorizer(stop_words='english')

metadata['Description'] = metadata['Description'].fillna('')

tfidf_matrix = tfidf.fit_transform(metadata['Description'])

# print(tfidf_matrix.shape)
# print(tfidf.get_feature_names()[5000:5010])

cosine_similarity = linear_kernel(tfidf_matrix, tfidf_matrix)

# print(cosine_sim.shape)
# print(cosine_similarity[1])

indices = pd.Series(metadata.index, index=metadata['Title']).drop_duplicates()

# print(indices[:5])

def get_recommendations(title, cosine_similarity=cosine_similarity):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_similarity[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    return metadata['Title'].iloc[movie_indices]


# print(get_recommendations('Bicicicleta Roadmaster Hurricane 29  Shimano Revoshift 21vel'))
# print(get_recommendations('Rodillos En Acero Inoxidable Sin Desmontar La Llanta'))
# print(get_recommendations('Cinta Antipinchazos Banda Bici Mtb-ruta 26  27.5  29  700c'))
# print(get_recommendations('Guante De Fútbol Golty Competicion Antifracturante'))
# print(get_recommendations('Guayos Tipo Bota Hombre Cancha Sintética Futbol 5 Tenis'))
# print(get_recommendations('Jersey. Nba. Baloncesto. Miami Wade'))
# print(get_recommendations('Tablero De Baloncesto En Acrílico 90cm X 120cm'))