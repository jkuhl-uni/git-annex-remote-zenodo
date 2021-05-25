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
- les outils de package manegement comme apt sont limités dans leur fonctionnement. En effet, c'est parfois difficile pour les utilisateur de définir des packages et de les enregistrer dans la database, ce qui complique l'enregistrement et la recherche des graphes de dépendences manuellement. Mais puisque ces outils sont stateful (l'état de la machine dépend de toutes les installations qui ont été faites au fil du temps) et impératifs (l'utilisation d'une nouvelle version de la bibliothèque OpenMP par exemple cause les autres applications installées à l'utiliser et donc il y aura une modification dans les packages), alors ce n'est pas possible pour les utilisateurs de reproduire les mêmes résultats.
- L'utilisation de chroot dans le developpement des outils de package management rend la procédure fonctionnelle. En effet, chroot limite l'accès possible en un environnement isolé où tous les identificateurs sont personnalisés pour cet env (ex: les variables d'environnement, la communication inter-processus, PIDs , ..). Donc, et puisque l'on limite l'accès aux libs et aux packages, après chaque build on retrouve les mêmes résultats puisque les données de l'input sont les mêmes (fonctions). 
- Pour chaque build, on connait les identificateurs de toutes les dépendences puisque ils tous stocké dans une fichier dans /gnu/store comme des inputs. On retrouve aussi grâce à ça le diagramme de dépendances.
  

### Jeudi 20/05:
- Datalad est en dessus de git-annex (extend) et permet de manipuler les données avec des simple commandes. Il ne stocke pas les données mais il les gère comme un système de fichiers / dossiers. L'utilisateur ne voit plus les dépôts comme des entités isolées qu'il peut manipuler d'une façon limitée. 
- On peut prendre un dépôt Git ou git-annex déjà initialisé et le convertir en un dataset Datalad facilement et le manipuler soit en ligne de commande ou avec l'API python qui automatise la gestion des versions et que l'on peut intégrer dans le workflow.
  + link: http://docs.datalad.org/en/stable/generated/datalad.api.Dataset.html
- Datalad permet d'exporter les dataset comme des archives sur plusieurs remotes (ex: figshare / ora). Pour le cas de figshare qui est une database, on peut simplement utiliser la commande export-to-figshare mais puisque l'infrastructure de figshare ne permet pas d'avoir des directory, alors le stockage se fait dans une liste des fichiers mal structurée.
  + link: http://docs.datalad.org/en/stable/generated/man/datalad-export-archive-ora.html
	  https://carpentries.topicbox.com/groups/discuss/Tb776978a905c0bf8-M3d3e4bb2f0a49fdf2391282c 


### Vendredi 21/05:
- L'importance de 'Data Version Control' est évidente puisque dans le domaine de la recherche on gère des données de différents types et de grande taille et ces données peuvent changer et évoluer rapidement et donc au final on aura plusieurs version de chaque fichier et quand on compile les fichiers sources on peut avoir des différents résultats si on prend les mauvaises versions des fichiers. Mais on peut pas toujours tout mettre sur Git (surtout dans le cas des fichiers de grande taille qui évoluent exponentiellement). On gère ça alors with git-annex qui crée un directory annex où sont stockés les noms et les métadata des fichiers. Donc quand le dépôt est push sur Github, seuls les métadata sont transmises et alors les dépôts ne sont plus lourds. Les données peuvent être transmises sur des autres depôts (figshare, amazon, ...) et on peut facilement les récupérer avec une commande.
- On fait cela donc avec Datalad.

## Semaine 3 (24/05 - 30/05):

### Lundi 24/05:
Jour férié.

### Mardi 25/05:
- On peut intégrer les outils de gestion des packages et des environnements (ex: Conda) et les outils de packaging et des containers (ex: Docker et Singularity) lors de la création d'un workflow quand on execute un fichier Snakefile. 
En effet, on peut atteindre plusieurs niveaux de reproductibilité selon l'approche choisie. Si l'utilisateur décide par exemple de ne pas définir aucun env Conda et de ne pas lancer le workflow dans un container, c'est le résultat minimal de la reproductibilité, puisqu'on réussit à garder un schéma qui montre le workflow et donc quand on veut reproduire un résultat scientifique (surtout quand on a plusieurs étapes et plusieurs données d'entrée/sortie), on peut refaire l'experience avec le même workflow. Mais il y a toujours un problème dans ce cas puisqu'on gère pas les versions et on peut lancer le workflow avec des différents packages / dépendances.
On peut améliorer cela en créant un environnement Conda où on spécifie les versions que l'on souhaite récupérer et installer. C'est déjà mieux comme ça.
On peut aussi choisir de définir une image Singularity ou Docker dans le Snakefile. Dans ce cas, Snakemake récupère l'image et exécute le workflow dans ce container qui est isolé et qui peut être transmis ou stocker facilement pour être utilisé pour reproduire le résultat.
En fin, on peut fusionner les deux approches pour atteindre le meilleur résultat. Si on lance le workflow dans un container en définissant un environnement Conda alors cet env ne sera pas fortement dépendant du OS.
- On peut suivre cette approche mais en utilisant GUIX. 


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



