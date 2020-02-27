import configparser
from os import path


class Constants(object):
    config_file_path = None
    config = configparser.ConfigParser()
    if config_file_path:
        config.read(config_file_path)
    elif path.exists("VAS-config.ini"):
        print("path exists")
        config.read("VAS-config.ini")
    else:
        print("reading from ../")
        config.read("../VAS-config.ini")

         
    if config:
        cam_101 =config["CAM_URL"]["cam_101"]
        cam_102 =config["CAM_URL"]["cam_102"]
        cam_103 =config["CAM_URL"]["cam_103"]
        cam_105 =config["CAM_URL"]["cam_105"]
        cam_107 =config["CAM_URL"]["cam_107"]
        
        occupancy_threshold =config["PARAMETERS"]["occupancy_threshold"]
        crowd_threshold =config["PARAMETERS"]["crowd_threshold"]
        duration =config["PARAMETERS"]["duration"]

        project_folder_path = config["DEFAULT"]["project_folder_path_from_home"]
        crowd_detection =config["DEFAULT"]["crowd_detection"]
        occupancy_detection =config["DEFAULT"]["occupancy_detection"]
        line_crossing_detection =config["DEFAULT"]["line_crossing_detection"]
        person_in_suspicious_area =config["DEFAULT"]["person_in_suspicious_area"]
        crowd_detection_button =config["VAS_GUI"]["crowd_detection_button"]
        crowd_detection_label =config["VAS_GUI"]["crowd_detection_label"]
        occupancy_detection_button =config["VAS_GUI"]["occupancy_detection_button"]
        occupancy_detection_label =config["VAS_GUI"]["occupancy_detection_label"]
        line_crossing_detection_button =config["VAS_GUI"]["line_crossing_detection_button"]
        line_crossing_detection_label =config["VAS_GUI"]["line_crossing_detection_label"]
        person_in_suspicious_area_button =config["VAS_GUI"]["person_in_suspicious_area_button"]
        person_in_suspicious_area_label =config["VAS_GUI"]["person_in_suspicious_area_label"]
        model =config["DNN"]["model"]
        graph =config["DNN"]["graph"]
