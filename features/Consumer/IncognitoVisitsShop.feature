# language: fr

@initial-release @consumer @wip
Fonctionnalité: Un Incognito visite un Shop

  **En tant qu'Incognito,  
  je veux pouvoir entrer dans un Shop  
  pour voir quels Produits il propose et faire connaissance avec ses Producteurs.**  

  Entrer dans un Shop ne nécessite pas de compte. Un compte rend juste l'utilisation du Shopozor plus confortable.

  # Il y a essentiellement deux possibilités pour récupérer le catalogue des Produits du serveur:
  # 1. Eager mode: aller chercher toutes les données disponibles. La réponse à la requête est dans ce cas assez grosse, mais
  #    il n'y a qu'une seule requête. Au chargement de l'interface du Consommateur, cette requête serait donc
  #    effectuée afin de représenter sur une carte tous les Shops disponibles avec leurs Produits, même si seulement les Shops
  #    sont représentés sur une carte. Cliquer sur un Shop pour en afficher les Produits ne demanderait pas d'effort supplémentaire.
  #    Dans le cas extrême où il y aurait une très grosse quantité de données à charger, la page aurait un temps de chargement élevé.
  # 2. Lazy mode: aller chercher les données au compte-goutte, faire plus de requêtes avec moins de données. L'affichage des Shops
  #    sur la carte ne nécessiterait qu'une toute petite requête qui n'irait chercher que les coordonnées de chaque Shop.
  #    Pour afficher les Produits d'un Shop en particulier, une nouvelle requête devrait être lancée pour déterminer quels
  #    Produits appartiennent à ce Shop. Chaque clic menant à une action qui a besoin d'information nécessiterait l'envoi
  #    d'une requête.
  # Au fur et à mesure des releases, les interfaces utilisateurs seront transformées en PWAs, avec un stockage local de données,
  # de telle sorte qu'une information qui a déjà été demandée n'aura pas besoin d'être redemandée au serveur. Nous synchroniserions
  # la base de données locale de l'application client avec le serveur en arrière-plan. Les souscriptions graphql mettraient à jour
  # la base de données locale en temps réel.
  # La technologie supportant graphql dans notre serveur est toutefois graphene, qui est réputée pour être lente. En d'autres termes,
  # moins les interfaces utilisateurs font de requêtes, mieux c'est. Si, toutefois, ces requêtes se font en arrière-plan, l'utilisateur
  # ne devrait pas remarquer de lag, sauf au premier chargement des données qu'il désire.
  # Dans les premiers mois d'utilisation du Shopozor, nous ne nous attendons pas à avoir une quantité pharaonique de données à
  # représenter sur nos interfaces et nous n'aurons pas de worker threads à disposition.
  # Nous avons décidé de partir sur le lazy mode. Des benchmarks seront effectués pour valider l'approche.

  Contexte: L'utilisateur est Incognito

    Etant donné un utilisateur non identifié sur le Shopozor

  @fixture.small-shops
  Scénario: Incognito obtient la liste des Shops

    La liste des Shops permet à Incognito de les situer sur une carte et de s'en faire
    une idée générale sur la base de leur description.

    Lorsqu'Incognito demande quels Shops il peut visiter
    Alors il obtient pour chaque Shop disponible ses coordonnées géographiques avec sa description générale

  @fixture.small-shops
  Plan du Scénario: Incognito visite un Shop

    Incognito peut entrer dans un Shop pour y consulter son catalogue de Produits. Celui-ci
    exhibe les Produits avec leurs Producteurs et montre sous quels Formats chaque Produit
    est disponible avec leurs prix. Pour éviter de noyer Incognito dans trop d'information,
    les catalogues présentent les Produits par Catégorie. Il ne lui est par exemple pas possible
    de se procurer le catalogue complet du Shop d'un seul coup. Au lieu de cela, il peut en obtenir
    le catalogue de la boulangerie, de la fromagerie, de la boucherie, etc.

    Etant donné qu'Incognito est entré dans un Shop
    Lorsqu'il en visite le stand <catégorie>
    Alors il obtient la liste de tous les Produits qui y sont publiés

    Exemples:
      | catégorie       |
      | Boissons        |
      | Boucherie       |
      | Boulangerie     |
      | Epicerie        |
      | Fruits          |
      | Laiterie        |
      | Légumes         |
      | Nettoyages      |
      | Soins corporels |
      | Traiteur        |

  @fixture.small-shops
  Scénario: Chaque Produit est détaillé

    Incognito peut obtenir tous les détails de chacun des Produits appartenant
    au catalogue du Shop qu'il visite, comme e.g. une description, la durée
    de conservation, le mode de conservation, etc.

    Etant donné qu'il est entré dans un Shop
    Lorsqu'Incognito y inspecte un Produit
    Alors il en obtient la description détaillée

# TODO: pour des raisons purement visuelles, il est nécessaire de pouvoir obtenir la liste des catégories et des types de produits (description, image)