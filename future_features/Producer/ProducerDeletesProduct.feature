# language: fr

@producer @push-notifications @versioning @wip
Fonctionnalité: Le Producteur retire un Produit de son inventaire

  **En tant que Producteur,  
  je veux pouvoir retirer de mon inventaire tout le stock d'un Produit  
  dont la production ou la livraison ne me sera finalement plus du tout possible.**  

  Ce retrait est notifié et justifié aux Consommateurs qui ont passé une commande de ce produit.

  # Cette fonctionnalité ne fait pas partie de la première release car elle implique la mise en place
  # de beaucoup d'éléments qui demandent énormément de travail de conception. En effet, il faut mettre
  # en place un système de notifications push pour avertir les Consommateurs concernés qu'un Produit
  # est retiré de leur panier ou de leur commande en cours. Par ailleurs, il faut également implémenter
  # un système de versioning des Produits afin de garder des historiques de vente cohérents, complets
  # et utilisables. Dans ce contexte, il faut définir comment le versioning est appliqué: est-ce qu'on
  # augmente la version d'un Produit automatiquement après chaque distribution même s'ils n'a pas de
  # modification (fait peu de sens) ou est-ce la version change uniquement lorsqu'une de ses
  # caractéristiques change ?
  # Enfin, il faut également mettre en place un système de nettoyage de la base de données
  # des éléments obsolètes (il faudra dans ce contexte définir combien de temps une donnée doit être
  # gardée en archive dans notre système).
  # Finalement, il faut également décider de l'action à prendre en cas de suppression d'un Produit
  # qui fait partie d'une commande en cours (cf. https://trello.com/c/mmX3RTTV).

  Contexte: Le Producteur est identifié

    Etant donné un Producteur identifié

  Plan du scénario: Le Producteur supprime un produit jamais commandé et présent dans aucun panier

    Un Produit qui n'a jamais été mis en lien avec personne d'autre que son propre
    Producteur peut sans autres être supprimé définitivement du Shopozor. Aucun historique
    de vente  n'a besoin de cette entrée pour reconstruire une commande en cas de problème.

    Étant donné un Produit <état> de l'inventaire du Producteur
    Et qui n'est lié à aucune commande en cours
    Et qui n'est présent dans le panier d'aucun Consommateur
    Et qui n'a jamais été commandé par personne
    Lorsque le Producteur le retire de son inventaire
    Alors le Produit est supprimé définitivement du Shopozor

    Exemples:
      | état       |
      | publié     |
      | non publié |

  Plan du scénario: Le Producteur supprime un Produit archivé mais lié à aucune commande en cours et présent dans aucun panier

    Un Produit qui a déjà été commandé par le passé doit être conservé dans le Shopozor
    afin de pouvoir reconstruire les historiques de vente y relatifs.

    Étant donné un Produit <état> de l'inventaire du Producteur
    Et qui n'est lié à aucune commande en cours
    Et qui n'est présent dans le panier d'aucun Consommateur
    Mais qui a déjà été commandé dans le passé
    Lorsque le Producteur le retire de son inventaire
    Alors le Produit n'est plus visible par les Consommateurs
    Et le Produit n'est plus associé au Producteur
    Mais ses références dans l'historique des commandes restent intactes

    Exemples:
      | état       |
      | publié     |
      | non publié |

  Scénario: Le Producteur supprime un Produit jamais commandé mais présent dans un panier

    Un Produit qui n'a jamais été commandé par personne mais qui est actuellement
    présent dans un panier peut être supprimé définitivement du Shopozor. Le propriétaire
    du panier doit par contre être notifié de cette suppression.

    Étant donné un Produit publié de l'inventaire du Producteur  
    Et qui n'a jamais été commandé par personne
    Mais présent dans le panier d'un Consommateur
    Et qui doit être retiré pour une certaine raison
    Lorsque le Producteur le retire de son inventaire
    Alors le Consommateur est notifié de la suppression du Produit
    Et il n'est plus présent dans son panier
    Et il est supprimé définitivement du Shopozor

  Scénario: Le Producteur supprime un Produit archivé mais lié à aucune commande en cours et présent dans un panier

    Si le Produit a déjà un historique de vente, alors sa suppression ne peut pas être définitive.
    Il faut conserver ses références dans les ventes du passé.

    Étant donné un Produit publié de l'inventaire du Producteur  
    Et commandé par aucun Consommateur
    Mais qui a déjà été commandé dans le passé
    Et présent dans le panier d'un Consommateur
    Et qui doit être retiré pour une certaine raison
    Lorsque le Producteur le retire de son inventaire
    Alors le Consommateur est notifié de la suppression du Produit
    Et il n'est plus présent dans le panier du Consommateur
    Et il n'est plus visible par les Consommateurs
    Et il n'est plus présent dans l'inventaire du Producteur

  @toBeClarified
  Scénario: Le Producteur retire de l'inventaire un Produit en commande pour la première fois

    Un Produit commandé (donc payé par le Consommateur) peut être supprimé définitivement du
    Shopozor s'il n'a jamais été commandé auparavant par personne, i.e. s'il ne fait partie
    d'aucun historique de vente.

    Étant donné un produit publié de l'inventaire du Producteur
    Et qui n'a jamais été commandé par personne
    Mais qui est lié à une commande en cours
    Et qui doit être retiré pour une certaine raison
    Lorsque le Producteur le retire de son inventaire
    Alors le Consommateur est notifié de la suppression du Produit
    Et il ne fait plus partie de sa commande
    Et il est supprimé définitivement du Shopozor
    # Et il faut proposer une solution au Consommateur
    # see https://trello.com/c/mmX3RTTV for a discussion

  @toBeClarified
  Scénario: Le Producteur retire de l'inventaire un Produit archivé et lié à une commande en cours

    La trace d'un Produit faisant partie d'une historique de vente doit être gardée. Un tel Produit
    ne peut pas être supprimé définitivement du Shopozor. Les références vers les versions antérieures
    de ce Produit doivent être gardées.

    Étant donné un produit publié de l'inventaire du Producteur
    Et qui a déjà été commandé dans le passé
    Mais qui est lié à une commande en cours
    Et qui doit être retiré pour une certaine raison
    Lorsque le Producteur le retire de son inventaire
    Alors le Consommateur est notifié de la suppression du Produit
    Et il ne fait plus partie de sa commande
    Et il n'est plus visible par les Consommateurs
    Et il n'est plus présent dans l'inventaire du Producteur
    # Et il faut proposer une solution au Consommateur
    # see https://trello.com/c/mmX3RTTV for a discussion