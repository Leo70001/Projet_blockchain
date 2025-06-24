# user_terminal.py
import sys
import threading
import json
from node import Node

def print_menu():
    print("\n" + "="*30)
    print("      MENU      ")
    print("="*30)
    print("1. Envoyer une transaction")
    print("2. Miner un bloc")
    print("3. Afficher mon solde")
    print("4. Afficher mon historique de transactions")
    print("5. Afficher la chaîne complète")
    print("6. Quitter")
    print("7. Ajouter un pair")
    print("="*30)

def main():
    if len(sys.argv) != 3:
        print("Usage: python user_terminal.py <port> <peer_port1,peer_port2,...>")
        sys.exit(1)

    port = int(sys.argv[1])
    peers_str = sys.argv[2]
    
    node = Node('127.0.0.1', port)
    
    server_thread = threading.Thread(target=node.start_server)
    server_thread.daemon = True
    server_thread.start()

    if peers_str != "none":
        peer_ports = [int(p) for p in peers_str.split(',')]
        for peer_port in peer_ports:
            node.add_peer('127.0.0.1', peer_port)

    while True:
        print_menu()
        choice = input("> Votre choix: ")

        if choice == '1':
            recipient = input("Entrez l'adresse du destinataire: ")
            try:
                amount = float(input("Entrez le montant: "))
                node.create_and_broadcast_transaction(recipient, amount)
            except ValueError:
                print("Montant invalide.")
        
        elif choice == '2':
            print("Minage en cours...")
            node.mine_and_broadcast_block()

        elif choice == '3':
            balance = node.blockchain.get_balance(node.address)
            print(f"Votre solde actuel est de: {balance}")

        elif choice == '4':
            history = node.blockchain.get_history(node.address)
            if not history:
                print("Aucune transaction dans votre historique.")
            else:
                print("\n--- Votre Historique ---")
                for tx in history:
                    print(json.dumps(tx, indent=2))
                print("----------------------")

        elif choice == '5':
            print("\n--- Blockchain Complète ---")
            chain_data = []
            for block in node.blockchain.chain:
                chain_data.append(block.__dict__)
            print(json.dumps(chain_data, indent=2))
            print("-------------------------")

        elif choice == '6':
            print("Arrêt du nœud...")
            sys.exit(0)
        
        elif choice == '7':
            try:
                peer_port = int(input("Entrez le port du pair a ajouter: "))
                node.add_peer('127.0.0.1', peer_port)
            except ValueError:
                print("Port invalide.")
            
        else:
            print("Choix invalide, veuillez réessayer.")

if __name__ == '__main__':
    main()