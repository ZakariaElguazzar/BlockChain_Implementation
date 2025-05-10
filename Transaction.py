from ecdsa import ecdsa, SECP256k1,SigningKey,VerifyingKey
from datetime import datetime
from hashlib import sha256

private_key = SigningKey.generate(curve=SECP256k1)
public_key = private_key.get_verifying_key()

class transaction:
    def __init__(self, sender_address,receiver_address, amount):
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("The amount must be a strict positif number.")
        if not isinstance(sender_address, VerifyingKey) or not isinstance(receiver_address, VerifyingKey):
            raise ValueError("The sender and receiver addresses must be of type SigningKey (ecdsa).")
        self.sender_address = sender_address
        self.receiver_address = receiver_address
        self.amount = amount
        self.date = datetime.now()
        self.signature = self.sign(private_key).hex()

    def hash(self):
        """
        Hash the transaction data using SHA-256.
        """
        transaction_string = f"{self.sender_address.to_string().hex()}{self.receiver_address.to_string().hex()}{self.amount}{self.date}"
        return sha256(transaction_string.encode()).hexdigest()
    
    def sign(self, private_key):
        """
        Sign the transaction using the sender's private key (ECDSA).
        """
        if not isinstance(private_key,SigningKey):
            raise ValueError("The private key must be of type SigningKey (ecdsa).")
        
        # Generate the hash of the transaction
        transaction_hash = self.hash()

        # Sign the transaction hash with the private key
        return private_key.sign(transaction_hash.encode())

    def verify(self, public_key):

        if not isinstance(public_key,VerifyingKey):
            raise ValueError("The public key must be of type SigningKey (ecdsa).")
        """
        Verify the transaction's signature.
        """
        if not public_key.verify(self.signature, self.hash()):
            raise ValueError("Invalid signature.")
        print("Signature verified successfully.")

    def __str__(self):
        return f"Transaction(sender: {self.sender_address}, receiver: {self.receiver_address}, amount: {self.amount}, date: {self.date}, signature: {self.signature})"

