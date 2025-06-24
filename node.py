# node.py
import threading
import socket
import json
from blockchain import Blockchain, Block, Transaction
from wallet import Wallet

class Node:
    def __init__(self, host, port):
        self.host = '127.0.0.1'
        self.port = port
        self.wallet = Wallet()
        self.address = self.wallet.get_address()
        print(f"Mon adresse de portefeuille: {self.address}")
        self.blockchain = Blockchain()
        self.peers = set()

    def start_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen()
        print(f"Nœud écoutant sur {self.host}:{self.port}")
        while True:
            client_socket, _ = server.accept()
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        try:
            data = client_socket.recv(4096).decode()
            if not data: return
            message = json.loads(data)
            if message['type'] == 'new_transaction':
                self.handle_new_transaction(message['data'])
            elif message['type'] == 'new_block':
                self.handle_new_block(message['data'])
        except Exception as e:
            print(f"Erreur en traitant le message: {e}")
        finally:
            client_socket.close()

    def add_peer(self, peer_host, peer_port):
        self.peers.add((peer_host, peer_port))
        print(f"Pair {peer_host}:{peer_port} ajouté.")

    def broadcast(self, message):
        for peer_host, peer_port in self.peers:
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((peer_host, peer_port))
                client.sendall(json.dumps(message).encode())
                client.close()
            except ConnectionRefusedError:
                print(f"Impossible de se connecter au pair {peer_host}:{peer_port}")

    def create_and_broadcast_transaction(self, recipient_address, amount):
        tx = Transaction(
            sender_address=self.address,
            recipient_address=recipient_address,
            amount=amount,
            public_key_hex=self.wallet.public_key.to_string().hex()
        )
        tx_hash = tx.compute_hash()
        tx.signature = self.wallet.sign_transaction(tx_hash)
        
        self.blockchain.add_transaction(tx)
        message = {"type": "new_transaction", "data": tx.to_dict()}
        self.broadcast(message)
        print("Transaction créée et diffusée.")

    def handle_new_transaction(self, tx_data):
        tx = Transaction(
            sender_address=tx_data['sender'],
            recipient_address=tx_data['recipient'],
            amount=tx_data['amount'],
            public_key_hex=tx_data['public_key'],
            signature=tx_data['signature'],
            timestamp=tx_data['timestamp']
        )
        if tx.is_valid():
            self.blockchain.add_transaction(tx)
            print("Nouvelle transaction reçue et ajoutée à la liste d'attente.")
        else:
            print(f"Transaction de {tx.sender} invalide (signature).")

    def mine_and_broadcast_block(self):
        if not self.blockchain.unconfirmed_transactions:
            print("Aucune transaction à miner.")
            return

        reward_tx = Transaction("SYSTEM", self.address, self.blockchain.mining_reward, "")
        
        transactions_to_mine = self.blockchain.unconfirmed_transactions[:]
        transactions_to_mine.insert(0, reward_tx)
        
        last_block = self.blockchain.last_block
        new_block = Block(
            index=last_block.index + 1,
            transactions=[tx.to_dict() for tx in transactions_to_mine],
            previous_hash=last_block.hash
        )
        self.blockchain.proof_of_work(new_block)
        
        self.blockchain.chain.append(new_block)
        self.blockchain.unconfirmed_transactions = []
        print(f"Nouveau bloc {new_block.index} miné et ajouté localement.")
        
        message = {"type": "new_block", "data": new_block.__dict__}
        self.broadcast(message)
        print("Nouveau bloc diffusé au réseau.")

    def handle_new_block(self, block_data):
        received_block = Block.from_dict(block_data)
        if self.blockchain.add_block(received_block):
            print(f"Nouveau bloc {received_block.index} reçu du réseau, validé et ajouté à la chaîne.")
        else:
            print(f"Bloc {received_block.index} reçu invalide, rejeté.")