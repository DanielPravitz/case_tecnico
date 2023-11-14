import logging
import json
import os

def init_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
   
   
def is_file_exists(path:str, prefix:str, extension:str) -> bool:
    
    """
    Verify if a file exists at a specified path

    Args:
        - path: file path
        - prefix: file name
        - extensions: file extension

    Returns:
        - True if file exists,and False otherwise
        
    """
    complete_path = f'{path}/{prefix}.{extension}'
    
    return True if os.path.isfile(complete_path) else False


def read_file_s3(path:dict, prefix:str, extension:str) -> dict:
    
    """
    Reads a file at a specified path

    Args:
        - path: file path
        - prefix: file name
        - extensions: file extension

    Returns:
        - File content 
    
    """
    
    logging.info(f"Reading file: {prefix}.{extension}")
    
    complete_path = f'{path}/{prefix}.{extension}'
    
    with open(complete_path) as file_content:
            
        data = json.load(file_content)

        file_content.close()
     
    logging.info(f"Read sucessfully!")
        
    return data
 

def save_to_s3_json(data:dict, path:str, prefix:str, extension:str) -> None:
    
    """
    Saves a file at a specified path

    Args:
        - path: file path
        - prefix: file name
        - extensions: file extension

    Returns:
        - None
    
    """
    
    complete_path = f'{path}/{prefix}.{extension}'
   
    logging.info(f"Saving file: {prefix}")
    
    with open(complete_path, 'w') as file:
        file.write(json.dumps(data))
        
        file.close()
    
    logging.info(f"Saved sucessfully!")
        
    pass
