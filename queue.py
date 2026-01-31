import random

class QueueManager:
    def __init__(self):
        self.queues = {} # chat_id: [songs]
        self.loop = {} # chat_id: bool

    def add(self, chat_id, song):
        if chat_id not in self.queues:
            self.queues[chat_id] = []
        self.queues[chat_id].append(song)

    def get_next(self, chat_id):
        if chat_id in self.queues and self.queues[chat_id]:
            if self.loop.get(chat_id, False):
                # If loop is on, we'll keep the song? 
                # Usually loop means loop current song or loop queue. 
                # Let's assume loop queue for now.
                song = self.queues[chat_id].pop(0)
                self.queues[chat_id].append(song)
                return song
            return self.queues[chat_id].pop(0)
        return None

    def get_queue(self, chat_id):
        return self.queues.get(chat_id, [])

    def clear(self, chat_id):
        self.queues[chat_id] = []

    def shuffle(self, chat_id):
        if chat_id in self.queues:
            random.shuffle(self.queues[chat_id])

    def toggle_loop(self, chat_id):
        self.loop[chat_id] = not self.loop.get(chat_id, False)
        return self.loop[chat_id]

queue_manager = QueueManager()
