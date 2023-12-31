"""
File : global_data.py
Description : Initializes Global data
Created on :
Author :
E-mail :
"""
from src.constant.project_constant import Constant as constant
import threading


class GlobalData(object):
    """
    Initializes the global data required in all modules of the application
    """
    # Variable to set execution environment
 
    # Stream details containing sensor_id as key,  [stream_url, frame_size] as value

    stream_details = dict()
    db_connection = constant.EMPTY_STRING
    db_session = constant.EMPTY_STRING
    app_logger = constant.EMPTY_STRING
    pipeline_status = constant.EMPTY_STRING

    gst_main_thread = constant.EMPTY_STRING
    camera_metadata = constant.EMPTY_STRING
    inference_metadata = constant.EMPTY_STRING
    person_decteion_boxes = list()
    error_codes = dict()
    sensor_request_state = dict()
    request_state = dict()
    sensorid_event_type_queue = dict()

    decoding_status = constant.EMPTY_STRING
    decoding_event = threading.Event()

    frame_audit_interval = constant.EMPTY_STRING
    thread_lock = threading.Lock()

    frame_threshold_values = constant.EMPTY_STRING
    check_for_state_change = constant.FAILURE_STATUS
    metadata_handling = constant.EMPTY_STRING
    is_stop_done = False

  
