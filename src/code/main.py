import dataclasses
import json 
import logging
import sys

from datetime import datetime
from glob import glob
from entities import Seller, Item, Shipping, ShippingItem, Order
from utils.utils import init_logging,  is_file_exists, read_file_s3, save_to_s3_json
from typing import List


def get_seller(data:dict) -> List[Seller]:
    
    """
    Get sellers data of the order 

    Args:
        - data: dict with all order data

    Returns:
        - a list of Seller Objects representing all sellers in the order
        
    """
    sellers : List[Seller] = [Seller(**seller) for seller in data['list_item_pedi']]
    
    return sellers
    
    

def get_items(data:dict) -> List[Item]:
    
    """
    Get items data of order 

    Args:
        - data: dict with all order data

    Returns:
        - a list of Item Objects representing all items in the order
        
    """
    
    items : List[Item] = [Item(**item) for item in data['list_item_pedi']]
    
    return items

def get_shipping_items(data:list) -> List[ShippingItem]:
     
    """
    Get shipping items of order 

    Args:
        - data: list with all shipping items

    Returns:
        - a list of Shipping Item Object representing all shipping items in the order
        
    """
    
    shipping_items : List[ShippingItem] = [ShippingItem(**shipping_item) for shipping_item in data ]
    
    return shipping_items
   
    
def get_shippings(data:dict) -> List[Shipping]:
    
    """
    Get shippings of order 

    Args:
        - data: dict with all shippings in the order

    Returns:
        - a list of Shipping Object representing all shipping in the order
        
    """
    
    for shipping_attr in data['list_envo']:
        shipping_attr['list_item_envo'] = get_shipping_items(shipping_attr['list_item_envo'])
        
    shippings: List[Shipping] = [Shipping(**shipping) for shipping in data['list_envo'] ]
    
    return shippings

    
def get_orders(data:dict) -> Order:
    
    """
    Get all data of the order 

    Args:
        - data: dict with all data of the order

    Returns:
        - a list of Order Object representing all data of the order
        
    """
    
    data['list_item_pedi'] = get_items(data)
    data['list_envo'] = get_shippings(data)

    order = Order(**data)
    
    return order

def verify_order_update(date_raw:str, date_trusted:str) -> bool:
    
    """
    Verify if a order status is up to date in trusted layer

    Args:
        - data_raw: last updated date of a order 
        - data_trusted: last updated date of a order in trusted layer

    Returns:
        - False if date in trusted layer is not up to date, and True otherwise
        
    """
    
    logging.info(f'Verifying updated date of order.')
        
    date_format = '%Y-%m-%dT%H:%M:%S.%fZ'
    
    dat_atui_trusted = datetime.strptime(date_trusted, date_format )
    
    dat_atui_raw = datetime.strptime(date_raw, date_format)
    
    if dat_atui_raw > dat_atui_trusted:
        logging.info(f'Order updated.Updating file!' )
        logging.info(f'Last update time:{dat_atui_raw}    Last update time in trusted:{dat_atui_trusted}')
        return True
    
    logging.info(f'The file is up to date!')
    return False

def main(raw_s3_path:str, trusted_s3_path:str, extension:str) -> None:
    """Main function."""

    init_logging()

    logging.info("Reading files...")
    for file in glob(f'{raw_s3_path}/*.json'):
        
        with open(file) as file_content:
            
            data = json.load(file_content)
            
            order = get_orders(data)
            logging.info(f"Read order: {order.txt_detl_idt_pedi_pgto}.{extension}")
            
            prefix_file = order.txt_detl_idt_pedi_pgto
        
            if is_file_exists(path=trusted_s3_path, prefix=prefix_file, extension=extension):
                logging.info(f"Order exists in trusted layer!")
                data_source = read_file_s3(path=trusted_s3_path, prefix=prefix_file, extension=extension)
               
                if verify_order_update(data['dat_atui'], data_source['dat_atui']):
                   
                    save_to_s3_json(data=dataclasses.asdict(order), path=trusted_s3_path, prefix=prefix_file, extension=extension)
            else:
                save_to_s3_json(data=dataclasses.asdict(order), path=trusted_s3_path, prefix=prefix_file, extension=extension)

if __name__ == "__main__":
    raw_path = str(sys.argv[1])
    trusted_path = str(sys.argv[2])
    
    #Optional extension argument. Default value: json
    extension = str(sys.argv[3]) if len(sys.argv) > 4 else 'json'
    
    main(raw_path, trusted_path, extension)