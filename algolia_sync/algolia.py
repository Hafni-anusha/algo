from algoliasearch.search_client import SearchClient 
import frappe 
import json

client = SearchClient.create('NACKX1OJD8', '9363abde47bfbf7a153516be09475db4')
index = client.init_index('dev_item')


def search_algolia(doc, event):
    
    items=frappe.get_doc('Item',doc.name)
    actors = {
        "item_name":items.item_name,
        "code":items.item_code
        }
    send = index.save_object(actors, {'autoGenerateObjectIDIfNotExist': True})

    for value in send:
        id = value["objectIDs"]
        update = frappe.db.set_value('Item',doc.name,'agolia_id',id)
    # items.save(ignore_permissions=True)
   
def delete_algolia(doc,event):
    items = frappe.get_doc('Item',doc.name)
    index.delete_object(items.agolia_id)

def update_algolia(doc,event):
    items = frappe.get_doc('Item',doc.name)
    index.partial_update_object({
        "item_name":items.item_name,
        "code" : items.item_code,
        "objectID" : items.agolia_id},
        {'createIfNotExists':False}
    )

def check_website(doc,event):
    items = frappe.get_doc('Item',doc.name)
    id=items.agolia_id
    actors={
            "item_name":items.item_name,
            "code" : items.item_code,
            "objectID" : items.agolia_id
        }
    if items.show_in_website == 1:
       
        index.save_object(actors)
    elif items.show_in_website == 0:
        index.delete_object(id)