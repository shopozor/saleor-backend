# language: fr

@initial-release @consumer @wip @in-preparation
Fonctionnalité: Incognito remplit son Panier

  **En tant qu'Incognito,  
  je veux remplir mon panier avec mes achats potentiels  
  de sorte à pouvoir ensuite passer à la caisse pour les payer**  

  Scénario: Incognito ajoute un Produit dans son Panier
    # TODO: à la création d'un Panier, un draftOrder doit être initialisé
    # TODO: puisque les draftOrderLines doivent être associées à un draftOrder

  Scénario: Incognito supprime un Produit de son Panier

  Scénario: Incognito modifie la quantité d'un Produit dans son Panier

  Scénario: Incognito remplit son panier

    Les Produits d'un même panier ne peuvent appartenir qu'à un et un seul Shop.

  # ceci correspond à créer un draftOrder et un draftOrderLine
  # draftOrderCreate
  # draftOrderComplete
  # draftOrderDelete
  # draftOrderUpdate
  # draftOrderLinesCreate --> associated with draftOrder; it receives an array of (quantity, variant)
  # draftOrderLinesCreate creates a list of orderLines; an orderLine is essentially a quantity and a variant