import streamlit as st
from database import connect_mongo, connect_neo4j
import queries_mongo
import queries_neo4j


        #  Questions MongoDB

st.set_page_config(page_title="MongoDB - Analyse Films", layout="centered")
st.title("🎬 Analyse de Films (MongoDB)")

# Connexion à la base MongoDB
db = connect_mongo()

# Liste déroulante
question = st.selectbox("📌 Choisissez une question :", [
    "1. Année avec le plus de films",
    "2. Nombre de films après 1999",
    "3. Moyenne des votes pour les films de 2007",
    "4. Histogramme du nombre de films par année",
    "5. Genres de films disponibles",
    "6. Film ayant généré le plus de revenus",
    "7. Réalisateurs ayant réalisé plus de 5 films",
    "8. Genre le plus rentable en moyenne",
    "9. Top 3 des films les mieux notés par décennie",
    "10. Film le plus long par genre",
    "11. Films avec Metascore > 80 et Revenue > 50M",
    "12. Corrélation entre durée et revenus",
    "13. Évolution de la durée moyenne par décennie"
])

# Appel de la fonction
if question == "1. Année avec le plus de films":
    result = queries_mongo.question_1(db)
    if "_id" in result:
        st.write(f"📅 Année : **{result['_id']}**")
        st.write(f"🎥 Nombre de films : **{result['count']}**")
    else:
        st.write(result["message"])

elif question == "2. Nombre de films après 1999":
    result = queries_mongo.question_2(db)
    st.write(f"🎥 Nombre total de films sortis après 1999 : **{result}**")

elif question == "3. Moyenne des votes pour les films de 2007":
    result = queries_mongo.question_3(db)
    st.write(f"⭐ Moyenne des votes pour les films de 2007 : **{result}**")

elif question == "4. Histogramme du nombre de films par année":
    import matplotlib.pyplot as plt

    annees, nb_films = queries_mongo.question_4_histogram_films_par_annee(db)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(annees, nb_films)
    ax.set_xlabel("Année")
    ax.set_ylabel("Nombre de films")
    ax.set_title("Histogramme des films par année")
    st.pyplot(fig)

elif question == "5. Genres de films disponibles":
    result = queries_mongo.question_5(db)
    st.write("🎭 Genres disponibles dans la base :")
    st.write(result)

elif question == "6. Film ayant généré le plus de revenus":
    film = queries_mongo.question_6(db)
    if "title" in film:
        st.write(f"💰 Film : **{film['title']}**")
        st.write(f"🎬 Année : {film['year']}")
        st.write(f"💵 Revenu : **{film['Revenue (Millions)']} millions de dollars**")
    else:
        st.write(film["message"])

elif question == "7. Réalisateurs ayant réalisé plus de 5 films":
    result = queries_mongo.question_7(db)
    if result:
        st.write("🎬 Réalisateurs les plus prolifiques :")
        for r in result:
            st.write(f"👨‍🎬 {r['_id']} - {r['nb_films']} films")
    else:
        st.write("Aucun réalisateur avec plus de 5 films trouvé.")

elif question == "8. Genre le plus rentable en moyenne":
    genre = queries_mongo.question_8(db)
    if "_id" in genre:
        st.write(f"💵 Genre : **{genre['_id']}**")
        st.write(f"📊 Revenu moyen : **{round(genre['revenu_moyen'], 2)} millions de dollars**")
    else:
        st.write(genre["message"])

elif question == "9. Top 3 des films les mieux notés par décennie":
    data = queries_mongo.question_9(db)
    for dec in data:
        st.subheader(f"📅 Décennie : {dec['_id']}s")
        for film in dec["top_3"]:
            st.markdown(f"- 🎬 **{film['title']}** ({film['year']}) — 🧠 Metascore : {film['Metascore']}")

elif question == "10. Film le plus long par genre":
    results = queries_mongo.question_10(db)
    st.write("🎬 Film le plus long pour chaque genre :")
    for item in results:
        st.markdown(f"**{item['_id']}** : {item['title']} ({item['year']}) — ⏱️ {item['runtime']} minutes")

elif question == "11. Films avec Metascore > 80 et Revenue > 50M":
    results = queries_mongo.question_11(db)
    if results:
        st.write("🎯 Films ayant une excellente note et un succès commercial :")
        st.dataframe(results)
    else:
        st.warning("Aucun film ne correspond à ces critères.")

elif question == "12. Corrélation entre durée et revenus":
    correlation, df = queries_mongo.question_12(db)
    
    if correlation is not None:
        st.write(f"📈 Coefficient de corrélation (durée vs revenus) : **{correlation}**")
        
        # Affichage graphique
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        ax.scatter(df["Runtime (Minutes)"], df["Revenue (Millions)"], alpha=0.5)
        ax.set_xlabel("Durée (Minutes)")
        ax.set_ylabel("Revenu (Millions)")
        ax.set_title("Corrélation entre durée et revenus des films")
        st.pyplot(fig)
    else:
        st.warning("Pas assez de données pour calculer la corrélation.")

elif question == "13. Évolution de la durée moyenne par décennie":
    df = queries_mongo.question_13(db)
    
    if not df.empty:
        st.write("📊 Évolution de la durée moyenne des films par décennie :")
        st.dataframe(df)

        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        ax.plot(df["Décennie"], df["Durée Moyenne"], marker='o')
        ax.set_xlabel("Décennie")
        ax.set_ylabel("Durée Moyenne (min)")
        ax.set_title("Durée moyenne des films par décennie")
        st.pyplot(fig)
    else:
        st.warning("Aucune donnée disponible.")
        
            #  Questions Neo4j
# --- Neo4j ---
# Connexion à la base Neo4j
driver = connect_neo4j()

st.header("🧠 Partie Neo4j")
question_neo4j = st.selectbox("Choisissez une question Neo4j :", [
    "14. Acteur ayant joué dans le plus de films",
    "15. Acteurs ayant joué avec Anne Hathaway",
    "16. Acteur ayant généré le plus de revenus",
    "17. Moyenne des votes",
    "18. Genre le plus représenté",
    "19. Films où les acteurs ayant joué avec moi ont aussi joué",
    "20. Réalisateur ayant travaillé avec le plus d’acteurs",
    "21. Films les plus connectés (par acteurs)",
    "22. Acteurs ayant joué avec le plus de réalisateurs",
    "23. Recommander un film à un acteur (selon ses genres)",
    "24. Créer des relations INFLUENCE_PAR entre réalisateurs",
    "25. Chemin le plus court entre deux acteurs",
    "26. Analyse des communautés d’acteurs"

])

    # Traitement Neo4j



if question_neo4j == "14. Acteur ayant joué dans le plus de films":
    result = queries_neo4j.question_14(driver)
    st.write(f"🎭 Acteur : **{result['acteur']}**")
    st.write(f"🎬 Nombre de films : **{result['nb_films']}**")

elif question_neo4j == "15. Acteurs ayant joué avec Anne Hathaway":
    result = queries_neo4j.question_15(driver)
    if result:
        st.write("🎭 Acteurs trouvés :")
        for acteur in result:
            st.markdown(f"- **{acteur}**")
    else:
        st.warning("Aucun acteur trouvé.")

elif question_neo4j == "16. Acteur ayant généré le plus de revenus":
    result = queries_neo4j.question_16(driver)
    if result:
        st.write(f"🎭 Acteur : **{result['acteur']}**")
        st.write(f"💵 Revenus totaux : **{round(result['total_revenus'], 2)} millions de dollars**")
    else:
        st.warning("Aucun résultat trouvé.")

elif question_neo4j == "17. Moyenne des votes":
    result = queries_neo4j.question_17(driver)
    if result:
        st.write(f"⭐ Moyenne des votes : **{round(result['moyenne_votes'], 2)}**")
    else:
        st.warning("Aucune donnée trouvée.")

elif question_neo4j == "18. Genre le plus représenté":
    result = queries_neo4j.question_18(driver)
    if result:
        st.write(f"🎭 Genre le plus fréquent : **{result['genre']}**")
        st.write(f"📊 Nombre de films : **{result['nb']}**")
    else:
        st.warning("Aucun genre trouvé.")

elif question_neo4j == "19. Films où les acteurs ayant joué avec moi ont aussi joué":
    result = queries_neo4j.question_19(driver)
    if result:
        st.write("🎬 Films trouvés :")
        for record in result:
            st.markdown(f"- **{record['film']}** ({record['annee']})")
    else:
        st.warning("Aucun film trouvé.")

elif question_neo4j == "20. Réalisateur ayant travaillé avec le plus d’acteurs":
    result = queries_neo4j.question_20(driver)
    if result:
        st.write(f"🎬 Réalisateur : **{result['realisateur']}**")
        st.write(f"👥 Nombre d'acteurs différents : **{result['nb_acteurs']}**")
    else:
        st.warning("Aucun résultat trouvé.")

elif question_neo4j == "21. Films les plus connectés (par acteurs)":
    result = queries_neo4j.question_21(driver)
    if result:
        st.write("🔗 Films ayant le plus d'acteurs en commun avec d'autres films :")
        for r in result:
            st.markdown(f"- 🎬 **{r['film']}** — {r['nb_films_connectes']} connexions")
    else:
        st.warning("Aucun résultat trouvé.")

elif question_neo4j == "22. Acteurs ayant joué avec le plus de réalisateurs":
    result = queries_neo4j.question_22(driver)
    if result:
        st.write("🎬 Top 5 des acteurs avec le plus de réalisateurs différents :")
        for r in result:
            st.markdown(f"- **{r['acteur']}** — 👨‍🎬 {r['nb_realisateurs']} réalisateurs")
    else:
        st.warning("Aucun résultat trouvé.")

elif question_neo4j == "23. Recommander un film à un acteur (selon ses genres)":
    nom_acteur = st.text_input("Entrez le nom d'un acteur (ex : Leonardo DiCaprio)")
    if nom_acteur:
        result = queries_neo4j.question_23(driver, nom_acteur)
        if result:
            st.write(f"🎯 Films recommandés pour **{nom_acteur}** :")
            for r in result:
                st.markdown(f"- 🎬 **{r['film']}** — 🎭 Genre : {r['genre']}")
        else:
            st.warning("Aucune recommandation trouvée.")

elif question_neo4j == "24. Créer des relations INFLUENCE_PAR entre réalisateurs":
    result = queries_neo4j.question_24(driver)
    st.success(result)

elif question_neo4j == "25. Chemin le plus court entre deux acteurs":
    acteur1 = st.text_input("Acteur de départ", value="Tom Hanks")
    acteur2 = st.text_input("Acteur cible", value="Scarlett Johansson")
    
    if acteur1 and acteur2:
        chemin = queries_neo4j.question_25(driver, acteur1, acteur2)
        if chemin:
            st.write(f"🔗 Chemin le plus court entre **{acteur1}** et **{acteur2}** :")
            for nom in chemin:
                st.markdown(f"- **{nom}**")
        else:
            st.warning("Aucun chemin trouvé entre ces deux acteurs.")

elif question_neo4j == "26. Analyse des communautés d’acteurs":
    if st.button("🛠️ Préparer les relations de co-joueurs"):
        msg = queries_neo4j.preparer_graphe_coacting(driver)
        st.success(msg)

    result = queries_neo4j.question_26(driver)
    if result:
        st.write("🌐 Acteurs avec le plus de co-joueurs (top 10) :")
        for item in result:
            st.markdown(f"- **{item['acteur']}** → {item['connexions']} co-joueurs")
    else:
        st.warning("Aucune donnée trouvée.")

    #  Questions transversales

st.header("🔄 Partie Transversale")
question_transversale = st.selectbox("Choisissez une question Transversale :", [
    "27. Films avec genres communs et réalisateurs différents",
    "28. Recommander des films selon les genres d’un acteur",
    "29. Relations de concurrence entre réalisateurs",
    "30. Collaborations fréquentes entre réalisateurs et acteurs"
])


if question_transversale == "27. Films avec genres communs et réalisateurs différents":
    result = queries_neo4j.question_27(driver)
    if result:
        for r in result:
            st.markdown(f"🎬 **{r['Film1']}** (*{r['Real1']}*) et **{r['Film2']}** (*{r['Real2']}*)")
            st.write(f"Genres communs : {', '.join(r['Genres'])}")
            st.markdown("---")
    else:
        st.warning("Aucun résultat trouvé.")

elif question_transversale == "28. Recommander des films selon les genres d’un acteur":
    acteur_cible = st.text_input("Entrez le nom d’un acteur :", "Anne Hathaway")
    if acteur_cible:
        recommandations = queries_neo4j.question_28(driver, acteur_cible)
        if recommandations:
            st.write(f"🎯 Recommandations pour **{acteur_cible}** :")
            for film in recommandations:
                st.markdown(f"- 🎬 **{film['Titre']}** — Genres : *{film['Genre']}*")
        else:
            st.warning("Aucune recommandation disponible pour cet acteur.")

elif question_transversale == "29. Relations de concurrence entre réalisateurs":
    result = queries_neo4j.question_29(driver)
    if result:
        st.subheader("🤝 Réalisateurs en concurrence")
        for r in result:
            st.markdown(f"- 🎬 **{r['real1']}** vs **{r['real2']}** — Genres communs : {', '.join(r['genres_communs'])}")
    else:
        st.warning("Aucune relation de concurrence trouvée.")



elif question_transversale == "30. Collaborations fréquentes entre réalisateurs et acteurs":
    result = queries_neo4j.question_30(driver)
    st.write(result)
