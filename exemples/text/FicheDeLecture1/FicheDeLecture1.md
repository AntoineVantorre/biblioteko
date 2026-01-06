IIR

Antoine Vantorre

Novembre 2025

Titre de l'article: Optimal Classification Trees

Lien de l'article:
https://proceedings.neurips.cc/paper_files/paper/2022/file/8bb0d291acd4acf06ef112099c16f326-Paper-Conference.pdf

Liste des auteurs et affiliation:
- Takeshi Kojima, — The University of Tokyo
- Shixiang (Shane) Gu, — Google Research, Brain Team
- Machel Reid, — Google Research
- Yutaka Matsuo, — The University of Tokyo
- Yusuke Iwasawa — The University of Tokyo

Nom de la conférence / revue:
https://dblp.uni-trier.de/db/conf/nips/index.html

Classification de la conférence / revue:
A*

Nombre de citations de l'article (quelle source ?):
306

Optimal Classification Trees

1. Problématique générale

Dans certains secteurs d'activité particuliers tels que la santé, les sciences sociales, l'industrie spécialisée, il est impossible d'entraîner efficacement un modèle d'IA « classique », grâce à des données brutes. Cette impossibilité s'explique par différentes causes, telles que des contraintes de confidentialité, des difficultés de collecte, le simple manque de donnée dans un secteur très spécifique, ou même hétérogénéité des données d'entraînement.

Dans de tels contextes, les approches classiques d'apprentissage supervisé sont insuffisants, et ne peuvent pas constituer une solution « solide » à la demande.

Cette contrainte pousse la recherche à explorer des stratégies alternatives : concevoir des modèles capables de raisonner sans données d'entraînement, ou avec un nombre de données d'entraînement très limités. L'idée n'est plus de faire apprendre statistiquement à partir d'un grand nombre d'exemples et d'observations, mais de trouver une solution au problème via des capacités de raisonnement, des connaissances pré-acquises et des structures linguistiques présentes dans les grands modèles de langage. Ces modèles appelés zéro-shot semblent déjà posséder des compétences latentes qui peuvent être mobilisées pour approcher une réponse pertinente, même en l'absence

totale de données d'entraînement, directement liées à la tache qui lui est dédié, cela s'explique par le fait que ces modèles ont été pré-entraînés sur des corpus gigantesques.

C'est dans ce contexte et ce but que se présente l'article étudié, qui interroge la capacité des LLMs à concevoir du raisonnement complexe en mode zéro-shot ;

Comment amener un modèle d'IA à raisonner correctement sans aucun exemple d'entraînement, simplement grâce à la formulation du prompt?

La problématique mise en lumière dans cet article ne nous amène pas à la technique du raisonnement automatique, elle interroge maintenant la nature même de la connaissance exploitée par les grands modèles de langage. Chercher à obtenir un raisonnement fiable sans aucune donnée d'entraînement spécifique, uniquement en manipulant la formulation du prompt, revient à se demander ce que les modèles ont réellement appris lors de leur long et massif pré-entraînement. Cette perspective nous force à repenser la construction traditionnelle d'un modèle d'IA.

Là où on construisait habituellement un modèle d'IA en s'appuyant sur des centaines de milliers d'exemples annotés pour déduire des « courbes » puis de la « logique » et pour finir par un algorithme complexe qui prédit une sortie en fonction des entrées, l'objectif n'est plus d'apprendre à partir de données, mais de révéler des compétences latentes déjà présentes dans le modèle grâce à son exposition, en amont, à d'immenses corpus textuels.

Ainsi cette problématique nous conduit à comprendre que le défi n'est pas tant de « créer un modèle sans données » mais de comprendre comment un modèle peut mobiliser des notions complexes, du raisonnement, des structures logiques, déjà intégrées pendant son entraînement initial. L'enjeu est de déterminer si « l'extraction » de schéma de logique peuvent être déclenchées de manière fiable, dans des contextes particuliers (utiles pour du zéro-shot) et systématiques, grâce à un simple prompt, est-t-il aussi possible d'obtenir d'un modèle d'IA zéro-shot une fiabilité semblable à un modèle classique qui a été entraîné avec un grand nombre d'exemples.

Cette question est d'autant plus importante puisque beaucoup d'applications pourraient bénéficier de modèles capables de raisonner en mode zéro-shot. Cela remet également en question la nature de « connaissances » des différentes « complexités/abstraction de notions », entre apprentissage statistique, compréhension linguistique et raisonnement artificiel.

## 2. Absence de travaux identifiée

Notre article ici se réfère à d'autres travaux antérieurs et atteste que plusieurs articles analysaient les performances des grands modèles de langage en apprentissage supervisé, en s'appuyant sur des techniques de few-shot ou de in-context learning, et qui démontre que les LMMs étaient capables de généraliser une tache à condition de recevoir plusieurs exemples structurés...

Il atteste aussi que d'autres articles analysaient les raisonnements automatiques, et s'accordent à dire que les modèles échouaient systématiquement lorsque la tache exigeait une démarche logique qui se compose de plusieurs étapes, en particulier en mode zéro-shot.

Cependant, un vide important persistait. La communauté supposait que les LLMs étaient intrinsèquement incapables de raisonner en zéro-shot. Les études n'examinaient à l'époque pas encore l'impact d'une simple instruction linguistique sur la capacité du modèle à produire une chaîne de raisonnement cohérente. Aucune étude ne s'était encore portée sur le fait d'activer un réel raisonnement interne déjà intégré dans le modèle grâce à son pré-entraînement.

Ainsi l'article met en évidence un manque concret dans les études scientifiques :

L'absence d'analyse systématique de la capacité des LLMs à générer spontanément des raisonnements étapes par étapes sans données, simplement à travers un prompt. En effet, personne

n'envisageait que le raisonnement puisse être une capacité latente, activable avec supervision. C'est sur ce vide scientifique que l'article désigne et développe.

## 3. Question de recherche

L'article nous met face à une question qui pourrait (possiblement) révolutionner une partie des modèles d'IA :

« Est ce qu'un LLM peut produire un raisonnement correct, structuré et multi-étapes en mode zéro-shot, en lui fournissant simplement un prompt tel que « Procédons étapes par étapes... »?

à son tour, de cette question découle plusieurs autres questions :

- Est ce que chaque prompt déclenche une suite d'étapes intellectuels, une suite de pensées?
- Dans le cas de raisonnement few-shot, est ce que les connaissances sont réellement acquises grâce au contexte ? Ou s'agit-il de connaissance déjà intégrées au modèle mais sous-exploitées?

- Quelles sont les limites de ces fonctionnalités ? Est ce révolutionnaire ou simplement anecdotique ?
- Le but étant de comprendre si les LLM possèdent des compétences cognitives implicites, et si c'est le cas, comment est ce qu'on pourrait les activer de manière fiable ?

## 4. Démarche scientifique mise en œuvre

Pour répondre à cette problématique, les auteurs de l'article reproduisent systématiquement une série d'experimentations sur différentes catégories de tâches de raisonnement, dans le but d'observer le comportement spontané de modèles lorsqu'on modifie le prompt dans sa structure. Il y a ici trois axes principaux à noter :

- Une procédure qui pousse le modèle à penser étape par étape en zéro-shot, puis donner une réponse finale
- Tester le modèle sur un ensemble de tâches variées, avec plusieurs types de raisonnements
- La comparaison systématique avec plusieurs méthodes existantes : (zero-shot classique/ few-shot/few-shot chain-of-thought)

De cette manière, le test rigoureux de ce phénomène peut révéler ou non une amélioration globale et donc une capacité propre présente dans les modèles d'IA l'inguistique

## 5. Mise en œuvre détaillée du dispositif expérimental

### a) Architecture du protocole Zero-Shot-CoT

Les auteurs introduisent une architecture efficace en deux étapes :

D'abord construire un prompt force le modèle à reflechire étape par étape, et façon détaillée, sans réponse finale, mais qui cherche à obtenir un cheminement de pensées explicite, qui permet de comprendre comment le modèle « reflechit »

Dans un second temps, on demande via un prompt simple d'extraire la réponse finale initialement attendue, dans un format spécial.

Ce séquencement entre développement et réponse permet de faciliter l'évaluation de l'expérimentation, et permet d'éviter toute eambiguité.

Cette méthode permet d'étudier le comportement intellectuel du modèle sans ajouter de données.

### b) Description des tâches et benchmarks

Pour obtenir un résultat cohérent, on généralise l'étude sur des jeux de données répartis en 4 familles :

- Raisonnement arithmétique
- Raisonnement symbolique

- Raisonnement logique
- Raisonnement de bon sens

Chacune de ces famille visant à exploiter différents types de raisonnement

Un raisonnement arithmétique nécessite pour sa part une suite d'étape logiques pour obtenir un résultat cohérent

Un raisonnement symbolique quant à lui nécessite des manipulations de symboles et d'état, ce qui est facile pour l'homme mais complexe pour la machine

Un raisonnement logique à son tour nécessite une compréhension d'instructions complexes par exemple

Un raisonnement de bon sens pour finir, mobilise des connaissances générales

C'est cette diversité dans l'étude qui permet de mesurer l'importance de la procédure et qui permet d'observer si le modèle est bien constitué d'une capacité de raisonnement complexe, ou si ce raisonnement est limité.

c) Méthodologie de collecte des résultats

Dans chaque famille de raisonnement, les auteurs ont calculé :

- Le taux de bonnes réponses
- La qualité et cohérences du raisonnement
- La robustesse de la méthode selon la taille du modèle
- L'impact du changement de prompt

On observe donc le cheminement de pensées du modèle, et les raisons pour lesquelles il est amené à faire des erreurs.

Ces notions abordées peuvent sembler difficile d'évaluation car présentent des notions abstraites et de ce fait complexes à définir. Ce qui implique que construire un protocole scientifique autour peut être sujet à des biais : comment déterminer la qualité d'un raisonnement ?

En effet, définir un « raisonnement cohérent ou une « bonne » explication est subjective, toutefois les auteurs parviennent à contourner ce problème en décomposant l'évaluation en plusieurs critères objectifs et reproductibles.

Dans un premier temps, ils analysent la cohérence interne de la suite de raisonnement générée. Cette cohérence globale est calculée grâce à la suite d'implications de raisonnements, une rupture logique entre deux blocs de raisonnements est considéré comme un écart observable et mesurable.

Les auteurs évaluent aussi la pertinence de chaque étape, l'idée étant de vérifier que chaque « bloc » de raisonnement a son importance dans la réponse finale ou si cela constitue une étape superficielle voir un hors sujet.

D'autre part, les auteurs évaluent la robustesse en modifiant légèrement le prompt en demandant explicitement de procéder étape par étape, afin de comparer la qualité du raisonnement

Ils testent aussi des modèles d'IA de tailles différentes, en changeant la quantité de paramètres par exemple, ce qui les amène à constater que plus le modèle est grand, plus le raisonnement est précis. Pour finir, il évaluent les différentes erreurs, entre erreur de calcul, erreur de compréhension, de raisonnement ou de sur réflexion.

C'est de cette manière que l'évaluation est en réalité objective et suis une procédure scientifique, bien que ça ne soit pas évident en comprenant la problématique

6. Résultats et avancées conceptuelles

L'observation nous met en lumière une réelle différence de performance :

Le zéro-shot-Cot multiplie la performance zero-shot par 3 à 8 selon les taches

Dans le cadre de taches arithmétiques, les performances peuvent passer de  $17\%$  à plus de  $78\%$ , ce qui temoigne d'un gain très significatif simplement e modifiant le prompt.

L'etude nous demontrte plusieurs choses telles que :

Plus le modele est grand, plus le Zero-Shot-Cot est efficace, cela pourrait s expliquer par le fait qu'un grand modele a acces a plus de connaissances latentes, ou que ces connaissances sont mieux « saisies/definies/comprises » par le modele.

Meme si le résultat est parfois erroné ou faux, le raisonnement est souvent cohérent, ce qui demontrre que le cheminement de pensé n'est pas « deduit » de laquestion et de la reponse finale, mais est bien une etape necessaire avant de trouver le résultat.

Les performances obtenues en zero-shot sont parfois comparables avec du few-shot, qui necessite quant a lui plusieurs exemples.

Avant la publication de cet rsticle, le monde scientifique considerait qu'il fallait necessairement quelques exemples pour que le modele d'ia fonctionne en multi-etapes, mais cette croyance est abolit.

Cette decouverte implique des nouvelles theories : est ce que les LLM contiennent un ensemble de schema cognits qui peut produit un raisonnement explicite, ce qui signifie donc qu'un prompt «procede etape par etape » est une façon d'activer ces schemas.

