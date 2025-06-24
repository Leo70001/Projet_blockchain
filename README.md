Blockchain de Transactions entre Amis
Description

Ce projet est une simulation simplifiée d'une blockchain en Python, conçue à des fins éducatives. Il met en œuvre les concepts fondamentaux de la technologie blockchain, inspirés du TP3 de SR73. L'application permet à trois utilisateurs, chacun opérant depuis son propre terminal, de participer à un réseau peer-to-peer, d'échanger des transactions, de miner de nouveaux blocs et de consulter leurs comptes.

La structure des blocs s'inspire de celle décrite dans le TP, incluant une empreinte du bloc précédent, les données de transaction, une signature et une preuve de travail. 

Fonctionnalités

    Portefeuilles Individuels : Chaque nœud génère une paire de clés cryptographiques (privée et publique) en utilisant l'algorithme ECDSA pour garantir la propriété des fonds. 

Transactions Signées : Chaque transaction est signée numériquement par l'expéditeur pour en prouver l'authenticité. Les autres nœuds du réseau vérifient cette signature.
Réseau Peer-to-Peer : Le système simule un réseau décentralisé où les nœuds communiquent entre eux pour diffuser les transactions et les nouveaux blocs.
Minage par Preuve de Travail (Proof-of-Work) : Pour ajouter un nouveau bloc à la chaîne, un "mineur" doit résoudre une énigme cryptographique, ce qui sécurise le réseau contre les modifications frauduleuses. Ce processus consiste à trouver une valeur qui, une fois hachée avec le reste du bloc, produit une empreinte numérique avec un certain nombre de zéros.
Récompense de Minage : Le mineur qui réussit à valider un bloc est récompensé pour son travail.
Consultation des Comptes : Chaque utilisateur peut à tout moment afficher son solde ainsi que l'historique complet de ses transactions.

Structure des Fichiers

    wallet.py : Gère la création des portefeuilles, la génération des clés ECDSA et les fonctions de signature/vérification.
    blockchain.py : Définit les classes principales : Transaction, Block, et Blockchain. Il contient la logique fondamentale de la chaîne, de la preuve de travail et de la validation.
    node.py : Implémente le nœud du réseau. Ce fichier gère le serveur d'écoute, la communication avec les autres pairs, et la logique de diffusion et de réception des informations.
    user_terminal.py : Fournit l'interface en ligne de commande (CLI) permettant à l'utilisateur d'interagir avec son nœud (envoyer de l'argent, miner, etc.).

Prérequis

    Python 3.x
    La bibliothèque ecdsa

Installation

Pour installer la dépendance nécessaire, ouvrez un terminal et exécutez la commande suivante :
Bash

pip install ecdsa

ou si vous avez plusieurs versions de Python :
Bash

python -m pip install ecdsa

Comment Lancer l'Application

Pour simuler le réseau, vous devez ouvrir trois terminaux distincts. Suivez cet ordre de lancement :

    Terminal 1 (Alice) :
    Bash

python user_terminal.py 5000 none

Terminal 2 (Bob) :
Bash

python user_terminal.py 5001 5000

Terminal 3 (Charlie) :
Bash

    python user_terminal.py 5002 5000,5001

Étape Cruciale : Connexion Bidirectionnelle

Le peering au démarrage est à sens unique. Vous devez le rendre bidirectionnel manuellement :

    Dans le terminal d'Alice (port 5000) :
        Choisissez l'option 7 (Ajouter un pair).
        Entrez le port de Bob : 5001.
        Choisissez à nouveau l'option 7.
        Entrez le port de Charlie : 5002.

Le réseau est maintenant prêt.
Scénario d'Utilisation

    Copiez les adresses : Notez l'adresse de portefeuille de chaque utilisateur, affichée au démarrage de chaque terminal.
    Alice envoie de l'argent : Dans le terminal d'Alice, choisissez l'option 1, entrez l'adresse de Bob et un montant. Vous devriez voir un message de réception sur les terminaux de Bob et Charlie.
    Charlie mine le bloc : Dans le terminal de Charlie, choisissez l'option 2. Il va traiter la transaction en attente, créer un nouveau bloc et le diffuser. Vous devriez voir les messages de réception du bloc sur les terminaux d'Alice et Bob.
    Vérifiez les soldes : Dans chaque terminal, utilisez l'option 3 pour voir les soldes mis à jour. Le solde d'Alice aura diminué, celui de Bob aura augmenté, et celui de Charlie aura augmenté grâce à la récompense de minage. 
