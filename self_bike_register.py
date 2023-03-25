import os
import boto3
import uuid
from dotenv import load_dotenv
from dotenv import dotenv_values

def displayAllValues():
    env_vars = dotenv_values()
    for var in env_vars:
        print(var)

def deleteVar(name):
    os.environ.pop(name,None)
    #os.unsetenv(name)
def setVar(name,value):
        
   
    # Open the .env file for appending
    with open(".env", "a") as f:
        # Write the new variable to the file
        f.write(f"\n{name}={value}")

    # Add the new variable to the environment
    os.environ[name] = value

    testVar = os.getenv(name)

    print("New variable added",testVar)




client = boto3.client(
    'dynamodb',
    aws_access_key_id='AKIAT3I7RJXEK5G4P2HN',
    aws_secret_access_key='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',
    region_name='us-east-1',
    )
dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id='AKIAT3I7RJXEK5G4P2HN',
    aws_secret_access_key='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',
    region_name='us-east-1',
    )

# Instantiate a table resource object without actually
# creating a DynamoDB table. Note that the attributes of this table
# are lazy-loaded: a request is not made nor are the attribute
# values populated until the attributes
# on the table resource are accessed or its load() method is called.
table = dynamodb.Table('Bikes')

# Print out some data about the table.
# This will cause a request to be made to DynamoDB and its attribute
# values will be set based on the response.
print(table.item_count)
id = str(uuid.uuid4())

table.put_item(
    Item = {
        'id':id,
        'biker':'user123'
        }
    )

response = table.get_item(
    Key = { 'id': id
        
        }
    )

print("Bike with following details created sucessfully",response['Item']) 