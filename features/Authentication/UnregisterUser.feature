#language: fr

@initial-release @auth @signup @wip
Fonctionnalité: Désinscrire un utilisateur

  *En tant qu'utilisateur enregistré,  
  je veux pouvoir supprimer mon compte  
  afin que mes données personnelles ne soient plus utilisées dans ce contexte.*  

  Pour des raisons de conformité avec la GDPR, il est possible pour un utilisateur 
  de supprimer son compte, ce qui équivaut à la suppression de ses données personnelles. 
  
  # 1. customerDelete(id)
  # staffDelete(id)
  # with id = graphene.Node.to_global_id('User', customer_user.pk), this is a base64 encoding of the User type with the user's primary key
  
  # 2. we need a mutation unregister that takes the user's password as argument along with 
  # the authentication token in the request's header; 
  # because the authentication token can't be changed, it is secure enough to assume that 
  # the email specified in the token corresponds to the account to be deleted
  # --> that would prevent a user from unregistering another user
  
  @user-accounts
  Plan du Scénario: L'utilisateur est inscrit
    
    Etant donné un <utilisateur> identifié
    Lorsqu'il se désinscrit avec un mot de passe valide 
    Et il reçoit un e-mail de confirmation de suppression de compte

    Exemples:
      | utilisateur  |
      | Consommateur |
      | Producteur   | 
      | Responsable  |
    
  @user-accounts
  Scénario: L'utilisateur confirme la désinscription dans les temps

    Les données personnelles de l'utilisateur sont supprimées, i.e. son entrée utilisateur 
    dans la base de données est supprimée définitivement. 

    # Idéalement, il faudrait que la session de l'utilisateur se ferme, i.e. 
    # que son token d'authentification soit invalidé. Ce n'est pas trivial à 
    # faire avec les JWTs. Il faut blacklister le token (cf. thématique identique 
    # pour la déconnexion d'un utilisateur: https://trello.com/c/67sBKXuk)

    # l'entrée de l'utilisateur dans le modèle User doit disparaître définitivement 
    # déjà ok dans saleor selon le code et selon les tests unitaires

    Etant donné un client qui a reçu un lien de confirmation de désinscription
    Lorsqu'il supprime son compte au plus tard 1 jour après sa réception
    Alors ses données personnelles sont supprimées
    Et le lien est invalidé

  @user-accounts
  Scénario: L'utilisateur confirme la désinscription trop tard

    Etant donné un client qui a reçu un lien de confirmation de désinscription
    Lorsqu'il supprime son compte 2 jours après sa réception
    Alors il obtient un message d'erreur stipulant que le lien a expiré 
    Et son compte n'est pas supprimé

  @user-accounts
  Scénario: L'utilisateur confirme la désinscription une deuxième fois

    Etant donné un client qui a reçu un lien de confirmation de désinscription
    Et qui a déjà supprimé son compte avec lien 
    Lorsqu'il supprime son compte à nouveau
    Alors il obtient un message d'erreur stipulant que le lien a expiré

  # need shop data
  @user-accounts 
  Scénario: Les Shops affiliés à l'utilisateur ne sont pas supprimés
    
    Si l'utilisateur est un Responsable, alors les Shops qu'il gérait jusque-là 
    ne sont pas supprimés.
    
    # pas encore implémenté

    Etant donné un Responsable qui a reçu un lien de confirmation de désinscription
    Lorsqu'il supprime son compte au plus tard 1 jour après sa réception
    Alors ses données personnelles sont supprimées
    Et le lien est invalidé
    Mais les Shops qu'il a gérés ne sont pas supprimés

  # need order data  
  @user-accounts
  Scénario: Les commandes associées à l'utilisateur ne sont pas supprimées
  
    Les commandes passées par un Consommateur ne sont pas supprimées.
  
    # déjà ok dans saleor

    Etant donné un Consommateur qui a reçu un lien de confirmation de désinscription
    Lorsqu'il supprime son compte au plus tard 1 jour après sa réception
    Alors ses données personnelles sont supprimées
    Et le lien est invalidé
    Mais ses commandes ne sont pas supprimées
  
  # need products
  @user-account
  Scénario: Les Produits associés à l'utilisateur sont supprimés
  
    Les Produits d'un Producteur sont supprimés.
  
    # pas encore implémenté, mais c'est possible à mettre en place
    
  # Le Producteur doit honorer ses commandes avant de se désinscrire
  
  # Le Producteur doit avoir tout son stock à zéro avant de se désinscrire
  
