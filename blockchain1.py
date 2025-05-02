import hashlib
import time
from typing import List

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data  # booking info
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        content = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}"
        return hashlib.sha256(content.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain: List[Block] = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, time.time(), "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_booking(self, trip_id, seat_number, passenger_name):
        data = {
            "trip_id": trip_id,
            "seat_number": seat_number,
            "passenger": passenger_name
        }
        new_block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            data=str(data),
            previous_hash=self.get_latest_block().hash
        )
        self.chain.append(new_block)
        print(f"✅ Booking added: {data}")

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            prev = self.chain[i - 1]
            curr = self.chain[i]
            if curr.hash != curr.calculate_hash():
                return False
            if curr.previous_hash != prev.hash:
                return False
        return True

    def print_chain(self):
        for block in self.chain:
            print(f"\nBlock #{block.index}")
            print(f"Time: {time.ctime(block.timestamp)}")
            print(f"Data: {block.data}")
            print(f"Hash: {block.hash}")
            print(f"Prev: {block.previous_hash}")

# 🔧 Demo
if __name__ == "__main__":
    chain = Blockchain()
    chain.add_booking(trip_id="NYC-DC", seat_number=1, passenger_name="Alice")
    chain.add_booking(trip_id="NYC-DC", seat_number=2, passenger_name="Bob")
    chain.add_booking(trip_id="LA-SF", seat_number=1, passenger_name="Charlie")

    print("\n🔗 Full Blockchain:")
    chain.print_chain()

    print("\n⛓️ Chain Valid?", chain.is_chain_valid())
