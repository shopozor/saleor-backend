#language: fr

@initial-release @auth @signup @wip
Fonctionnalité: Le Rex désinscrit un Responsable

  *En tant que Rex,  
  je veux pouvoir supprimer le compte d'un Responsable  
  afin que ses données de Responsable ne soient plus utilisées dans ce contexte.*  

  Un Consommateur qui est un Responsable ne doit pas pouvoir se désinscrire de lui-même.
  Seul le Rex peut supprimer un tel compte. Ensuite, il devient un Consommateur normal et
  peut supprimer son compte de Consommateur.

  # TODO: Que fait-on si le Responsable doit payer les Producteurs?

  # TODO: Ajouter les scénarios nécessaires

  # Scénario: Un Responsable ne peut pas se désinscrire

  # need shop data
  @user-accounts
  Scénario: Les Shops affiliés à l'utilisateur ne sont pas supprimés

    Si l'utilisateur est un Responsable, alors les Shops qu'il gérait jusque-là
    ne sont pas supprimés.

    # pas encore implémenté
    # TODO: il faut gérer le cas où le Responsable est un Producteur, i.e.
    # est-ce qu'il faut que le Rex lui enlève les responsabilités une à une
    # (1. enlever le compte Responsable 2. enlever le compte Producteur)?

    Etant donné un Responsable enregistré
    Lorsque le Rex supprime son compte
    Alors ses données de Responsable sont supprimées
    Mais les Shops qu'il a gérés ne sont pas supprimés
    Et ses données de Consommateur restent inchangées
    Et ses données de Producteur restent inchangées