CREATE SCHEMA IF NOT EXISTS public;

CREATE TABLE public.instructors (
  id SERIAL PRIMARY KEY,
  name VARCHAR,
  email VARCHAR,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE public.courses (
  id SERIAL PRIMARY KEY,
  title VARCHAR,
  instructor_id INTEGER REFERENCES public.instructors(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE public.course_descriptions (
  course_id INTEGER PRIMARY KEY REFERENCES public.courses(id),
  description TEXT
);

-- 서울 캠퍼스 스키마
CREATE SCHEMA IF NOT EXISTS seoul;

CREATE TABLE seoul.students (
  id SERIAL PRIMARY KEY,
  name VARCHAR,
  email VARCHAR,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE seoul.enrollments (
  student_id INTEGER REFERENCES seoul.students(id),
  course_id INTEGER REFERENCES public.courses(id),
  enrollment_date VARCHAR,
  PRIMARY KEY (student_id, course_id)
);

CREATE TABLE seoul.reviews (
  id SERIAL PRIMARY KEY,
  student_id INTEGER REFERENCES seoul.students(id),
  course_id INTEGER REFERENCES public.courses(id),
  comment TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 제주 캠퍼스 스키마
CREATE SCHEMA IF NOT EXISTS jeju;

CREATE TABLE jeju.students (
  id SERIAL PRIMARY KEY,
  name VARCHAR,
  email VARCHAR,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE jeju.enrollments (
  student_id INTEGER REFERENCES jeju.students(id),
  course_id INTEGER REFERENCES public.courses(id),
  enrollment_date VARCHAR,
  PRIMARY KEY (student_id, course_id)
);

CREATE TABLE jeju.reviews (
  id SERIAL PRIMARY KEY,
  student_id INTEGER REFERENCES jeju.students(id),
  course_id INTEGER REFERENCES public.courses(id),
  comment TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- AI 분석 스키마
CREATE SCHEMA IF NOT EXISTS analytics;

-- pgvector 미설치 시 VECTOR(512) → FLOAT[] 또는 VARCHAR 사용
-- embedding, vector 컬럼은 임시로 VARCHAR로 설정

CREATE TABLE analytics.student_embeddings (
  campus VARCHAR,  -- 'seoul' or 'jeju'
  student_id INTEGER,
  embedding VARCHAR,  -- 원래는 VECTOR(512)
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (campus, student_id)
);

CREATE TABLE analytics.course_vectors (
  course_id INTEGER REFERENCES public.courses(id),
  vector VARCHAR,  -- 원래는 VECTOR(512)
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
