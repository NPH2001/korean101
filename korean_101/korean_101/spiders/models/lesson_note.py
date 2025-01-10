class LessonNote:
    def __init__(self, lesson_focus, cultural_insight, url):
        self.lesson_focus = lesson_focus
        self.cultural_insight = cultural_insight
        self.url = url

    def to_dict(self):
        return {
            'lesson_focus': self.lesson_focus,
            'cultural_insight': self.cultural_insight,
            'url': self.url
        }
