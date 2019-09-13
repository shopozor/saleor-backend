# language: fr

# TODO: un Produit sans cost_price ou sans price est invalide <-- ceci est défini au moment de créer les Formats de Produit!
# TODO: pour publier un Produit, le Producteur doit avoir le droit de publier dans une liste de Shops définie par le Rex

@initial-release @producer @wip @in-preparation
Fonctionnalité: Le Producteur ajoute un Produit à son inventaire

  **En tant que Producteur,  
  je veux pouvoir ajouter des produits à mon inventaire,  
  afin de produire un catalogue de mes Produits qui me facilitera leur gestion et leur vente.**  

  Contexte: Le Producteur est identifié

    Etant donné un Producteur identifié

  Scénario: Le Producteur ajoute un nouveau Produit conforme

    Pour être accepté dans le Shopozor, un Produit doit au moins être caractérisé
    par un nom et une catégorie.

    Etant donné un nouveau Produit qui a un nom
    Et qui appartient à une catégorie
    Lorsque le Producteur l'ajoute à son inventaire
    Alors le Produit est créé
    Et lui est associé
    Et son stock est nul
    Et il n'est pas visible par les Consommateurs

  Scénario: Le Producteur ajoute un nouveau Produit sans nom

    Un Produit sans nom est invalide.

    Etant donné un nouveau Produit qui appartient à une catégorie
    Mais sans nom
    Lorsque le Producteur l'ajoute à son inventaire
    Alors il obtient un message d'erreur stipulant que son Produit n'a pas de nom
    Et le produit n'est pas créé
    Et ne lui est pas associé

  Scénario: Le Producteur ajoute un nouveau Produit sans catégorie

    Un Produit sans catégorie est invalide.

    Etant donné un nouveau Produit qui a un nom
    Mais qui n'appartient à aucune catégorie
    Lorsque le Producteur l'ajoute à son inventaire
    Alors il obtient un message d'erreur stipulant que son Produit n'a pas de catégorie
    Et le produit n'est pas créé
    Et ne lui est pas associé