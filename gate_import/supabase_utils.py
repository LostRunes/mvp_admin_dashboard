import requests
import urllib.parse
from config import SUPABASE_URL, HEADERS

def select(table, query_params=None):
    """
    Query a Supabase table. query_params can be a string or a dict of filters.
    """
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    
    if isinstance(query_params, dict):
        # Format dict into PostgREST query parameters (e.g. key=eq.val)
        parts = []
        for k, v in query_params.items():
            if v is None:
                parts.append(f"{k}=is.null")
            else:
                # URL encode the value to handle spaces, special characters, etc.
                val_encoded = urllib.parse.quote(str(v))
                parts.append(f"{k}=eq.{val_encoded}")
        query_str = "&".join(parts)
        url = f"{url}?{query_str}"
    elif isinstance(query_params, str) and query_params:
        url = f"{url}?{query_params}"
        
    res = requests.get(url, headers=HEADERS)
    if res.status_code != 200:
        raise Exception(f"Failed select from {table}: Status {res.status_code}, Response: {res.text}")
    return res.json()

def insert(table, data):
    """
    Insert data into a Supabase table.
    """
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    res = requests.post(url, headers=HEADERS, json=data)
    if res.status_code not in (200, 201):
        raise Exception(f"Failed insert into {table}: Status {res.status_code}, Response: {res.text}")
    return res.json()

def delete(table, query_params):
    """
    Delete rows from a table.
    """
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    if isinstance(query_params, dict):
        parts = []
        for k, v in query_params.items():
            if v is None:
                parts.append(f"{k}=is.null")
            else:
                val_encoded = urllib.parse.quote(str(v))
                parts.append(f"{k}=eq.{val_encoded}")
        query_str = "&".join(parts)
        url = f"{url}?{query_str}"
    elif isinstance(query_params, str) and query_params:
        url = f"{url}?{query_params}"
        
    res = requests.delete(url, headers=HEADERS)
    if res.status_code not in (200, 204):
        raise Exception(f"Failed delete from {table}: Status {res.status_code}, Response: {res.text}")
    return True

def get_or_create(table, lookup_dict, create_dict=None):
    """
    Retrieves a record based on lookup_dict. If it doesn't exist, inserts it.
    Returns: (record_dict, was_created_bool)
    """
    existing = select(table, lookup_dict)
    if existing:
        return existing[0], False
    
    insert_data = {**lookup_dict}
    if create_dict:
        insert_data.update(create_dict)
        
    new_records = insert(table, insert_data)
    if new_records:
        return new_records[0], True
    return None, False
