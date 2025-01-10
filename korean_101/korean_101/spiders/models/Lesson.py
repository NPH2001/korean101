class Lesson:
    def __init__(self,
                 name,
                 description,
                 course_media_type,
                 media_length=None,
                 list_vocabulary=None,
                 lesson_notes=None,
                 lesson_transcript=None,
                 list_dialogue=None,
                 lesson_id=None):
        self.lesson_id = lesson_id
        self.name = name
        self.description = description
        self.course_media_type = course_media_type
        self.media_length = media_length
        self.list_dialogue =list_dialogue
        self.list_vocabulary = list_vocabulary
        self.lesson_notes = lesson_notes
        self.lesson_transcript = lesson_transcript

    def add_dialogue(self, list_dialogue_type):
        self.list_dialogue.append(list_dialogue_type)

    def to_dict(self):
        return {
            'lesson_id': self.lesson_id,
            'name': self.name,
            'description': self.description,
            'course_media_type': self.course_media_type,
            'media_length': self.media_length,
            # 'list_dialogue': [dialogue.to_dict() for dialogue in self.list_dialogue],
            'list_vocabulary': self.list_vocabulary,
            'lesson_notes': self.lesson_notes.to_dict() if self.lesson_notes else None,
            'lesson_transcript': self.lesson_transcript.to_dict() if self.lesson_transcript else None,
        }
