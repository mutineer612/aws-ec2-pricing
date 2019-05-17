#! /usr/local/bin/python3                                                    
                                                  
import boto3 
import re

pricing = boto3.client('pricing')

# Return all AWS Services
response = pricing.describe_services()
for service in response['Services']:
    print(service['ServiceCode'] + ": " + ", ".join(service['AttributeNames']))
print()

# ServiceCode: AmazonEC2 Attributes and Values
response = pricing.describe_services(ServiceCode='AmazonEC2')
attrs = response['Services'][0]['AttributeNames']

for attr in attrs:
    response = pricing.get_attribute_values(ServiceCode='AmazonEC2', AttributeName=attr)

    values = []
    for attr_value in response['AttributeValues']:
        values.append(attr_value['Value'])

    print("  " + attr + ": " + ", ".join(values))