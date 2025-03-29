from pymongo import MongoClient

from neo4j import GraphDatabase


def connect_mongo():
    uri = "mongodb+srv://nyahnfetgno:Ae7U2pTws@cluster0.olivw.mongodb.net/?appName=Cluster0"
    client = MongoClient(uri)
    db = client["entertainment"]  # Nom de ta base MongoDB
    return db

def connect_neo4j():
    uri = "neo4j+s://c6085e74.databases.neo4j.io"
    user = "neo4j"
    password = "erOdeAHpZ7I0FokISY646HiHhabq_Ot8EJUW07nYTHA"
    driver = GraphDatabase.driver(uri, auth=(user, password))
    return driver


# --- Insertion des films et acteurs ---
def import_films(db, driver):
    films = db.films.find()
    with driver.session() as session:
        for film in films:
            film_id = film.get("_id")
            title = film.get("title")
            year = film.get("year")
            votes = film.get("Votes")
            revenue = film.get("Revenue (Millions)")
            rating = film.get("rating")
            director = film.get("Director")
            actors_str = film.get("Actors")
            genre = film.get("genre")


            # Créer le film
            session.run("""
                MERGE (f:Film {id: $id})
                SET f.title = $title, f.year = $year, f.votes = $votes,
                    f.revenue = $revenue, f.rating = $rating, f.director = $director,  f.genre = $genre
            """, id=film_id, title=title, year=year, votes=votes,
                 revenue=revenue, rating=rating, director=director, genre=genre)

            # Créer les acteurs + relations
            if actors_str:
                actors = [a.strip() for a in actors_str.split(",")]
                for actor in actors:
                    session.run("""
                        MERGE (a:Actor {name: $name})
                        WITH a
                        MATCH (f:Film {id: $film_id})
                        MERGE (a)-[:A_JOUE]->(f)
                    """, name=actor, film_id=film_id)

            # Créer le réalisateur + relation
            if director:
                session.run("""
                    MERGE (d:Realisateur {name: $name})
                    WITH d
                    MATCH (f:Film {id: $film_id})
                    MERGE (d)-[:REALISE]->(f)
                """, name=director, film_id=film_id)

        # Ajouter les membres du projet comme acteurs liés à un film
        membres = ["Sidoine", "Estelle", "Yann"]
        film_test_id = "16"  # ID d'un film existant dans la base
        for membre in membres:
            session.run("""
                MERGE (a:Actor {name: $name})
                WITH a
                MATCH (f:Film {id: $film_id})
                MERGE (a)-[:A_JOUE]->(f)
            """, name=membre, film_id=film_test_id)

            
# --- Exécution ---
if __name__ == "__main__":
    db = connect_mongo()
    driver = connect_neo4j()
    import_films(db, driver)
    print("✅ Importation terminée avec succès.")
