def question_1(db):
    pipeline = [
        {"$group": {"_id": "$year", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 1}
    ]
    result = list(db.films.aggregate(pipeline))
    
    if result:
        return result[0]  # par ex: {'_id': 2015, 'count': 248}
    else:
        return {"message": "Aucune donnée trouvée"}


def question_2(db):
    query = {"year": {"$gt": 1999}}
    count = db.films.count_documents(query)
    return count

def question_3(db):
    pipeline = [
        {"$match": {"year": 2007, "votes": {"$ne": None}}},
        {"$group": {"_id": None, "moyenne_votes": {"$avg": "$votes"}}}
    ]
    result = list(db.films.aggregate(pipeline))
    
    if result:
        return round(result[0]["moyenne_votes"], 2)
    else:
        return "Pas de données disponibles pour 2007"

def question_4_histogram_films_par_annee(db):
    pipeline = [
        {"$group": {"_id": "$year", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}  # Trie par année croissante
    ]
    result = list(db.films.aggregate(pipeline))

    # On extrait deux listes : les années et le nombre de films
    annees = [doc['_id'] for doc in result if doc['_id'] is not None]
    nb_films = [doc['count'] for doc in result if doc['_id'] is not None]

    return annees, nb_films

def question_5(db):
    pipeline = [
        # Étape 1 : Créer un champ "genres_array" à partir de la chaîne "genre"
        {"$addFields": {
            "genres_array": {"$split": ["$genre", ","]}
        }},
        # Étape 2 : Éclater les genres
        {"$unwind": "$genres_array"},
        # Étape 3 : Regrouper par genre unique
        {"$group": {"_id": "$genres_array"}},
        # Étape 4 : Trier les genres
        {"$sort": {"_id": 1}}
    ]
    result = list(db.films.aggregate(pipeline))
    genres = [doc["_id"] for doc in result]
    return genres

def question_6(db):
    result = db.films.find(
        {"Revenue (Millions)": {"$ne": None}}  # pour éviter les films sans revenu
    ).sort("Revenue (Millions)", -1).limit(1)

    film = list(result)
    return film[0] if film else {"message": "Aucun film avec un revenu connu"}

def question_7(db):
    pipeline = [
        {"$group": {"_id": "$Director", "nb_films": {"$sum": 1}}},
        {"$match": {"nb_films": {"$gt": 5}}},
        {"$sort": {"nb_films": -1}}
    ]
    result = list(db.films.aggregate(pipeline))
    return result

def question_8(db):
    pipeline = [
        {"$match": {"Revenue (Millions)": {"$ne": None}, "genre": {"$ne": None}}},
        {"$addFields": {
            "genres_array": {"$split": ["$genre", ","]}
        }},
        {"$unwind": "$genres_array"},
        {"$group": {
            "_id": "$genres_array",
            "revenu_moyen": {"$avg": "$Revenue (Millions)"}
        }},
        {"$sort": {"revenu_moyen": -1}},
        {"$limit": 1}
    ]
    result = list(db.films.aggregate(pipeline))
    return result[0] if result else {"message": "Aucun genre trouvé"}

def question_9(db):
    pipeline = [
        {"$match": {"Metascore": {"$ne": None}, "year": {"$ne": None}}},
        {"$addFields": {
            "decade": {"$subtract": ["$year", {"$mod": ["$year", 10]}]}
        }},
        {"$sort": {"decade": 1, "Metascore": -1}},
        {"$group": {
            "_id": "$decade",
            "top_films": {
                "$push": {
                    "title": "$title",
                    "Metascore": "$Metascore",
                    "year": "$year"
                }
            }
        }},
        {"$project": {
            "top_3": {"$slice": ["$top_films", 3]}
        }},
        {"$sort": {"_id": 1}}
    ]
    result = list(db.films.aggregate(pipeline))
    return result

def question_10(db):
    pipeline = [
        {"$match": {
            "Runtime (Minutes)": {"$ne": None},
            "genre": {"$ne": None}
        }},
        {"$addFields": {
            "genres_array": {"$split": ["$genre", ","]}
        }},
        {"$unwind": "$genres_array"},
        {"$sort": {"Runtime (Minutes)": -1}},
        {"$group": {
            "_id": "$genres_array",
            "title": {"$first": "$title"},
            "runtime": {"$first": "$Runtime (Minutes)"},
            "year": {"$first": "$year"}
        }},
        {"$sort": {"_id": 1}}
    ]
    result = list(db.films.aggregate(pipeline))
    return result

def question_11(db):
    query = {
        "Metascore": {"$gt": 80},
        "Revenue (Millions)": {"$gt": 50}
    }
    projection = {
        "_id": 0,
        "title": 1,
        "year": 1,
        "Metascore": 1,
        "Revenue (Millions)": 1
    }
    results = db.films.find(query, projection).sort("Metascore", -1)
    return list(results)

import pandas as pd

def question_12(db):
    query = {
        "Runtime (Minutes)": {"$ne": None},
        "Revenue (Millions)": {"$ne": None}
    }
    projection = {
        "_id": 0,
        "Runtime (Minutes)": 1,
        "Revenue (Millions)": 1
    }

    cursor = db.films.find(query, projection)
    data = list(cursor)
    df = pd.DataFrame(data)

    # Nettoyage des colonnes
    df["Runtime (Minutes)"] = pd.to_numeric(df["Runtime (Minutes)"], errors="coerce")
    df["Revenue (Millions)"] = pd.to_numeric(df["Revenue (Millions)"], errors="coerce")
    df = df.dropna(subset=["Runtime (Minutes)", "Revenue (Millions)"])

    if not df.empty:
        correlation = df["Runtime (Minutes)"].corr(df["Revenue (Millions)"])
        return round(correlation, 3), df
    else:
        return None, pd.DataFrame()

import pandas as pd

def question_13(db):
    pipeline = [
        {"$match": {
            "Runtime (Minutes)": {"$ne": None},
            "year": {"$ne": None}
        }},
        {"$addFields": {
            "decade": {"$subtract": ["$year", {"$mod": ["$year", 10]}]}
        }},
        {"$group": {
            "_id": "$decade",
            "moyenne_duree": {"$avg": "$Runtime (Minutes)"}
        }},
        {"$sort": {"_id": 1}}
    ]
    result = list(db.films.aggregate(pipeline))

    # Convertir en DataFrame pour visualisation
    df = pd.DataFrame(result)
    df.rename(columns={"_id": "Décennie", "moyenne_duree": "Durée Moyenne"}, inplace=True)
    df["Durée Moyenne"] = df["Durée Moyenne"].round(2)
    return df


