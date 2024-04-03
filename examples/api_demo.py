import chattertools as ch
import os
from dotenv import load_dotenv
load_dotenv()

chatter = ch.Client(key = os.getenv('CHATTER_API_KEY'))
machineState = chatter.machines.get(1025).state.get()
for t in machineState:
    print(f'{t.dataType}: {t.value}')