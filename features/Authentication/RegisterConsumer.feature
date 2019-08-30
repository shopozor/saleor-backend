#language: fr

@initial-release @auth
@fixture.signup
Fonctionnalité: Enregistrer un nouveau Consommateur

  *En tant que nouveau Consommateur du Shopozor,  
  je veux pouvoir y créer un compte avec un e-mail et un mot de passe,  
  afin d'avoir accès à toutes ses fonctionnalités.*  

  Un Consommateur n'a pas besoin de compte sur le Shopozor pour faire ses
  achats, auquel cas la spécification y fait référence en tant que "Incognito"
  (cf. fonctionnalités relatives au Consommateur pour plus de détails).
  En tant que Consommateur, un compte me permet :

  * de faire une demande pour fournir le Shopozor en tant que Producteur
  * de faire une demande pour gérer un ou plusieurs Shops en tant que Responsable
  * d'ouvrir un porte-monnaie virtuel
  * d'avoir un historique de mes achats
  * de stocker mes coordonnées géographiques pour e.g. filtrer automatiquement les Produits / Shops
    les plus proches de chez moi
  * de stocker mes coordonnées pour pré-remplir les formulaires de paiement en ligne
  * de souscrire aux notifications push du Shopozor (e.g. si une commande doit être modifiée après paiement)
  * de souscrire à des abonnements proposant certains avantages commerciaux

  ![Processus d'enregistrement](UserRegistration-fr.png)

  # Nous avons deux possibilités :
  # - soit nous enregistrons l'e-mail de l'utilisateur qui définit ensuite son mot de passe au moment
  #   de l'activation du compte
  # - soit nous enregistrons l'e-mail et le mot de passe de l'utilisateur qui valide ensuite son compte
  #   en suivant le lien d'activation du compte
  # Nous nous sommes décidés pour le dernier choix car il respecte le principe de séparation des préoccupations.
  # En effet, pour implémenter le premier choix, il faut coupler la définition du mot de passe à l'activation
  # du compte. La création du compte avec un identifiant et un mot de passe est plus compréhensible comme opération
  # de notre API que l'activation d'un compte en définissant un mot de passe. De plus, dans le premier cas, il n'est pas
  # possible d'extraire proprement la fonctionnalité de réinitialisation du mot de passe d'un utilisateur, autant
  # pour l'application client que pour le serveur ainsi qu'en termes de tests. Le premier cas implique l'usage
  # de la méthode setPassword de l'API qu'il est plus judicieux de tester en tant que fonctionnalité en tant que telle
  # sans qu'elle ne soit couplée à quoi que ce soit d'autre.

  Scénario: Un nouveau Consommateur s'enregistre avec un mot de passe conforme

    Le Consommateur potentiel commence par donner un e-mail et un mot de passe. Il devra ensuite
    valider son e-mail en visitant un lien de confirmation qui lui y aura été envoyé. Dans
    l'intervalle, un compte inactif protégé par son mot de passe lui est créé.  

    Le lien est du type

    <pre>http://www.shopozor.ch/activate/encodedUserId/token</pre>

    Lorsqu'un Consommateur inconnu fait une demande d'enregistrement avec un mot de passe conforme
    Alors il reçoit un e-mail avec un lien d'activation de compte
    Et son compte est créé
    Et son mot de passe est sauvegardé
    Mais son compte est inactif

  Scénario: Un nouveau Consommateur s'enregistre avec un mot de passe non conforme

    Lorsqu'un Consommateur inconnu fait une demande d'enregistrement avec un mot de passe non conforme
    Alors il obtient un message d'erreur stipulant que son mot de passe n'est pas conforme à la politique des mots de passe
    Et son compte n'est pas créé
    Et il ne reçoit pas d'e-mail d'activation de compte

  @fixture.user-accounts  
  Scénario: Le Consommateur a déjà un compte inactif et propose un mot de passe conforme

    Le Consommateur qui a déjà enregistré son e-mail et son mot de passe mais n'a pas réussi à
    consulter son lien de confirmation dans les temps conserve un compte inactif. Il peut alors
    refaire une demande d'enregistrement et obtenir un nouveau lien d'activation de compte.
    Il peut spécifier un mot de passe différent lors de cette nouvelle demande.

    Lorsqu'un utilisateur fait une demande d'enregistrement avec l'e-mail d'un compte inactif et un mot de passe conforme
    Alors il reçoit un e-mail avec un lien d'activation de compte  
    Et son mot de passe est sauvegardé
    Et son compte reste inactif

  @fixture.user-accounts
  Scénario: Le Consommateur a déjà un compte inactif et propose un mot de passe non conforme

    Si l'utilisateur propose un mot de passe non conforme, alors son compte ne s'active pas.
    Quoi qu'il arrive avec le mot de passe n'est pas vraiment important. Il peut être sauvé ou
    pas, il sera redéfini au moment où l'utilisateur entre un mot de passe conforme.

    Lorsqu'un utilisateur fait une demande d'enregistrement avec l'e-mail d'un compte inactif et un mot de passe non conforme
    Alors il obtient un message d'erreur stipulant que son mot de passe n'est pas conforme à la politique des mots de passe
    Et son mot de passe n'est pas sauvegardé
    Et son compte reste inactif  
    Et il ne reçoit pas d'e-mail d'activation de compte

  @HackerAbuse @fixture.user-accounts
  Scénario: Un utilisateur s'enregistre avec l'e-mail d'un compte actif

    Si un utilisateur tente de s'enregistrer avec un e-mail lié à un compte déjà actif,
    il faut notifier le Consommateur correspondant à cet e-mail et inscrire l'incident
    dans un journal car il se peut que ce Consommateur soit en train de se faire pirater
    son compte. La notification est envoyée que le pirate potentiel ait entré un mot de
    passe conforme ou non.

    Aucun message d'erreur n'est retourné afin de donner le moins d'information possible
    à un potentiel pirate.

    Lorsqu'un utilisateur fait une demande d'enregistrement avec l'e-mail d'un compte actif et un mot de passe conforme
    Alors il n'obtient aucun message d'erreur
    Et un message d'avertissement est envoyé à cet e-mail
    Et l'incident est enregistré dans un journal
    Et son mot de passe n'est pas sauvegardé

  @HackerAbuse @fixture.user-accounts
  Scénario: L'e-mail est insensible à la casse

    Si un utilisateur essaie de s'enregistrer avec un e-mail comprenant les mêmes symboles
    qu'un e-mail existant mais avec une casse différente, alors l'utilisateur doit se voir
    refuser la création de son compte pour cause d'identifiant déjà existant.

    Aucun message d'erreur ne doit être retourné car cela donnerait de l'information sur les
    comptes existants dans le Shopozor. Ce scénario est pratiquement équivalent au scénario
    précédent en termes de comportement. Il assure en plus l'unicitié d'un compte quelle que
    soit la casse de l'e-mail.

    Etant donné l'e-mail d'un compte actif dont la casse est modifiée
    Lorsqu'un utilisateur fait une demande d'enregistrement avec cet e-mail et un mot de passe conforme
    Alors il n'obtient aucun message d'erreur
    Et un message d'avertissement est envoyé à cet e-mail
    Et l'incident est enregistré dans un journal
    Et son mot de passe n'est pas sauvegardé
    Et aucun compte n'est créé avec cet e-mail

  Scénario: Le nouveau Consommateur active son compte dans les temps

    Au moment où l'utilisateur suit son lien d'activation, il s'invalide et son compte
    est activé.

    Etant donné un nouveau Consommateur qui a reçu un lien d'activation de compte
    Lorsqu'il active son compte au plus tard 1 jour après sa réception
    Alors son compte est activé
    Et son lien d'activation est invalidé
    Mais il n'est pas identifié


  Scénario: Le nouveau Consommateur active son compte une deuxième fois

    Le lien d'activation de compte ne peut être utilisé qu'une seule fois,
    dans un certain laps de temps.

    Etant donné un nouveau Consommateur qui a reçu un lien d'activation de compte
    Et qui a déjà activé son compte
    Lorsqu'il l'active pour la deuxième fois avant l'expiration du lien
    Alors il obtient un message d'erreur stipulant que le lien a expiré


  Scénario: Le nouveau Consommateur active son compte trop tard

    En plus de n'être utilisable qu'une seule fois, le lien expire après un certain temps.
    Dans ce cas, l'utilisateur reste inactif avec un mot de passe, i.e. son compte n'est pas supprimé.
    Il a toujours la possibilité d'activer son compte en refaisant une demande d'enregistrement pour
    obtenir un nouveau lien, auquel cas il aura même la possibilité de spécifier un mot de passe différent.

    Etant donné un nouveau Consommateur qui a reçu un lien d'activation de compte
    Lorsqu'il active son compte 2 jours après sa réception
    Alors il obtient un message d'erreur stipulant que le lien a expiré
    Et son compte reste inactif