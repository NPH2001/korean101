class LessonTranscript:
    def __init__(self, content, url):
        self.content = content
        self.url = url

    def to_dict(self):
        return {
            'content': self.content,
            'url': self.url
        }
