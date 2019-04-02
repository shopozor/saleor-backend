# language: fr

@initial-release @auth @wip
Fonctionnalité: L'utilisateur réinitialise son mot de passe 

  *En tant qu'Utilisateur,  
  je veux pouvoir réinitialiser mon mot de passe  
  lorsque je l'ai oublié.*  
  
  ![Processus de réinitialisation du mot de passe](ResetUserPassword-fr.png)

  @user-accounts
  Plan du Scénario: Le client fait une demande de réinitialisation de mot de passe 

    Le mot de passe actuel du client est conservé jusqu'au moment où il en donne un autre.

    # On utilise la mutation passwordReset(email). 
    # Le lien de réinitialisation suit le même pattern que celui de l'activation d'un compte.

    Lorsqu'un <utilisateur> enregistré réinitialise son mot de passe 
    Alors il reçoit un e-mail de réinitialisation de mot de passe
    Et son mot de passe reste inchangé

    Exemples:
      | utilisateur  |
      | Consommateur |
      | Producteur   |
      | Responsable  |
      | Rex          |
      | Softozor     |

  @HackerAbuse
  Scénario: Un utilisateur inconnu fait une demande de réinitialisation de mot de passe 

    La demande de réinitialisation du mot de passe par un utilisateur inconnu n'affecte 
    en rien le système. L'incident est simplement rapporté dans un journal à des fins 
    d'analyse.

    Lorsqu'un utilisateur inconnu fait une demande de réinitialisation de son mot de passe 
    Alors il ne reçoit pas d'e-mail de réinitialisation de compte
    Et l'incident est enregistré dans un journal

  Scénario: Le client définit un mot de passe conforme dans les temps

    Au moment où l'utilisateur définit son mot de passe, la validité du lien est vérifiée. 
    Si le lien est valide et le mot de passe est conforme à la politique relative aux mots de passe, 
    le mot de passe est sauvegardé et le lien d'activation invalidé.

    # Ceci fait usage de la mutation setPassword qui a besoin d'un id, un token et un mot de passe. 
    # L'invalidation du token est automatique suite au changement de mot de passe.

    # It may be that saleor's existing setPassword mutation needs to be modified to take a base64 user id like this:
    # uid = urlsafe_base64_encode(force_bytes(user.pk)).decode()
    # This is indeed the userid given by the reset link
    # The setPassword mutation takes another kind of id though (cf. tests):
    # id = graphene.Node.to_global_id('User', customer_user.id)
    # this amounts to base64(':'.join([type, text_type(id)])) --> this is something different
    # The needed token seems to be one generated by the default_token_generator

    Etant donné un client qui a reçu un lien de réinitialisation de mot de passe
    Lorsqu'il définit un mot de passe conforme au plus tard 1 jour après sa réception
    Alors son nouveau mot de passe est sauvegardé
    Et son lien de réinitialisation est invalidé

  @HackerAbuse  
  Scénario: Le client définit un mot de passe non conforme dans les temps
    
    Si le client entre un mot de passe non conforme, cela signifie qu'il a contourné les vérifications 
    de l'application client. Dans ce cas, le mot de passe reste inchangé et son lien s'invalide. Il peut 
    refaire une demande de réinitialisation et recommencer le processus.
    
    # Il va falloir trouver quelles données utilisateur changer dans ce cas pour invalider le token (puisque 
    # le token ne s'invalide que si des données utilisateur ont changé ou s'il a expiré).

    Etant donné un client qui a reçu un lien de réinitialisation de mot de passe
    Lorsqu'il définit un mot de passe non conforme au plus tard 1 jour après sa réception
    Alors son mot de passe reste inchangé
    Et son lien d'activation est invalidé
    
  Scénario: Le client définit son mot de passe une deuxième fois avec le même lien
    
    Le lien de réinitialisation de mot de passe ne peut être utilisé qu'une seule fois.
    
    Etant donné un client qui a reçu un lien de réinitialisation de mot de passe
    Et qui a déjà réinitialisé son mot de passe avec ce lien
    Lorsqu'il le réinitialise pour la deuxième fois
    Alors il obtient un message d'erreur stipulant que le lien a expiré
    Et son mot de passe reste inchangé
    
  Scénario: Le client définit son mot de passe trop tard 
    
    En plus de n'être utilisable qu'une seule fois, le lien expire après un certain temps. 
    Dans ce cas, le mot de passe du client reste inchangé. Il a toujours la possibilité 
    de refaire une demande de réinitialisation pour obtenir un nouveau lien.  
    
    Etant donné un client qui a reçu un lien de réinitialisation de mot de passe
    Lorsqu'il définit un mot de passe conforme 2 jours après sa réception
    Alors il obtient un message d'erreur stipulant que le lien a expiré
    Et son mot de passe reste inchangé