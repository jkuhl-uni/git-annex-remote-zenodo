# Journal:

## Semaine 1 (10/05 - 16/05):

### Lundi 10/05:
- J'ai revu des points git-annex pour se refamiliariser avec cet outil.
- J'ai mis à jour le fichier __notes.md__ pour ajouter des liens utils et des explications pour des outils dont j'aurai besoin dans le futur dans le cadre du stage.
- J'ai commencé la lecture du cours MOOC Recherche Reproductible.
- J'ai lu les leçons du Module 1 et j'ai pris des notes des aspects intéressants.
- J'ai lu la moitié des éléments du module 2 et pris des notes.
- J'ai regardé des exemples des journaux et des blogs des anciens étudiants qui ont utilisé Org-mode/ Rstudio/ Jupyter pour avoir des bons résultats pratiques.

### Mardi 11/05:
- J'ai continué la lecture des séquences du Module 2.
- Regardé des parties de la visio-conférence de la Journée SIF Recherche Reproductible et pris des notes.

### Mercredi 12/05:
- Regardé la deuxième moitié de la visio-conférence de la Journée SIF Recherche Reproductible.
- Lu des articles scientifiques pour mieux assimiler les outils GUIX et Snakemake et comprendre leur utilité dans le cadre de la recherche reproductible.
- Discuté avec Mr. Vincent Danjean sur des éléments du sujet. 

### Jeudi 13/05:
Jour férié.

### Vendredi 14/05:
- J'ai fait des tutos pour apprendre comment écrire des fichiers Snakemake.
- J'ai lu des articles pour mieux assimiler l'utilité des outils comme Docker dans le cadre de la RR.

## Semaine 2 (17/05 - 23/05):

### Lundi 17/05:
- Atelier reproductibilité des environnements logiciels (Jour 1): l'utilité et l'importance de la recherche reproductible est évidente et c'est pour cette raison que c'est nécessaire de prendre en considération le développement des environnements logiciels aussi et pas seulement le côté workflow / outils d'analyse. Ainsi, l'utilisation de GUIX ne se manifeste pas seulement dans le cas des utilisateurs individuels qui cherchent à retrouver les même résultats des calculs qu'ils avaient trouvé il y a des années, mais aussi dans le cas des centres de recherche où c'est intéressant de pouvoir redéployer les clusters et les rendre productibles. 
  + link: https://hpc.guix.info/events/2021/atelier-reproductibilit%C3%A9-environnements/
- J'ai suivi des tutorials Zenodo pour publier des articles sur la base de données en utilisant l'API. Au début, j'ai vérifié l'accès à l'API (GET query), en suite, j'ai utilisé des commandes simples cURL pour créer un nouveau dépôt (POST query) et en fin j'ai publié des fichiers sur ce dépôt (PUT query).
  + link: https://felipecrp.github.io/2021/01/01/uploading-to-zenodo-through-api.html
- J'ai fait un deuxième tutorial pour publier des articles sur l'API mais cette fois j'ai utilisé python. La démarche était la même.
  + link: https://developers.zenodo.org/?python#quickstart-upload
- J'ai aussi publié un article manuellement comme test sur le sandbox Zenodo aussi.

### Mardi 18/05:
- Atelier reproductibilité des environnements logiciels (Jour 2): Une première présentation qui explique comment se servir de Docker et l'outil Snapshot Archive de Debian pour générer un env logiciel permettant d'exécuter des programmes où il y avait des anciennes versions des dépendances. En effet, après avoir récupéré les bonnes versions avec Snapshot Debian (en utilisant les dates des packages), on peut générer une nouvelle image Docker avec un Dockerfile où on récupère les bonnes dépendances et on peut ainsi créer un container avec cette image pour refaire l'expérience dans cet environnement. La deuxième présentation portait sur l'inévitabilité du choix de passer de module à NIX / GUIX et une comparaison entre les deux selon des cas d'usage. Finalement, l'importance de la programmation lettrée a été expliqué et elle se manifeste dans son capacité à faciliter les tâche du calcul intensif dans le cadre de la recherche scientifique puisqu'elle aide à grouper l'exécution des programmes, les explications, et les graphes et résultats dans un même fichier que l'on peut exporter et analyser facilement. Un outil qui mène à ce résultat est Org mode, et quand c'est couplé avec un environnement géré par GUIX, on s'approche de plus en plus au meilleur résultat reproductible.
  + link: https://hpc.guix.info/events/2021/atelier-reproductibilit%C3%A9-environnements/
- Je continue à lire un peu plus sur les logiciels que l'on va utiliser dans le reste de ce sujet et donc cet article scientifique écrit par Ludovic Courtès et Ricardo Wurmus sur le logiciel GUIX et comment il permet de gérer des environnements reproductibles. Et puisque les packages disponibles sont dans l'ordre de 2000, c'est util pour les utilisateurs qui veulent reproduire le même env sur un autre système HPC (cela peut être aussi intéressant pour les rechercheurs qui analysent l'impact du hardware sur la performance du software).
  + link: https://link.springer.com/content/pdf/10.1007%2F978-3-319-27308-2_47.pdf

### Mercredi 19/05:


### Jeudi 20/05:


### Vendredi 21/05:


## Semaine 3 (24/05 - 30/05):

### Lundi 24/05:

### Mardi 25/05:

### Mercredi 26/05:

### Jeudi 27/05:

### Vendredi 28/05:


## Semaine 4 (31/05 - 06/06):

### Lundi 31/05:

### Mardi 01/06:

### Mercredi 02/06:

### Jeudi 03/06:

### Vendredi 04/06:


## Semaine 5 (07/06 - 13/06):

### Lundi 07/06:

### Mardi 08/06:

### Mercredi 09/06:

### Jeudi 10/06:

### Vendredi 11/06:


## Semaine 6 (14/06 - 20/06):

### Lundi 14/06:

### Mardi 15/06:

### Mercredi 16/06:

### Jeudi 17/06:

### Vendredi 18/06:


## Semaine 7 (21/06 - 27/06):

### Lundi 21/06:

### Mardi 22/06:

### Mercredi 23/06:

### Jeudi 24/06:

### Vendredi 25/06:


## Semaine 8 (28/06 - 04/07):

### Lundi 28/06:

### Mardi 29/06:

### Mercredi 30/06:

### Jeudi 01/07:

### Vendredi 02/07:


## Semaine 9 (05/07 - 11/07):

### Lundi 05/07:

### Mardi 06/07:

### Mercredi 07/07:

### Jeudi 08/07:

### Vendredi 09/07:


## Semaine 10 (12/07 - 18/07):

### Lundi 12/07:

### Mardi 13/07:

### Mercredi 14/07:

### Jeudi 15/07:

### Vendredi 16/07:


## Semaine 11 (19/07 - 25/07):

### Lundi 19/07:

### Mardi 20/07:

### Mercredi 21/07:

### Jeudi 22/07:

### Vendredi 23/07:


## Semaine 12 (26/07 - 31/07):

### Lundi 26/07:

### Mardi 27/07:

### Mercredi 28/07:

### Jeudi 29/07:

### Vendredi 30/07:



