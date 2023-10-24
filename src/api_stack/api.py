from fastapi import APIRouter, HTTPException
from pydantic import TypeAdapter
from typing import List
from models import Item, NewItemRequest
import boto3
from boto3.dynamodb.conditions import Key
from datetime import datetime
from uuid import uuid4

class ExampleApi:
    def __init__(self, table: str) -> None:
        self.router = APIRouter()
        db = boto3.resource("dynamodb")
        self.table = db.Table(table)
        self._init_routes()

    def get_item(self, email: str, item_id: str) -> Item:
        resp = self.table.get_item(
            Key={
                'email': email,
                'id': item_id
            }
        )
        if not resp["Item"]:
            raise HTTPException(status_code=404, detail="Could not find item")
        return Item(**resp["Item"])
    
    def delete_item(self, email: str, item_id: str) -> None:
        try:
            self.table.delete_item(
                Key={
                    'email': email,
                    'id': item_id
                }
            )
        except Exception as e:
            print(e) # Replace with actual logging
            raise HTTPException(status_code=400, detail="Unable to delete item")
    
    def get_items(self, email: str) -> List[Item]:
        resp = self.table.query(
            KeyConditionExpression=Key('email').eq(email)
        )
        if not resp["Items"]:
            raise HTTPException(status_code=404, detail=f"No items returned for email {email}")
        ta = TypeAdapter(List[Item])
        items = ta.validate_python(resp["Items"])
        return items
    
    def create_item(self, body: NewItemRequest) -> Item:
        current_date = str(datetime.now())
        new_id = str(uuid4())
        new_item = {
            'id': new_id,
            'email': body.email,
            'name': body.name,
            'price': body.price,
            'ordered_date': current_date, 
            'is_shipped': False,
        }
        try:
            self.table.put_item(
                Item=new_item
            )
            return Item(**new_item)
        except Exception as e:
            print(e) # Replace with actual logging
            raise HTTPException(status_code=400, detail="Unable to create item")
        
    def _init_routes(self):
        self.router.add_api_route(
            path="/{email}/{item_id}",
            endpoint=self.get_item,
            methods=["GET"]
        )
        self.router.add_api_route(
            path="/{email}/{item_id}",
            endpoint=self.delete_item,
            methods=["DELETE"]
        )
        self.router.add_api_route(
            path="/create",
            endpoint=self.create_item,
            methods=["POST"]
        )
        self.router.add_api_route(
            path="/{email}",
            endpoint=self.get_items,
            methods=["GET"]
        )
