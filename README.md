# Projet de la dream Team

## Doc
Les documentations se trouvent en:
```
docs/fr
  Analyse_projet.md      ---> analyse du sujet, attaché au glossaire
  Projet_Encadré.md      ---> rapport
  Antoine/Journal de conception.md    -> fil de l'eau Antoine
  Elise/Journal de conception.md      -> fil de l'eau Elise
  Conception/
    Glossaire metier.md
    Glossaire technique.md
```

Les Scenarios de reference se trouve ici:
```
docs/fr/Conception/Scenarios
```

Commandes pour lancer le projet:
```
docker compose up --build
```
Pour analyser la bdd:
```
docker exec -it pje-d-db-1 psql -U myuser -d mydatabase
```

https://github.com/AntoineVantorre/biblioteko/tree/dev