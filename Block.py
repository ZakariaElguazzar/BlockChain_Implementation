import hashlib
from datetime import datetime
import Transaction
from ecdsa import SECP256k1,SigningKey

class Block:
    index_counter = 0
    difficulty = 4  # You can adjust the difficulty here

    def __init__(self):
        Block.index_counter += 1
        self.index = Block.index_counter
        self.previous_hash = None
        self.actual_hash = None
        self.date = datetime.now()
        self.data = []  # Initialize as a list to hold transactions
        self.nonce = 0

    def hash(self):
        """
        Hash the block data using SHA-256.
        """
        block_string = f"{self.index}{self.previous_hash}{self.date}{self.data}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine(self):
        """
        Mine the block by finding a nonce that produces a hash with the specified difficulty.
        """
        self.nonce = 0
        self.date = datetime.now()

        while True:
            hashed = self.hash()
            if hashed.startswith('0' * Block.difficulty):
                self.actual_hash = hashed
                break
            self.nonce += 1

    def verify_hash(self):
        """
        Verify the block's hash.
        """
        if self.hash() != self.actual_hash:
            raise ValueError("Invalid hash.")
        self.verify_difficulty()
        print("Hash verified successfully.")
        return True

    def verify_difficulty(self):
        """
        Verify that the block hash meets the difficulty requirement.
        """
        if not self.hash().startswith('0' * Block.difficulty):
            raise ValueError("Hash does not meet difficulty requirement.")
        return True

    def verify_transactions(self):
        """
        Verify the transactions in the block.
        """
        if not self.data:
            raise ValueError("No transactions to verify.")
        for transaction in self.data:
            if not isinstance(transaction, Transaction.Transaction):
                raise ValueError("Invalid transaction type.")
            if not transaction.verify(transaction.sender_address):
                raise ValueError("Invalid transaction signature.")
        return True

    def verify_block(self):
        """
        Verify the entire block.
        """
        self.verify_hash()
        self.verify_difficulty()
        self.verify_transactions()
        return True

block1 = Block()
block1.difficulty = 4
sender_address = SigningKey.generate(curve=SECP256k1).get_verifying_key()
receiver_address = SigningKey.generate(curve=SECP256k1).get_verifying_key()
print("Sender address:", type(sender_address))
block1.data = [Transaction.transaction(sender_address, receiver_address, 10)]
block1.mine()
print("Block mined successfully.")
print("Block actual hash:", block1.actual_hash)
print("Block nonce:", block1.nonce)
print("Block index:", block1.index)
print("Block previous hash:", block1.previous_hash)
print("Block date:", block1.date)
print("Block data:", block1.data[0].__str__())
print("Block difficulty:", block1.difficulty)
