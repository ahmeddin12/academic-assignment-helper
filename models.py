# backend/models.py
from sqlalchemy import Column, Integer, String, Float, Text, JSON, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from .db import Base

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100))
    email = Column(String(100), unique=True, index=True)
    password_hash = Column(String)
    student_id = Column(String(50))
    created_at = Column(TIMESTAMP, server_default=func.now())
    assignments = relationship("Assignment", back_populates="student")

class Assignment(Base):
    __tablename__ = "assignments"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    filename = Column(String)
    filepath = Column(String)
    original_text = Column(Text)
    topic = Column(String)
    academic_level = Column(String)
    word_count = Column(Integer)
    uploaded_at = Column(TIMESTAMP, server_default=func.now())
    student = relationship("Student", back_populates="assignments")
    result = relationship("AnalysisResult", uselist=False, back_populates="assignment")

class AnalysisResult(Base):
    __tablename__ = "analysis_results"
    id = Column(Integer, primary_key=True, index=True)
    assignment_id = Column(Integer, ForeignKey("assignments.id"))
    suggested_sources = Column(JSON)
    plagiarism_score = Column(Float)
    flagged_sections = Column(JSON)
    research_suggestions = Column(Text)
    citation_recommendations = Column(Text)
    confidence_score = Column(Float)
    analyzed_at = Column(TIMESTAMP, server_default=func.now())
    assignment = relationship("Assignment", back_populates="result")

class AcademicSource(Base):
    __tablename__ = "academic_sources"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    authors = Column(String)
    publication_year = Column(Integer)
    abstract = Column(Text)
    full_text = Column(Text)
    source_type = Column(String)
    embedding = Column(Vector(1536))
