class Course:
    def __init__(self,  name, description, total_lesson=None, course_id=None):
        self.course_id = course_id
        self.name = name
        self.description = description
        self.total_lesson = total_lesson
        self.list_lesson = []

    def add_lesson(self, lesson):
        self.list_lesson.append(lesson)
        
    def to_dict(self):
            return {
                'course_id': self.course_id,
                'name': self.name,
                'description': self.description,
                'total_lesson': self.total_lesson,
                'list_lesson': [lesson.to_dict() for lesson in self.list_lesson]  # Chuyển đổi danh sách bài học
            }