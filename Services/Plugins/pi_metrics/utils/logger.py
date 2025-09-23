import logging
import os

def get_logger(name:str, file_name:str)->logging.Logger:
    """
    A helper function that create and configure a logger to write in a .log file.


    Args:
    
        - name(str): The name of the logger -> so it can be reused in different files
        - file_nama(str): Relative path of the log file

    Retruns:
        - logging.Logger: A configured logger object that writes INFO-level messages and above to the specified log file.
        
    """

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_path = os.path.join(BASE_DIR, file_name)
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        file_handler = logging.FileHandler(log_path, mode='a')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger