import subprocess
import os
import pickle
from datetime import datetime

TERMINAL_NOTIFIER_PATH = '/usr/local/bin/terminal-notifier'


class FreeSpaceNotification:
    def __init__(self, mounted_on='/'):
        self.mounted_on = mounted_on
        self.filename = '/tmp/freespace-history.pkl'
        
    
    def get_free_space(self):
        output = subprocess.check_output(['df', '-kh', self.mounted_on])
        output = output.decode().strip()

        count = 0
        free_space_info = None
        for item in output.split("\n")[-1].split():
            item = item.strip()
            if item:
                count += 1
                if count == 4:
                    return item
    
    def notify(self, title, subtitle="", message=""):
        t = '-title {!r}'.format(title)
        s = '-subtitle {!r}'.format(subtitle)
        m = '-message {!r}'.format(message)
        os.system('{} {}'.format(TERMINAL_NOTIFIER_PATH, ' '.join([m, t, s])))
    
    def get_info(self):
        if not os.path.exists(self.filename):
            return list()
        
        with open(self.filename, 'rb') as handle:
            return pickle.load(handle)
    
    def save_info(self, free_space):
        data = self.get_info()
        data.append({
            'time': datetime.now(),
            'value': free_space,
        })

        with open(self.filename, 'wb') as handle:
            pickle.dump(data, handle)
    
    def get_last_execution(self):
        data = self.get_info()
        if not data:
            return
        
        last = data[-1]
        return "Última medição foi de {} em {}".format(
            last['value'], last['time'].strftime('%H:%M'))
    
    def run(self):
        free_space = self.get_free_space()
        self.notify(
            '{} de espaço livre em disco'.format(free_space),
            self.get_last_execution()
        )

        self.save_info(free_space)

if __name__ == '__main__':
    app = FreeSpaceNotification()
    app.run()
    
