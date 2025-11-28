Table students {
  id integer [pk]
  name varchar
  email varchar
  created_at datetime
}

Table instructors {
  id integer [pk]
  name varchar
  email varchar
  created_at datetime
}

Table courses {
  id integer [pk]
  title varchar
  instructor_id integer [ref: > instructors.id]
  created_at datetime
}

Table course_descriptions {
  course_id integer [pk, ref: > courses.id]
  description text
}

Table enrollments {
  student_id integer [ref: > students.id]
  course_id integer [ref: > courses.id]
  enrollment_date varchar
  Note: "Composite PK (student_id, course_id) assumed"
}

Table reviews {
  id integer [pk]
  student_id integer [ref: > students.id]
  course_id integer [ref: > courses.id]
  comment text
  created_at datetime
}
