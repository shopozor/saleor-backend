# language: fr

@initial-release @common @login
Fonctionnalité: Déconnecter un utilisateur

  *En tant qu'utilisateur identifié sur le Shopozor,  
  je veux pouvoir m'en déconnecter  
  de telle sorte que je doive à nouveau entrer mes identifiants pour m'y reconnecter.*    
  
  A tout moment, l'utilisateur peut se déconnecter.
  
  Scénario: L'utilisateur ferme sa session
    Etant donné un utilisateur identifié sur le Shopozor
    Lorsque l'utilisateur se déconnecte
    Alors sa session se ferme
    Et il obtient un message stipulant qu'il est déconnecté
    
  Scénario: L'utilisateur déconnecté demande des infos sur son compte
    Etant donné un utilisateur qui vient de se déconnecter
    Lorsqu'il demande au Shopozor qui il est avec son ancien token
    Alors il obtient un message stipulant qu'il n'est pas identifié