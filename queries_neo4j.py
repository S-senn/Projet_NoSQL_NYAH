def question_14(driver):
    with driver.session() as session:
        result = session.run("""
            MATCH (a:Actor)-[:A_JOUE]->(f:Film)
            RETURN a.name AS acteur, COUNT(f) AS nb_films
            ORDER BY nb_films DESC
            LIMIT 1
        """)
        return result.single()


def question_15(driver):
    with driver.session() as session:
        result = session.run("""
            MATCH (anne:Actor {name: "Anne Hathaway"})-[:A_JOUE]->(film:Film)<-[:A_JOUE]-(autres:Actor)
            WHERE autres.name <> "Anne Hathaway"
            RETURN DISTINCT autres.name AS acteur
            LIMIT 10
        """)
        return [record["acteur"] for record in result]  # retourne une liste de strings

def question_16(driver):
    with driver.session() as session:
        result = session.run("""
            MATCH (a:Actor)-[:A_JOUE]->(f:Film)
            WHERE f.revenue IS NOT NULL AND f.revenue <> ""
            RETURN a.name AS acteur, SUM(toFloat(f.revenue)) AS total_revenus
            ORDER BY total_revenus DESC
            LIMIT 1
        """)
        return result.single()

def question_17(driver):
    with driver.session() as session:
        result = session.run("""
            MATCH (f:Film)
            WHERE f.votes IS NOT NULL AND f.votes <> ""
            RETURN avg(toFloat(f.votes)) AS moyenne_votes
        """)
        return result.single()

def question_18(driver):
    with driver.session() as session:
        result = session.run("""
            MATCH (f:Film)
            WHERE f.genre IS NOT NULL
            UNWIND split(f.genre, ",") AS genre
            WITH trim(genre) AS g
            RETURN g AS genre, COUNT(*) AS nb
            ORDER BY nb DESC
            LIMIT 1
        """)
        return result.single()

def question_19(driver):
    with driver.session() as session:
        result = session.run("""
            MATCH (toi:Actor {name: "Sidoine"})-[:A_JOUE]->(f1:Film)<-[:A_JOUE]-(autre:Actor)
            WHERE autre.name <> "Sidoine"
            MATCH (autre)-[:A_JOUE]->(f2:Film)
            RETURN DISTINCT f2.title AS film, f2.year AS annee
            LIMIT 15
        """)
        return list(result)

def question_20(driver):
    with driver.session() as session:
        result = session.run("""
            MATCH (r:Realisateur)-[:REALISE]->(f:Film)<-[:A_JOUE]-(a:Actor)
            RETURN r.name AS realisateur, COUNT(DISTINCT a) AS nb_acteurs
            ORDER BY nb_acteurs DESC
            LIMIT 1
        """)
        return result.single()

def question_21(driver):
    with driver.session() as session:
        result = session.run("""
            MATCH (f1:Film)<-[:A_JOUE]-(a:Actor)-[:A_JOUE]->(f2:Film)
            WHERE f1 <> f2
            WITH f1, COUNT(DISTINCT f2) AS nb_films_connectes
            RETURN f1.title AS film, nb_films_connectes
            ORDER BY nb_films_connectes DESC
            LIMIT 5
        """)
        return list(result)

def question_22(driver):
    with driver.session() as session:
        result = session.run("""
            MATCH (a:Actor)-[:A_JOUE]->(f:Film)<-[:REALISE]-(r:Realisateur)
            RETURN a.name AS acteur, COUNT(DISTINCT r) AS nb_realisateurs
            ORDER BY nb_realisateurs DESC
            LIMIT 5
        """)
        return list(result)

def question_23(driver, acteur):
    with driver.session() as session:
        result = session.run("""
            MATCH (a:Actor {name: $acteur})-[:A_JOUE]->(f1:Film)
            WHERE f1.genre IS NOT NULL
            WITH a, collect(DISTINCT f1.genre) AS genres_vus
            UNWIND genres_vus AS genre
            MATCH (f2:Film)
            WHERE f2.genre CONTAINS genre AND NOT (a)-[:A_JOUE]->(f2)
            RETURN DISTINCT f2.title AS film, f2.genre AS genre
            LIMIT 5
        """, acteur=acteur)
        return list(result)

def question_24(driver):
    with driver.session() as session:
        session.run("""
            MATCH (r1:Realisateur)-[:REALISE]->(f1:Film),
                  (r2:Realisateur)-[:REALISE]->(f2:Film)
            WHERE r1 <> r2 AND f1.genre IS NOT NULL AND f2.genre IS NOT NULL
            AND any(g1 IN split(f1.genre, ",") WHERE g1 IN split(f2.genre, ","))
            MERGE (r1)-[:INFLUENCE_PAR]->(r2)
        """)
        return "✅ Relations INFLUENCE_PAR créées avec succès."

def question_25(driver, acteur1, acteur2):
    with driver.session() as session:
        result = session.run("""
            MATCH (a1:Actor {name: $acteur1}), (a2:Actor {name: $acteur2}),
                  p = shortestPath((a1)-[:A_JOUE*]-(a2))
            RETURN [n IN nodes(p) | n.name] AS chemin
        """, acteur1=acteur1, acteur2=acteur2)
        record = result.single()
        return record["chemin"] if record else None

def preparer_graphe_coacting(driver):
    with driver.session() as session:
        session.run("""
            MATCH (a1:Actor)-[:A_JOUE]->(f:Film)<-[:A_JOUE]-(a2:Actor)
            WHERE a1.name < a2.name
            MERGE (a1)-[:A_COJOUÉ_AVEC]->(a2)
        """)
        return "🔗 Relations A_COJOUÉ_AVEC créées."

def question_26(driver):
    with driver.session() as session:
        result = session.run("""
            MATCH (a:Actor)-[:A_COJOUÉ_AVEC]-(co)
            WITH a, COUNT(co) AS nb_co
            RETURN a.name AS acteur, nb_co
            ORDER BY nb_co DESC
            LIMIT 10
        """)
        return [{"acteur": record["acteur"], "connexions": record["nb_co"]} for record in result]

def question_27(driver):
    query = """
    MATCH (f1:Film)<-[:REALISE]-(r1:Realisateur),
          (f2:Film)<-[:REALISE]-(r2:Realisateur)
    WHERE f1 <> f2 AND r1 <> r2 AND f1.genre IS NOT NULL AND f2.genre IS NOT NULL
    WITH f1, f2, r1, r2,
         [genre IN split(f1.genre, ",") WHERE genre IN split(f2.genre, ",")] AS genres_communs
    WHERE size(genres_communs) > 0
    RETURN f1.title AS Film1, r1.name AS Real1,
           f2.title AS Film2, r2.name AS Real2,
           genres_communs AS Genres
    LIMIT 20
    """
    with driver.session() as session:
        result = session.run(query)
        return [record.data() for record in result]

def question_28(driver, acteur_nom="Anne Hathaway"):
    query = """
    WITH $acteur AS acteur_cible
    MATCH (a:Actor {name: acteur_cible})-[:A_JOUE]->(f:Film)
    WHERE f.genre IS NOT NULL
    UNWIND split(f.genre, ",") AS genre
    WITH a, COLLECT(DISTINCT trim(genre)) AS genres_pref

    MATCH (f2:Film)
    WHERE f2.genre IS NOT NULL
      AND ANY(g IN genres_pref WHERE g IN split(f2.genre, ","))
      AND NOT (a)-[:A_JOUE]->(f2)
    RETURN DISTINCT f2.title AS Titre, f2.genre AS Genre
    LIMIT 10
    """
    with driver.session() as session:
        result = session.run(query, acteur=acteur_nom)
        return [record.data() for record in result]

def question_29(driver):
    with driver.session() as session:
        result = session.run("""
            MATCH (f1:Film)-[:REALISE]->(r1:Realisateur),
                  (f2:Film)-[:REALISE]->(r2:Realisateur)
            WHERE f1 <> f2 AND r1 <> r2
              AND f1.genre IS NOT NULL AND f2.genre IS NOT NULL
            WITH r1.name AS real1, r2.name AS real2,
                 [g1 IN split(f1.genre, ",") WHERE toLower(trim(g1)) IN [g2 IN split(f2.genre, ",") | toLower(trim(g2))]] AS genres_communs
            WHERE size(genres_communs) > 0
            RETURN DISTINCT real1, real2, genres_communs
            LIMIT 10
        """)
        return [record.data() for record in result]



def question_30(driver):
    with driver.session() as session:
        result = session.run("""
            MATCH (r:Realisateur)-[:REALISE]->(f:Film)<-[:A_JOUE]-(a:Actor)
            RETURN r.name AS realisateur, a.name AS acteur
            LIMIT 10
        """)
        return [record.data() for record in result]
