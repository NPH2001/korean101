class Dialogue_Type:
    def __init__(self, title: str):
        self.title = title
        self.list_dialogue_data = []
    
    def add_dialogue(self, dialogue_data):
        self.list_dialogue_data.append(dialogue_data)

    def to_dict(self):
        return {
            'dialogue_type': self.title,
            'list_dialogue': [dialogue_data.to_dict() for dialogue_data in self.list_dialogue_data] 
        }