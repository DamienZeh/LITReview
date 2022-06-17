![Alt text](https://github.com/DamienZeh/LITReview/blob/main/accounts/static/bookreviews/logo.png)<br>

# Gestionnaire de demandes et critiques de livres

- Projet permettant de créer et gérer des publications,<br>
 pour demander des avis sur des livres et créer des critiques de ceux-ci.<br/>
 Il fonctionne sur un serveur local.<br><br>



## Téléchargement et installation 


- Avec votre terminal, allez dans le dossier ou vous souhaitez placer le projet.<br/> 
Exemple : ``cd C:\Users\damie\Documents\Python_Project``
- Copiez le projet : ``git clone https://github.com/DamienZeh/LITReview.git``
- Puis, allez dans ce projet : ``cd LITReview\``
- puis créez l’environnement virtuel avec  ``python -m venv env``<br/>
	_(‘env’ est le nom que j’ai sur mon environnement virtuel, il est aussi noté dans le gitignore.)_
- Puis activez le : ``.\env\Scripts\activate`` (pour windows)<br/>
ou ``source env\bin\activate`` (pour linux)<br/>
	_(Vous avez maintenant un ‘(env)’ d’affiché, l'environnement est activé)_<br>
cette commande devra être lancée à chaque redémarrage du terminal.
- Puis, l’installation  des packages présent dans le requirements.txt:<br> ``pip install -r requirements.txt`` <br/><br>

## Description

### Démarrage

Lancez simplement le  **serveur local**, avec la commande « ``python manage.py runserver`` ».<br/>
A partir de la, votre terminal affichera le lien à cliquer :<br> "http://127.0.0.1:8000/", qui vous amènera à la page de connexion du site.<br>
Le fichier de données db.sqlite3 sera automatiquement chargé.<br><br>

### Le site
Cette application web permet de créer des critiques et des demandes de critiques de livres.<br/>
L'utilisateurs s'inscrit, puis peut participer.<br/>
Il pourra alors s'abonner à d'autres utilisateurs, voir leurs publications, et gérer les siennes.<br/>
Voici les différentes pages du site :

- **Créer un compte/ s'inscrire**<br/>
L'utilisateur se connecte avec ses identifiants, ou s'inscrit, s'il n'en pas encore.<br/><br/>

- **La page flux**<br/>
Une fois connecté, l'utilisateur peut créer un ticket(une demande de critique),<br/>
ou une review(une critique).<br/>
Il peut aussi créer une review sans être une réponse à un ticket.<br/>
Il peut voir ses tickets, ses reviews,
et celles de ceux à qui il est abonné.<br/>
Il peut répondre aux tickets de ceux à qui il est abonné, par une review.<br/>
Il peut voir les reviews de ses propres tickets écrits par les autres utilisateurs,<br/>
même s'il n'est pas abonné à eux.<br>
Il ne peut y avoir qu'une seule review par ticket.<br><br/>

- **La page posts**<br/>
L'utilisateur peut voir et gérer ses propres publications (tickets, reviews).<br>
Il peut les modifier ou les supprimer.<br/><br/>

- **La page d'abonnement**<br/>
C'est ici que l'utilisateur va pouvoir taper le nom des personnes qu'il souhaite suivre.<br/>
Il verra aussi le nom des personnes qu'il suit déjà, <br>
et aussi le nom de ceux qui le suivent, lui.<br>
Il aura la possibilité de se désabonner de n'importe qu'elle personne qu'il suit.<br/><br/>

- **Se déconnecter**<br/>
A tout moment, l'utilisateur peut se déconnecter.<br>
Il sera alors rediriger à la page de connexion.<br/><br/>

- **Administrateur**<br/>
Si vous rajoutez ``admin`` à l'adresse générée dans le terminal, donc :<br>
"http://127.0.0.1:8000/admin", et que vous avez des droits administrateurs, <br>
il vous sera alors possible de gérer tickets, reviews et abonnements,<br>
directement sur l'interface d'administration.<br/><br/>

**Détail sur les données présentes**<br>
Le fichier db.sqlite3 déjà présent, contient, pour l'exemple des utilisateurs fictifs,<br>
 qui ont publié plusieurs tickets et reviews, et ont différents abonnements, <br>
 pour vous montrez clairement le fonctionnement.<br><br>

 Vous pouvez bien évidemment créer vos propres profils, ce qui est le but,<br> 
 mais si jamais vous voulez tester l'application avec ces profils fictifs,<br>
  qui donnent un aperçu clair du fonctionnement de l'application,<br> voici quelques identifiants :<br>
- Exemple d'utilisateurs fictifs : ``alan``, ``ellie``, ``ian``, ``john`` et ``dennis``;<br>
- En super utilisateur (pour l'administrateur) : ``damien`` ;<br>
- Pour des raisons de simplicité pour ces exemples,<br> ils ont tous le même mot de passe... ``password`` ;<br><br>

### Vérification du code
- Pour faire un contrôle du code avec **flake8** (avec max lenght à 79), tapez :<br/>
``flake8 --max-line-length 79 --exclude=env`` ;<br/><br/>

## Auteur

* **Damien Hernandez** _alias_ [DamienZeh](https://damienhernandez.fr/)


