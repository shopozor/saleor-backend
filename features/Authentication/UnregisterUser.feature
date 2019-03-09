#language: fr

@initial-release @auth @signup
Fonctionnalité: Désinscrire un utilisateur

  *En tant qu'utilisateur enregistré,  
  je veux pouvoir supprimer mon compte  
  afin que mes données ne soit plus utilisées dans ce contexte.*  

  Pour des raisons de conformité avec la GDPR, le Shopozor offre la possibilité 
  à ses utilisateurs de supprimer leur compte, ce qui équivaut à la suppression 
  des données personnelles. 
  
  # customerDelete(id)
  # staffDelete(id)
  # with id = graphene.Node.to_global_id('User', customer_user.pk), this is a base64 encoding of the User type with the user's primary key
  
  Scénario: L'utilisateur n'est pas inscrit

    Afin de ne pas dévoiler quels identifiants sont reconnus par le Shopozor, 
    il faut indiquer un succès de la désinscription dans le cas où l'identifiant 
    à désinscrire n'est pas reconnu par le Shopozor. Si on indique que l'opération 
    a échoué, un hacker potentiel peut déduire que les identifiants n'existent pas 
    et utiliser cette information à son avantage.

    Etant donné un utilisateur non inscrit sur le Shopozor
    Lorsqu'il se désinscrit
    Alors il obtient un message stipulant qu'un e-mail lui a été transmis
    Et le Shopozor enregistre l'incident dans son journal
    
  Scénario: L'utilisateur est inscrit
    
    Etant donné un utilisateur identifié sur le Shopozor
    Lorsqu'il se désinscrit 
    Alors il obtient un message stipulant qu'un e-mail lui a été transmis
    Et il reçoit un e-mail de confirmation de suppression de compte

  Scénario: L'utilisateur confirme la désinscription dans les temps
    
    # TODO: on ne peut pas vérifier que le mail a été envoyé il y a moins d'une heure
    # ceci devrait plutôt être vérifié dans des tests unitaires / d'intégration
    # Il faudrait donc plutôt vérifier que le mail vient d'être reçu ... il faut ajouter 
    # des tests unitaires qui vérifient que ça marche si le mail a été ENVOYE il y a moins d'une heure
    Etant donné un e-mail de confirmation de désinscription reçu il y a moins d'une heure 
    Et qui n'a pas encore été lu
    Lorsque l'utilisateur consulte le lien de confirmation qu'il contient
    Alors il obtient un message stipulant que la désinscription a été effectuée avec succès
    Et son compte est supprimé
    Et sa session se ferme
    Et le lien est invalidé

  # TODO: --> unit / integration test  
  Scénario: L'utilisateur confirme la désinscription trop tard
    Etant donné un e-mail de confirmation de désinscription envoyé il y a plus d'une heure
    Lorsqu'un utilisateur visite le lien de confirmation
    Alors il obtient un message d'erreur stipulant que le lien a expiré 
    Et son compte n'est pas supprimé

  Scénario: L'utilisateur confirme la désinscription une deuxième fois
    Etant donné un e-mail de confirmation de désinscription déjà lu
    Lorsqu'un utilisateur le visite
    Alors il obtient un message d'erreur stipulant que le lien a expiré
    Et son compte n'est pas supprimé
    
  Scénario: Les données personnelles de l'utilisateur sont supprimées
    
    Les données personnelles de l'utilisateur sont supprimées, i.e. son entrée utilisateur 
    dans la base de données est supprimée définitivement. 
    
    # l'entrée de l'utilisateur dans le modèle User doit disparaître définitivement 
    # déjà ok dans saleor selon le code et selon les tests unitaires
    
  Scénario: Les Shops affiliés à l'utilisateur ne sont pas supprimés
    
    Si l'utilisateur est un Responsable, alors les Shops qu'il gérait jusque-là 
    ne sont pas supprimés.
    
    # pas encore implémenté, mais c'est possible à mettre en place
    
  Scénario: Les commandes associées à l'utilisateur ne sont pas supprimées
  
    Les commandes passées par un Consommateur ne sont pas supprimées.
  
    # déjà ok dans saleor
  
  Scénario: Les Produits associés à l'utilisateur sont supprimés
  
    Si l'utilisateur est un Producteur, alors ses Produits sont supprimées.
  
    # pas encore implémenté, mais c'est possible à mettre en place