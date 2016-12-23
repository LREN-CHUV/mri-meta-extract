# coding: utf-8
from sqlalchemy import Column, Date, Enum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Check(Base):
    __tablename__ = 'check'

    id = Column(Integer, primary_key=True, nullable=False)
    quality_check_id = Column(ForeignKey('quality_check.id'), nullable=False, index=True)
    nifti_id = Column(ForeignKey('nifti.id'), nullable=False, index=True)
    value = Column(Float, nullable=False)

    nifti = relationship('Nifti')
    quality_check = relationship('QualityCheck')


class Dicom(Base):
    __tablename__ = 'dicom'

    id = Column(Integer, primary_key=True, nullable=False)
    repetition_id = Column(ForeignKey('repetition.id'), nullable=False, index=True)
    path = Column(Text, nullable=False)

    repetition = relationship('Repetition')


class Nifti(Base):
    __tablename__ = 'nifti'

    id = Column(Integer, primary_key=True, nullable=False)
    repetition_id = Column(ForeignKey('repetition.id'), nullable=False, index=True)
    path = Column(Text, nullable=False)
    result_type = Column(String(255), nullable=False)
    output_type = Column(String(255), nullable=False)

    repetition = relationship('Repetition')


class Participant(Base):
    __tablename__ = 'participant'

    id = Column(String(255), primary_key=True)
    gender = Column(Enum('male', 'female', 'other', 'unknown', name='gender'), nullable=False)
    handedness = Column(Enum('left', 'right', 'ambidexter', 'unknown', name='handedness'), nullable=False)
    birthdate = Column(Date, nullable=True)


class Project(Base):
    __tablename__ = 'project'

    id = Column(Integer, primary_key=True)
    researcher_id = Column(ForeignKey('researcher.id'), nullable=False, index=True)
    scan_id = Column(ForeignKey('scan.id'), nullable=False, index=True)
    name = Column(String(255), nullable=False, unique=True)

    researcher = relationship('Researcher')
    scan = relationship('Scan')


class QualityCheck(Base):
    __tablename__ = 'quality_check'

    id = Column(Integer, primary_key=True, nullable=False)
    scientist_id = Column(ForeignKey('researcher.id'), nullable=False, index=True)

    scientist = relationship('Researcher')


class Repetition(Base):
    __tablename__ = 'repetition'

    id = Column(Integer, primary_key=True, nullable=False)
    sequence_id = Column(ForeignKey('sequence.id'), nullable=False, index=True)
    value = Column(Integer, nullable=False)

    sequence = relationship('Sequence')


class Researcher(Base):
    __tablename__ = 'researcher'

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String(255), nullable=False)
    firstname = Column(String(255), nullable=False)
    lastname = Column(String(255), nullable=False)


class Responsible(Base):
    __tablename__ = 'responsible'

    scientist_id = Column(ForeignKey('researcher.id'), primary_key=True, nullable=False, index=True)
    scan_id = Column(ForeignKey('scan.id'), primary_key=True, nullable=False, index=True)
    role = Column(Enum('technician', 'supervisor', name='responsible_role'), nullable=False)

    scan = relationship('Scan')
    scientist = relationship('Researcher')


class Scan(Base):
    __tablename__ = 'scan'

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    role = Column(Enum('C', 'P', 'IC', 'U', name='scan_role'), nullable=False)
    comment = Column(Text, nullable=False)
    participant_id = Column(ForeignKey('participant.id'), nullable=False, index=True)

    participant = relationship('Participant')


class Sequence(Base):
    __tablename__ = 'sequence'

    id = Column(Integer, primary_key=True, nullable=False)
    session_id = Column(ForeignKey('session.id'), nullable=False, index=True)
    sequence_type_id = Column(ForeignKey('sequence_type.id'), nullable=False, index=True)

    sequence_type = relationship('SequenceType')
    session = relationship('Session')


class SequenceType(Base):
    __tablename__ = 'sequence_type'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    manufacturer = Column(String(255), nullable=False)
    manufacturer_model_name = Column(String(255), nullable=False)
    institution_name = Column(String(255), nullable=False)
    slice_thickness = Column(Float, nullable=True)
    repetition_time = Column(Float, nullable=True)
    echo_time = Column(Float, nullable=True)
    echo_number = Column(Integer, nullable=True)
    number_of_phase_encoding_steps = Column(Integer, nullable=True)
    percent_phase_field_of_view = Column(Float, nullable=True)
    pixel_bandwidth = Column(Integer, nullable=True)
    flip_angle = Column(Float, nullable=True)
    rows = Column(Integer, nullable=True)
    columns = Column(Integer, nullable=True)
    magnetic_field_strength = Column(Float, nullable=True)
    space_between_slices = Column(Float, nullable=True)
    echo_train_length = Column(Integer, nullable=True)
    percent_sampling = Column(Float, nullable=True)
    pixel_spacing_0 = Column(Float, nullable=True)
    pixel_spacing_1 = Column(Float, nullable=True)


class Session(Base):
    __tablename__ = 'session'

    id = Column(Integer, primary_key=True, nullable=False)
    scan_id = Column(ForeignKey('scan.id'), nullable=False, index=True)
    value = Column(Integer, nullable=False)

    scan = relationship('Scan')