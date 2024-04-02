import chattertools as ch
import os
import time
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

class MachineWatcher:
    def __init__(self, machineId):
        self.machineId = machineId
        self.chatter = ch.Client(key = os.getenv('CHATTER_API_KEY'))

        self.state = {
            ch.DataType.ONLINE: None,
            ch.DataType.MODE: None,
            ch.DataType.PROGRAM: None,
            ch.DataType.SPINDLE_SPEED: None,
            ch.DataType.PART_COUNT: None,
            ch.DataType.PART_GOAL: None,
        }

    def run(self):
        while True:
            externalState = self.chatter.machines.get(1025).state.get()
            for transaction in externalState:
                if transaction.dataType in self.state:
                    self.state[transaction.dataType] = transaction.value

            print(f'Machine {self.machineId} state - {datetime.now()}')
            for key, value in self.state.items():
                print(f'{key}: {value}')

            time.sleep(1)

if __name__ == "__main__":
    watcher = MachineWatcher(1025)
    try:
        watcher.run()
    except KeyboardInterrupt:
        print('Exiting...')
        exit()