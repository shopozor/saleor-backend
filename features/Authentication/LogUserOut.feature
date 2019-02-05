# language: fr

@initial-release @login
Fonctionnalité: Déconnecter un utilisateur

  *En tant qu'utilisateur identifié sur le Shopozor,  
  je veux pouvoir m'en déconnecter  
  de telle sorte que je doive à nouveau entrer mes identifiants pour m'y reconnecter.*  
  
  A tout moment, l'utilisateur peut se déconnecter.
  
  Scénario: L'utilisateur ferme sa session
    Etant donné un utilisateur identifié sur le Shopozor
    Lorsque l'utilisateur se déconnecte
    Alors sa session se ferme