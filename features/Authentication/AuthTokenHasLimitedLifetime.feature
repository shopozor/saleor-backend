# language: fr

@initial-release @login
Fonctionnalité: Le token d'identification a une durée de vie limitée

  En tant que Shopozor,
  je veux pouvoir forcer mes utilisateurs à se ré-identifier
  pour garantir leur sécurité.

  Contexte: L'utilisateur n'est pas identifié
    Etant donné un utilisateur non identifié sur le Shopozor

  Scénario: Le token d'identification a une durée de vie limitée
    Lorsqu'un utilisateur s'identifie avec un e-mail et un mot de passe valides
    Alors son token est valide pendant 1 année
    Et il doit être rafraîchi tous les 1 mois
