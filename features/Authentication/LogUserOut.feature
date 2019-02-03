# language: fr

@initial-release @common @login
Fonctionnalité: Déconnecter un utilisateur

  En tant qu'utilisateur identifié sur le Shopozor,  
  je veux pouvoir m'en déconnecter  
  de telle sorte que je doive à nouveau entrer mes identifiants pour m'y reconnecter.  
  
  A tout moment, l'utilisateur peut se déconnecter.  
  
  En plus de cela, si l'utilisateur n'a pas demandé à ce que le Shopozor se souvienne de lui,
  la déconnexion s'effectue automatiquement au moment du rafraîchissement de sa session
  (cf. [Se souvenir de l'utilisateur](?feature=Authentication\RemindUser.feature)). 
  Dans ce cas-là, la session n'est pas rafraîchie et l'utilisateur est déconnecté.
  
  Scénario: L'utilisateur ferme sa session
    Etant donné un utilisateur identifié sur le Shopozor
    Lorsque l'utilisateur se déconnecte
    Alors sa session se ferme
    Et il obtient un message stipulant qu'il est déconnecté
    
  Scénario: L'utilisateur déconnecté demande des infos sur son compte
    Etant donné un utilisateur qui vient de se déconnecter
    Lorsqu'il demande au Shopozor qui il est avec son ancien token
    Alors il obtient un message stipulant qu'il n'est pas identifié