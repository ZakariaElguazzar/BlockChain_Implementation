import Block
import Transaction

class Blockchain:
    difficulty = 3  # Number of zeros required at the beginning of the hash

    def __init__(self):
        self.chain = []
        self.genesis_block()

    def genesis_block(self):
        """
        Creates the genesis block (without transactions).
        """
        genesis = Block.block()
        genesis.difficulty = Blockchain.difficulty
        genesis.previous_hash = "0" * 64  # fictitious hash for the beginning
        genesis.data = []
        genesis.mine()
        self.chain.append(genesis)
        return genesis

    def add_block(self, block):
        """
        Adds a block after verification.
        """
        if not isinstance(block, Block.block):
            raise ValueError("The block must be of type Block.")

        last_block = self.get_last_block()
        if block.previous_hash != last_block.actual_hash:
            raise ValueError("The previous hash does not match.")

        if not block.verify_hash():
            raise ValueError("Invalid block hash.")

        if not block.verify_transactions():
            raise ValueError("Invalid transactions.")

        self.chain.append(block)
        return block

    def get_last_block(self):
        return self.chain[-1] if self.chain else None

    def get_chain(self):
        return self.chain

    def validate_chain(self):
        """
        Verifies the complete integrity of the blockchain.
        """
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.previous_hash != previous.actual_hash:
                raise ValueError(f"Chain broken between blocks {i-1} and {i}.")
            current.verify_hash()
            current.verify_transactions()

        print("Chain is valid.")
        return True

    def adjust_difficulty(self):
        """
        Adjusts the mining difficulty (simple example).
        """
        if len(self.chain) % 1000 == 0:  # every 1000 blocks
            Blockchain.difficulty += 1
