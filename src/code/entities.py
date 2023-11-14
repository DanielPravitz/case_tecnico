from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True, slots=True)
class Seller():
    """
    A class used to represent an Seller
    
    ...

    Attributes
    ----------
    nom_item : str
        order item name
    idt_vrne_venr: str
        seller identifier for product variant
    idt_venr: str
        seller identification number
    """
    
    idt_venr: str
    idt_vrne_venr:str
    nom_ver:str
  
@dataclass(frozen=True, slots=True)
class Item():
    """
    A class used to represent an Item 

    ...

    Attributes
    ----------
    cod_vrne_prod : str
        product variant identification
    nom_item : str
        order item name
    nom_venr : str
        seller's name
    cod_ofrt_ineo_requ : str
        order offer identification
    vlr_oril : float
        product variant original price with minimum value greater than or equal to 0
    vlr_prod : float
        product variant price with minimum value greater than or equal to 0
    vlr_prod_ofrt_desc: float
        discount on the product variant with a minimum value greater than or equal to 0 and with the default being 0
    qtd_item_pedi: int
        quantity of items in the order, with a minimum of 1 item per order
    idt_vrne_venr: str
        seller identifier for product variant
    idt_venr: str
        seller identification number
    nom_prod_orig: str
        #NOT DOCUMENTED IN DATA DICTIONARE
    vlr_desc_envo: float
        #NOT DOCUMENTED IN DATA DICTIONARE
    txt_plae_otmz_url_prod: str
        #NOT DOCUMENTED IN DATA DICTIONARE
    """
    
    cod_vrne_prod: str
    nom_item: str
    nom_venr: str
    cod_ofrt_ineo_requ: str
    vlr_oril: float
    vlr_prod: float
    vlr_prod_ofrt_desc: float
    qtd_item_pedi: int
    idt_vrne_venr: str
    idt_venr: str
    nom_prod_orig: str = field(default_factory=str)
    vlr_desc_envo: float = field(default_factory=float)
    txt_plae_otmz_url_prod: str = field(default_factory=str)
    
    def __post_init__(self) -> None:
        if self.vlr_oril < 0:
            raise ValueError("vlr_oril attribute must greater than zero.")

        if self.vlr_prod < 0:
            raise ValueError("vlr_prod attribute must greater than zero.")
        
        if self.vlr_prod_ofrt_desc < 0:
            raise ValueError("vlr_prod_ofrt_desc attribute must greater than zero.")
        
        if self.qtd_item_pedi < 1:
            raise ValueError("qtd_item_pedi attribute must be 1 or greather than 1.")

        
@dataclass(frozen=True, slots=True)
class ShippingItem():
    """
    A class used to represent an Shipping Item
    ...

    Attributes
    ----------
    cod_prod : str
        registration product code that will be received when offering multiple products
    cod_prod_venr : str
        product code registered in the seller's system
    qtd_prod:
        the quantity of the item
    stat_entg : str
        text that contains information about the item's delivery movement
        
    """
    cod_prod: str
    cod_prod_venr: str
    qtd_prod: int
    stat_entg: str 
    
    
@dataclass(frozen=True, slots=True)
class Shipping():
    
    """
    A class used to represent an Shipping
    ...

    Attributes
    ----------
    cod_tipo_entg : str
        delivery type code used to ship product
    nom_stat_entg : str
        description of the Delivery Status of the product to the customer
    cod_venr:
        seller's identification
    dat_emis_cpvt : str
        #NOT DOCUMENTED IN DATA DICTIONARE
    list_item_envo : str
       a reference to shipped items
        
    """
    cod_tipo_entg: str
    nom_stat_entg: str
    cod_venr: str
    dat_emis_cpvt: str = field(default_factory=str)
    objt_des_stat_rtmt: dict = field(default_factory=dict)
    list_item_envo: List[ShippingItem] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class Order():
    """
    A class used to represent an Order

    ...

    Attributes
    ----------
    txt_detl_idt_pedi_pgto : str
        the id of the parent order that generated the current order.
    cod_idef_clie : str
        order customer identifier
    dat_hor_tran : str
        order creation date
    stat_pgto : str
        representation of an order payment situation (status) on the Itaú marketplace
    stat_pedi : str
        representation of the name of the situation (status) of the order placed on the itaú shop marketplace
    dat_atui : str
        date of last order update
    list_item_pedi: List[Item]
        a reference to order items
    list_envo: List[Shipping]
        
    """
    
    txt_detl_idt_pedi_pgto: str
    cod_idef_clie: str
    dat_hor_tran: str
    stat_pgto: str 
    stat_pedi: str 
    dat_atui : str
    list_item_pedi: List[Item] 
    list_envo: List[Shipping] = field(default_factory=list)
    
    
    
    
   
