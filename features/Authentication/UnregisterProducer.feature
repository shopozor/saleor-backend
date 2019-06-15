#language: fr

@initial-release @auth @wip
Fonctionnalité: Désinscrire un Producteur

  *En tant que Responsable ou Rex,  
  je veux pouvoir supprimer le compte Producteur d'un de mes Producteurs,  
  afin que ses données de Producteur ne soient plus utilisées dans ce contexte.*  

  Un Consommateur qui est un Producteur ne doit pas pouvoir se désinscrire.
  Une fois seulement que son "compte Producteur" a été supprimé par le Responsable
  ou le Rex, il peut supprimer son compte Consommateur.

  # @fixture.user-accounts
  # Scénario: Un Producteur ne peut pas se désinscrire

  @fixture.user-accounts
  Plan du Scénario: Le Producteur n'a ni commandes en cours ni stock

    # TODO: qu'est-ce qu'il faut encore supprimer?

    Etant donné un Producteur enregistré
    Et qui n'a pas de commandes en cours
    Et dont le stock de produits est vide
    Lorsque le <persona> le désinscrit
    Alors les Produits du Producteur sont supprimés
    Mais ses données de Consommateur restent inchangées

    Exemples:
     | persona     |
     | Responsable |
     | Rex         |

  @fixture.user-accounts
  Plan du Scénario: Le Producteur a des commandes en cours

    Le Responsable ou le Rex prennent la responsabilité des commandes
    en cours du Producteur.

    # TODO: il faudra définir quelles options ont le Responsable et le Rex
    # TODO: il faudra définir comment ils peuvent gérer les commandes en cours
    # TODO: il faut également déterminer quelles mesures de sécurité il faut prendre
    # par exemple est-ce que le Responsable / Rex doit donner son mot de passe pour effectuer l'opération?

    Etant donné un Producteur enregistré
    Et qui a des commandes en cours
    Lorsque le <persona> le désinscrit
    Alors il obtient un message d'erreur stipulant que des commandes sont en cours

    Exemples:
     | persona     |
     | Responsable |
     | Rex         |

  @fixture.user-accounts
  Plan du Scénario: Le Producteur a des produits en stock

    Le Responsable ou le Rex prennent la responsabilité du stock de produits du Producteur.

    # TODO: il faudra définir quelles options ont le Responsable et le Rex
    # TODO: il faudra définir comment ils peuvent gérer les produits
    # TODO: il faut également déterminer quelles mesures de sécurité il faut prendre
    # par exemple est-ce que le Responsable / Rex doit donner son mot de passe pour effectuer l'opération?

    Etant donné un Producteur enregistré
    Et qui a des produits en stock
    Lorsque le <persona> le désinscrit
    Alors il obtient un message d'erreur stipulant que des produits sont en stock

    Exemples:
     | persona     |
     | Responsable |
     | Rex         |