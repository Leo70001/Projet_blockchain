import hashlib
import json
import time
from wallet import verify_signature

class Transaction:
    def __init__(self, sender_address, recipient_address, amount, public_key_hex, signature=None, timestamp=None):
        self.sender = sender_address
        self.recipient = recipient_address
        self.amount = amount
        self.public_key = public_key_hex
        self.timestamp = timestamp or time.time()
        self.signature = signature

    def to_dict(self):
        return self.__dict__

    def compute_hash(self):
        tx_dict = self.__dict__.copy()
        tx_dict.pop('signature', None)
        tx_string = json.dumps(tx_dict, sort_keys=True)
        return hashlib.sha256(tx_string.encode()).hexdigest()
    
    def is_valid(self):
        if self.sender == "SYSTEM":
            return True
        if not self.signature:
            return False
        return verify_signature(self.public_key, self.signature, self.compute_hash())

class Block:
    def __init__(self, index, transactions, previous_hash, nonce=0, timestamp=None):
        self.index = index
        self.timestamp = timestamp or time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_content = {
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': self.transactions,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }
        block_string = json.dumps(block_content, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    @classmethod
    def from_dict(cls, block_data):
        return cls(
            index=block_data['index'],
            transactions=block_data['transactions'],
            previous_hash=block_data['previous_hash'],
            nonce=block_data['nonce'],
            timestamp=block_data['timestamp']
        )

class Blockchain:
    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.difficulty = 4
        self.mining_reward = 50
        self.create_genesis_block()

    def create_genesis_block(self):
        fixed_timestamp = 1650000000.0  # Timestamp constant pour tous les nœuds
        genesis_block = Block(
            index=0,
            transactions=[],
            previous_hash="0",
            nonce=0,
            timestamp=fixed_timestamp
        )
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        return self.chain[-1]

    def add_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    def proof_of_work(self, block):
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * self.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        block.hash = computed_hash

    def add_block(self, block):
        last_hash = self.last_block.hash
        if block.previous_hash != last_hash:
            print(f"Erreur: Le hash du bloc précédent ne correspond pas.")
            return False

        test_block = Block(block.index, block.transactions, block.previous_hash, block.nonce, block.timestamp)
        if not (block.hash.startswith('0' * self.difficulty) and block.hash == test_block.compute_hash()):
            print(f"Erreur: La preuve de travail du bloc est invalide.")
            return False

        self.chain.append(block)
        return True

    def get_balance(self, address):
        balance = 100  # Solde initial arbitraire
        for block in self.chain:
            for tx in block.transactions:
                if tx['sender'] == address:
                    balance -= tx['amount']
                if tx['recipient'] == address:
                    balance += tx['amount']
        return balance

    def get_history(self, address):
        history = []
        for block in self.chain:
            for tx in block.transactions:
                if tx['sender'] == address or tx['recipient'] == address:
                    history.append(tx)
        return history
