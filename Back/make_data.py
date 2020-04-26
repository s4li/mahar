from models import Course, Lesson, session

lessons = ['درس اول', 'درس دوم', 'درس سوم', 'درس چهارم', 'درس پنجم', 'درس ششم', 'درس هفتم', 'درس هشتم']
curs = Course(title='دهم')
new_course = session.add(curs)
session.flush() 
for lesson in lessons:
    lesn = Lesson(title=lesson, course_id=curs.id)
    new_lesson = session.add(lesn)
    session.commit()
