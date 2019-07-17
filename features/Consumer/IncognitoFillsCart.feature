# language: fr

@initial-release @consumer @wip @in-preparation
Fonctionnalité: Incognito remplit son Panier

  **En tant qu'Incognito,  
  je veux remplir mon Panier avec les Produits qui me plaisent
  afin de les acheter.**  

  # TODO: que se passe-t-il si l'application frontend crashe? le panier est-il associé à un token / identifiant
  # TODO: (anonyme, qui lie juste une application client au serveur sans lier un utilisateur) ?

  Contexte: Incognito est entré dans un Shop

    Etant donné un Consommateur non identifié
    Et qui est entré dans un Shop

  Scénario: Incognito ajoute un Format de Produit dans son Panier

    # à la création d'un Panier, un draftOrder doit être initialisé
    # Panier vide ==> draftOrder created
    Etant donné un Panier vide
    Et un Produit qui intéresse Incognito
    # ceci ajoute une draftOrderLine au draftOrder
    Lorsqu'il en ajoute un Format à son Panier
    Alors son Panier contient le Format de Produit désiré
    # est-ce que saleor fonctionne déjà comme ceci de base ?
    # il faudra adapter ce step de sorte à ce que fait saleor out-of-the-box
    Mais le stock du Format du Produit reste inchangé

  Scénario: Incognito supprime un Format de Produit de son Panier

  Scénario: Incognito modifie la quantité d'un Format de Produit dans son Panier

  Scénario: Incognito remplit son panier

    Les Produits d'un même panier ne peuvent appartenir qu'à un et un seul Shop.

    Etant donné un Panier vide

  # ceci correspond à créer un draftOrder et un draftOrderLine
  # draftOrderCreate
  # draftOrderComplete
  # draftOrderDelete
  # draftOrderUpdate
  # draftOrderLinesCreate --> associated with draftOrder; it receives an array of (quantity, variant)
  # draftOrderLinesCreate creates a list of orderLines; an orderLine is essentially a quantity and a variant