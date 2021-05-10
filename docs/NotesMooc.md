# MOOC RR:

## MODULE 1: CAHIER DE NOTES, CAHIER DE LABORATOIRE.

### intro: 
- On utilise des fichiers texte car ils sont codés en **UTF-8** et sont donc accessibles depuis les logiciels de gestion de versions et aussi les éditeurs textes dans le futur.

### spécification Markdown:
- Les fichiers texte sont limités car ils ne permettent pas de manipuler les mots pour les <u>surligner</u> / _mettre en italique_, ~~barrer~~ ...

- D'où l'utilité des langages de balisage (ex: Markdown).
	+ [wiki](https://en.wikipedia.org/wiki/Markdown)
	+ [Élaboration et conversion de documents avec Markdown et Pandoc](https://enacit.epfl.ch/cours/markdown-pandoc/)

<!-- ex: 
 - pour ajouter une image: 
	![title](url)
 - pour ajouter un blockquote:
	> blabla
	> blabla
 - pour mattre un code en inline:
	`print()`
-->
 
- On peut utiliser Pandoc pour convertir les documents Markdown en pdf / html / docx ... : 
		`pandoc test.md -o test.html`

- On peut convertir en ligne en utilisant le site: [convertisseur pdf](http://markdown2pdf.com/)

- Pour pouvoir ajouter des symboles UTF-8 uniques on utilise: [Table des symboles UTF-8](https://www.utf8-chartable.de/)


### Text Encoding Initiative:
- l'encodage en TEI (utilise XML) aide à faire un balisage pour rendre les données plus intelligentes -> regrouper après l'analyse du texte -> réduire la taille des corpus.

- La TEI permet d'introduire des informations allant bien au-delà des éléments formels (ex: [comparaison HTML/TEI](https://fr.wikipedia.org/wiki/Text_Encoding_Initiative)).

- TEI met l'accent sur la sémantique des objets représentés. 


### Les étiquettes et logiciels d'indexation pour s'y retrouver:
- On peut ajouter des étiquettes à un fichier Markdown en les mettant en commentaire (ex: < !-- keyword1 -->).

- On peut ajouter des étiquettes/métadonnées à un fichier image en les mettant en commentaire (ex: exiftool -comment="keyword1"  test.jpg).

<!-- 
Pour que l'étiquette garde un sens, il suffit d'encadrer un mot par une paire de signes de ponctuation comme « : », « ; » ou « ? ». Un label comme « :code: » sera facilement mémorisé et fera un parfait équivalent du mot-clé « code » 
-->

- Utiliser le moteur de recherche de bureau DocFetcher pour trouver les fichiers recherchés.


## MODULE 2 : LA VITRINE ET L'ENVERS DU DÉCOR : LE DOCUMENT COMPUTATIONNEL.

### Le principe des documents computationnels:
- Avoir un seul document qui contient les calculs, les résultats et des commentaires qui expliquent les choix faits.

- 3 possibilités:
	+ Jupyter: permet de gérer des notebooks et d'utiliser les langages Python3/R (déjà installé avec anaconda, il suffit juste de le lancer avec jupyter notebook
).
	+ RStrudio: pareil, mais c'est plus facile à partager ses résultats en format HTML et c'est aussi facile d'export en plusieurs formats. On peut l'utiliser avec autres langages, notamment Python, mais il y a un souci de la nonexistence des sessions (ex: il faut redéfinir les variables dans une nouvelle cellule) et donc les bouts de code ont tendance à être longs ce qui peut compliquer la tâche de l'explication.
	+ OrgMode: plus intéressant car il permet d'utiliser plusieurs langages et voire même une session shell au même temps. C'est aussi simple d'export le fichier en plusieurs formats avec des raccourcis.

#### liens utils:
- [Jupyter tips](https://www.dataquest.io/blog/jupyter-notebook-tips-tricks-shortcuts/)

- [Autres langages en Jupyter](https://gitlab.inria.fr/learninglab/mooc-rr/mooc-rr-ressources/tree/master/documents/notebooks/)


### 




