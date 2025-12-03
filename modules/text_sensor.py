import random
import time

class IncidentEar:
    def __init__(self):
        print(f"\n👂  Ayush (Text Sensor): Initializing...")
        
        # --- SIMULATION DATA ---
        # Since we don't have a live Twitter API connection yet,
        # we will use this list to simulate incoming messages.
        self.simulated_tweets = [
            "Stockholm traffic is moving smoothly.",
            "Lovely day in Norrmalm!",
            "ACCIDENT reported near Central Station! Road blocked.",
            "Traffic is normal at Drottninggatan.",
            "Major JAM reported due to construction work.",
            "Clear skies and clear roads in the city.",
            "CRITICAL: Multi-car collision near Kungsträdgården."
        ]
        
        # Placeholder for BERT Model
        # self.model = TFAutoModel.from_pretrained("bert-base-uncased")
        print("✅ NLP System Ready!")

    def get_latest_incident(self):
        """
        Picks a random tweet to simulate a live feed and classifies it.
        """
        # 1. Get a random message
        tweet = random.choice(self.simulated_tweets)
        
        # 2. Classify it (Simulating the BERT Logic)
        # In the real code, you would pass 'tweet' to the BERT model here.
        
        if "ACCIDENT" in tweet or "collision" in tweet:
            event_type = "CRITICAL ACCIDENT 🔴"
            penalty = 2000  # Massive penalty (effectively blocks road)
            
        elif "JAM" in tweet or "construction" in tweet:
            event_type = "WARNING 🟡"
            penalty = 500   # Medium penalty (slow, but passable)
            
        else:
            event_type = "Clear 🟢"
            penalty = 0     # No penalty
            
        return tweet, event_type, penalty

# --- TEST BLOCK ---
if __name__ == "__main__":
    ear = IncidentEar()
    
    print("\n📡 Starting 5-second Social Media Scan...")
    for i in range(5):
        text, status, penalty = ear.get_latest_incident()
        print(f"    Scan {i+1}: '{text[:30]}...' -> Type: {status} (Penalty: {penalty})")
        time.sleep(1)