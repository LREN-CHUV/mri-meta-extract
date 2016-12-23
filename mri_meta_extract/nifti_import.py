##########################################################################
# IMPORTS
##########################################################################

import logging
import re
import glob

from . import connection
from datetime import date


##########################################################################
# GLOBAL
##########################################################################

ARGS = ['root_folder', 'csv', 'db']

conn = None


##########################################################################
# FUNCTIONS - NIFTI
##########################################################################

def nifti2db(folder, participant_id, scan_date, db_url=None):
    global conn
    conn = connection.Connection(db_url)
    for file_path in glob.iglob(folder + '/**/*.nii', recursive=True):
        logging.info("Processing '%s'" % file_path)
        try:
            session = int(re.findall(
                '/([^/]+?)/[^/]+?/[^/]+?/[^/]+?\.nii', file_path)[0])
            sequence = re.findall(
                '/([^/]+?)/[^/]+?/[^/]+?\.nii', file_path)[0]
            repetition = int(re.findall(
                '/([^/]+?)/[^/]+?\.nii', file_path)[0])

            logging.info("SEQUENCE : " + sequence)

            if participant_id and scan_date:

                filename = re.findall('/([^/]+?)\.nii', file_path)[0]

                try:
                    prefix_type = re.findall('(.*)PR', filename)[0]
                except IndexError:
                    prefix_type = "unknown"

                try:
                    postfix_type = re.findall('-\d\d_(.+)', filename)[0]
                except IndexError:
                    postfix_type = "unknown"

                save_nifti_meta(
                    participant_id,
                    scan_date,
                    session,
                    sequence,
                    repetition,
                    prefix_type,
                    postfix_type,
                    file_path
                )

        except ValueError:
            logging.warning(
                "A problem occurred with '%s' ! Check the path format... " % file_path)

    conn.close()
    logging.info('[FINISH]')


##########################################################################
# FUNCTIONS - UTILS
##########################################################################

def date_from_str(date_str):
    day = int(re.findall('(\d+)\.\d+\.\d+', date_str)[0])
    month = int(re.findall('\d+\.(\d+)\.\d+', date_str)[0])
    year = int(re.findall('\d+\.\d+\.(\d+)', date_str)[0])
    return date(year, month, day)


##########################################################################
# FUNCTIONS - DATABASE
##########################################################################

def save_nifti_meta(
        participant_id,
        scan_date,
        session,
        sequence,
        repetition,
        prefix_type,
        postfix_type,
        file_path
):
    if not conn.db_session.query(conn.Nifti).filter_by(path=file_path).first():

        scan = conn.db_session.query(conn.Scan).filter_by(date=scan_date, participant_id=participant_id)\
            .first()
        sequence_type_list = conn.db_session.query(
            conn.SequenceType).filter_by(name=sequence).all()

        if scan and len(sequence_type_list) > 0:
            scan_id = scan.id
            sess = conn.db_session.query(conn.Session).filter_by(
                scan_id=scan_id, value=session).first()

            if sess:
                session_id = sess.id
                if len(sequence_type_list) > 1:
                    logging.warning(
                        "Multiple sequence_type available for %s !" % sequence)
                sequence_type_id = sequence_type_list[0].id
                seq = conn.db_session.query(conn.Sequence).filter_by(
                    session_id=session_id,
                    sequence_type_id=sequence_type_id)\
                    .first()

                if seq:
                    sequence_id = seq.id
                    rep = conn.db_session.query(conn.Repetition).filter_by(
                        sequence_id=sequence_id,
                        value=repetition)\
                        .first()

                    if rep:
                        repetition_id = rep.id
                        nii = conn.Nifti(
                            repetition_id=repetition_id,
                            path=file_path,
                            result_type=prefix_type,
                            output_type=postfix_type
                        )
                        conn.db_session.add(nii)
                        conn.db_session.commit()