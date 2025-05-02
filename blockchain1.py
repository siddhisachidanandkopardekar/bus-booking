import streamlit as st
import hashlib
import time
import json
from typing import List

# --- Blockchain Classes ---
class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data  # booking info
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        content = f"{self.index}{self.timestamp}{json.dumps(self.data, sort_keys=True)}{self.previous_hash}"
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
        if self.is_seat_taken(trip_id, seat_number):
            return False, "🚫 Seat already booked!"
        new_block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            data=data,
            previous_hash=self.get_latest_block().hash
        )
        self.chain.append(new_block)
        return True, f"✅ Booking added: {data}"

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            prev = self.chain[i - 1]
            curr = self.chain[i]
            if curr.hash != curr.calculate_hash():
                return False
            if curr.previous_hash != prev.hash:
                return False
        return True

    def is_seat_taken(self, trip_id, seat_number):
        for block in self.chain[1:]:  # skip genesis block
            if isinstance(block.data, dict) and \
               block.data["trip_id"] == trip_id and \
               block.data["seat_number"] == seat_number:
                return True
        return False

    def get_chain_data(self):
        return [{
            "index": block.index,
            "timestamp": time.ctime(block.timestamp),
            "data": block.data,
            "hash": block.hash,
            "previous_hash": block.previous_hash
        } for block in self.chain]

# --- Streamlit UI ---
st.set_page_config(page_title="🧾 Blockchain Booking System", layout="wide")
st.title("🧾 Blockchain-Based Booking System")

# Persistent blockchain object
if "blockchain" not in st.session_state:
    st.session_state.blockchain = Blockchain()

tab1, tab2 = st.tabs(["➕ Add Booking", "📜 View Blockchain"])

with tab1:
    st.subheader("Add a New Booking")

    trip_id = st.text_input("Trip ID", placeholder="e.g. NYC-DC")
    seat_number = st.number_input("Seat Number", min_value=1, step=1)
    passenger_name = st.text_input("Passenger Name")

    if st.button("Add Booking"):
        if trip_id and passenger_name:
            success, msg = st.session_state.blockchain.add_booking(
                trip_id, seat_number, passenger_name
            )
            st.success(msg) if success else st.error(msg)
        else:
            st.warning("Please fill in all fields.")

with tab2:
    st.subheader("Blockchain Contents")
    for block in st.session_state.blockchain.get_chain_data():
        st.json(block)

    if st.button("🔍 Validate Chain"):
        valid = st.session_state.blockchain.is_chain_valid()
        st.success("✅ Chain is valid!") if valid else st.error("❌ Chain is invalid!")
