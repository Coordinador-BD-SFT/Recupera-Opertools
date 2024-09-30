customer_structure = {
    'id': id,
    'document': int,
    'nombre': str,
    'account': list,  # Lista de el numero de cuenta asociada al customer
}

account_structure = {
    'numero': int,
    'asignment_type': date,
    'crm_origen': str,
    'marca': str,
    'ref': int,
    'active_account': bool,
    'disccount': int,
    'debt': float,
}

demographic_data_structure = {
    'numbers': list,  # Lista de numeros (str)
    'mails': list,  # lista de correos (str)
    'city': str,
    'adress': str,
}
