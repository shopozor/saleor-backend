# language: fr

@initial-release @common @login
Fonctionnalité: Identifier un utilisateur

  *En tant qu'utilisateur enregistré dans le Shopozor,  
  je veux pouvoir m'identifier avec un e-mail et un mot de passe  
  afin de pouvoir faire mes achats ou accéder aux outils de gestion liés à mon compte.*

  Les utilisateurs suivants sont des "clients":

  * Consommateur

  Les utilisateurs suivants sont des "administrateurs":

  * Producteur
  * Responsable
  * Rex
  * Softozor

  Le Consommateur et le Producteur n'ont aucune permission particulière.
  Ils peuvent accéder et modifier leurs données personnelles.
  Les produits font partie des données personnelles du Producteur.

  # TODO: bouger ça dans les features y relatives
  En plus de la gestion de ses données personnelles, un Responsable peut

  * accéder et modifier les produits publiés par les Producteurs affiliés à ses Shops
  * accéder à l'historique de ventes de tous ses Shops
  * verser le revenu des ventes à ses Producteurs

  En plus de la gestion de ses données personnelles, le Rex peut

  * accéder et modifier les produits publiés par n'importe quel Producteur affilié au Shopozor
  * accéder à l'historique des ventes de tous les Shops du Shopozor
  * verser le revenu des ventes à ses Shops
  * changer les permissions des utilisateurs du Shopozor

  En plus de la gestion de ses données personnelles, Softozor a tous les droits, pour des raisons de maintenance. 
  C'est un super-utilisateur.
  
  Contexte: L'utilisateur n'est pas identifié
    Etant donné un utilisateur non identifié sur le Shopozor

  Plan du Scénario: L'utilisateur n'est pas encore enregistré
    Lorsqu'un <utilisateur> s'identifie en tant que <utilisateur prétendu> avec un e-mail et un mot de passe invalides
    Alors il obtient un message d'erreur stipulant que ses identifiants sont incorrects

    Exemples:
      | utilisateur    | utilisateur prétendu |
      | client         | client               |
      | administrateur | client               |
      | client         | administrateur       |
      | administrateur | administrateur       |

  Plan du Scénario: L'utilisateur est enregistré mais entre un mot de passe erroné
    Lorsqu'un <utilisateur> s'identifie en tant que <utilisateur prétendu> avec un e-mail valide et un mot de passe invalide
    Alors il obtient un message d'erreur stipulant que ses identifiants sont incorrects

    Exemples:
      | utilisateur    | utilisateur prétendu |
      | client         | client               |
      | administrateur | client               |
      | client         | administrateur       |
      | administrateur | administrateur       |

  Plan du Scénario: L'utilisateur peut s'identifier avec son identifiant et son mot de passe

    N'importe quel administrateur peut s'identifier en tant que client.

    Lorsqu'un <utilisateur> s'identifie en tant que <utilisateur prétendu> avec un e-mail et un mot de passe valides
    Alors sa session s'ouvre pour 1 mois
    Et reste valide pendant 1 an

    Exemples:
      | utilisateur    | utilisateur prétendu |
      | client         | client               |
      | administrateur | administrateur       |
      | administrateur | client               |

  Scénario: Un client ne peut pas s'identifier en tant qu'administrateur
    Lorsqu'un client s'identifie en tant qu'administrateur avec un e-mail et un mot de passe valides
    Alors il obtient un message d'erreur stipulant que son compte n'a pas les droits d'administrateur

  Plan du Scénario: Les utilisateurs se font attribuer leur permissions
    Lorsqu'un <persona> s'identifie avec un e-mail et un mot de passe valides
    Alors sa session s'ouvre pour 1 mois
    Et reste valide pendant 1 an
    Et il obtient les permissions <permissions>
    Et il est considéré comme un <type d'utilisateur>

    Exemples:
      | persona      | permissions                                                           | type d'utilisateur |
      | Consommateur | -                                                                     | client             |
      | Producteur   | -                                                                     | administrateur     |
      | Responsable  | MANAGE_PRODUCERS                                                      | administrateur     |
      | Rex          | MANAGE_STAFF,MANAGE_USERS,MANAGE_PRODUCERS,MANAGE_MANAGERS            | administrateur     |
      | Softozor     | MANAGE_STAFF,MANAGE_USERS,MANAGE_PRODUCERS,MANAGE_MANAGERS,MANAGE_REX | administrateur     |
