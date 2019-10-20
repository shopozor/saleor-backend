# language: fr

@initial-release @consumer
Fonctionnalité: Un Incognito visite un Shop

  **En tant qu'Incognito,  
  je veux pouvoir entrer dans un Shop  
  pour voir quels Produits il propose et faire connaissance avec ses Producteurs.**  

  Entrer dans un Shop ne nécessite pas de compte. Un compte rend juste l'utilisation du Shopozor plus confortable.
  Les prix des Produits sont montrés de façon transparente: les catalogues montrent clairement les prix brut et net
  de chaque Produit et de chaque Format de Produit, ainsi que les taxes y correspondant. Voir [issue "Take Swiss VAT into account"](https://github.com/shopozor/backend/issues/95)
  pour plus de détails sur comment toutes ces données sont calculées.

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

  @shops.graphql
  @fixture.small-shops
  Scénario: Incognito obtient la liste des Shops

    La liste des Shops permet à Incognito de les situer sur une carte et de s'en faire
    une idée générale sur la base de leur description.

    Lorsqu'Incognito demande quels Shops il peut visiter
    Alors il obtient pour chaque Shop disponible ses coordonnées géographiques avec sa description générale

  @shopCategories.graphql
  @fixture.small-shops
  Scénario: Incognito obtient la liste des Rayons

    La visite d'un Shop se fait au travers des différents Rayons qu'il propose. Chaque Shop propose
    les mêmes Rayons mais les remplit avec des Produits différents réalisés par des Producteurs différents.

    Lorsqu'Incognito se renseigne sur les différents Rayons disponibles dans le Shopozor
    Alors il en obtient la liste

  @wip
  @shopCatalogue.graphql
  @fixture.small-shops
  Scénario: Incognito se balade dans les Rayons d'un Shop

    Incognito peut entrer dans un Shop pour y consulter son catalogue de Produits. Celui-ci
    exhibe les Produits avec leurs Producteurs et montre sous quels Formats chaque Produit
    est disponible avec leurs prix. Pour éviter de noyer Incognito dans trop d'information,
    les catalogues présentent les Produits par Catégorie. Il ne lui est par exemple pas possible
    de se procurer le catalogue complet du Shop d'un seul coup. Au lieu de cela, il peut en obtenir
    le catalogue de la boulangerie, de la fromagerie, de la boucherie, etc.

    Etant donné le Shop de son choix
    Lorsqu'Incognito en visite les Rayons
    Alors il obtient la liste de tous les Produits qui y sont publiés

  @wip
  @productDetails.graphql
  @fixture.tiny-shops
  Scénario: Chaque Produit est détaillé

    Incognito peut obtenir tous les détails de chacun des Produits appartenant
    au catalogue du Shop qu'il visite, comme e.g. une description, la durée
    de conservation, le mode de conservation, etc.

    Etant donné le Shop de son choix
    Lorsqu'Incognito y inspecte un Produit
    Alors il en obtient la description détaillée

  @wip
  @productDetails.graphql
  @fixture.tiny-shops
  Scénario: Les différentes marges et taxes de chaque Produit sont détaillées

    Tous les détails en CHF sur le prix d'un Produit sont communiqués de façon transparente.

    # We need to upgrade the current product margin query; currently, it only gives incomplete
    # percentages on the margin obtained on Products / ProductVariants

    Soit un Produit proposé dans le catalogue d'un Shop
    Lorsqu'Incognito demande la marge que s'en fait le Shopozor
    Alors il obtient le montant versé au Producteur
    Et la marge qui revient au Responsable du Shop qui l'a vendu
    Et la marge qui revient au Rex
    Et la marge qui revient à Softozor
    Et le montant de la TVA sur le Produit
    Et le montant de la TVA sur le service fourni par le Shopozor

  @wip
  @productDetails.graphql
  @fixture.tiny-shops
  Scénario: Incognito obtient les détails sur le prix d'un Produit

    Soit un Produit proposé dans le catalogue d'un Shop
    Lorsqu'Incognito en demande le prix
    Alors il obtient que le prix net correspond au montant net versé au Producteur + la marge nette du Shopozor
    Et que le prix brut correspond au prix net + la TVA sur le service du Shopozor + la TVA sur le Produit