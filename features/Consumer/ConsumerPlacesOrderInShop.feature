# language: fr

@initial-release @consumer @wip @in-preparation
Fonctionnalité: Un Consommateur passe une commande dans un Shop

  **En tant que Consommateur,  
  je veux pouvoir faire mes courses avec ou sans compte utilisateur  
  car je n'ai pas envie d'avoir mes données personnelles stockées dans un Shop en ligne.**  

  Plusieurs points importants au sujet des commandes:

  * Avoir un compte ou non sur le Shopozor ne limite en rien la possibilité de payer ses courses
  en ligne. Même les moyens de paiements ne sont pas limités. En effet, c'est le prestataire de
  service (six, swissbilling, twint, etc.) qui prend l'entière responsabilité de la validation d'un
  paiement. L'utilisateur entre ses coordonnées pour valider son paiement sur une interface du prestataire
  en question (par exemple son adresse pour une facture chez swissbilling). Sur la base de ces infos,
  le prestataire peut déterminer si l'utilisateur est blacklisté ou si son compte bancaire contient
  les provisions nécessaires pour honorer la transaction.

  * Le stock d'un Produit est mis à jour chez le Producteur une fois que le Consommateur passe à la caisse avec
  un panier le contenant. Par exemple, si un Consommateur a mis 1kg de carottes dans son panier, alors cette quantité
  est retirée du stock du Producteur correspondant au moment où le Consommateur passe à la caisse. De cette façon, un
  autre Consommateur ayant pris un Format de ce Produit dans son panier serait notifié s'il ne pouvait plus le prendre.
  C'est ce qui se passerait si deux Consommateurs prenaient dans leurs paniers le dernier Format d'un même Produit.
  Seul l'un de ces Consommateurs pourra l'acheter, au final. Le Shopozor favorise le Consommateur qui passe en
  premier à la caisse. Si le paiement de ce Consommateur ne peut pas être validé ou n'est pas effectué dans un certain
  laps de temps, alors le stock du Producteur est rétabli et le Format du Produit en question peut être repris
  dans le panier d'un autre Consommateur.
  Il est plus sûr de procéder ainsi que d'effectuer cette opération sur le stock du Producteur au moment du paiement.
  En effet, si le stock du Producteur était mis à jour sur paiement d'une commande, le premier Consommateur à payer sa
  commande obtiendrait le Format du Produit présent en une seule et dernière unité. Les autres Consommateurs ayant
  ce Format dans leur commande verraient leur commande modifiée au moment du paiement, peut-être même durant la validation
  du paiement par le prestataire de service de paiement, ce qui nécessiterait une opération de remboursement de la part
  du Shopozor, impliquant des frais de transaction, ce qui n'est pas désiré.  
  Dans le cas du Format de Produit libre (e.g. le Producteur a 800g de marchandise qu'il vend au poids), lorsque e.g.
  un client réserve 600g et un autre 400g, et qu'un total de 800g est disponible, alors le second qui passe à la caisse
  verra son panier modifié.

  * Une commande ne peut être reliée qu'à un et un seul Shop. Il n'est pas
  possible de regrouper des Produits de Shops différents dans une même
  commande.


  # TODO: à quel moment une commande se lie-t-elle à un utilisateur? <-- au moment du checkout, car c'est là que le client
  # envoie une requête au serveur pour communiquer le contenu de la commande (à vérifier dans saleor comment c'est fait!)

  Scénario: Incognito passe à la caisse

    Entrer dans un Shop ne nécessite pas de compte. Un compte rend juste
    l'utilisation du Shopozor plus confortable.
    # TODO: ne pas oublier de créer un numéro de commande

  # TODO: needs Consumer fixture
  Scénario: Le Consommateur passe à la caisse
    # TODO: La différence est ici que la commande est reliée au Consommateur dans la base de données
    # TODO: ne pas oublier de créer un numéro de commande

  # Passer une commande signifie être passé à la caisse et avoir fait valider le paiement par le prestataire de services de paiements.

