#! /usr/local/bin/python3

import boto3
import json
import re

location = "US West (Oregon)" 			# AWS GovCloud (US), Asia Pacific (Mumbai), Asia Pacific (Seoul), Asia Pacific (Singapore), Asia Pacific (Sydney), Asia Pacific (Tokyo), Canada (Central), EU (Frankfurt), EU (Ireland), EU (London), EU (Paris), South America (Sao Paulo), US East (N. Virginia), US East (Ohio), US West (N. California), US West (Oregon)
tenancy = "Shared" 						# Shared, Dedicated
instanceType = "m5.xlarge"     			# General Purpose Instance Family/Models
operatingSystem = "RHEL"				# Generic, Linux, NA, RHEL, SUSE, Windows
preInstalledSw = "NA"					# NA, SQL Ent, SQL Std, SQL Web
licenseModel = "No License required"	# Bring your own license, NA, No License required
volumeType = "General Purpose" 			# Cold HDD, General Purpose, Magnetic, Provisioned IOPS, Throughput Optimized HDD

pricing = boto3.client('pricing')

# EC2 Instance Attribute Match
instanceData = pricing.get_products(
     ServiceCode='AmazonEC2',
     Filters = [
         {'Type' :'TERM_MATCH', 'Field':'location',        'Value':location		   },
         {'Type' :'TERM_MATCH', 'Field':'tenancy',         'Value':tenancy         },
         {'Type' :'TERM_MATCH', 'Field':'instanceType',    'Value':instanceType    },
         {'Type' :'TERM_MATCH', 'Field':'operatingSystem', 'Value':operatingSystem },
         {'Type' :'TERM_MATCH', 'Field':'preInstalledSw',  'Value':preInstalledSw  },
         {'Type' :'TERM_MATCH', 'Field':'licenseModel',    'Value':licenseModel    },

     ],
     #MaxResults=100
)

# Return output from pricing API
#instanceString = str(instanceData)
#print (instanceString)

# When the Capacity Reservation is active, you are charged the equivalent On-Demand rate whether you run the instances or not.
# If you do not use the reservation, this shows up as unused reservation on your EC2 bill.
# When you run an instance that matches the attributes of a reservation, you just pay for the instance and nothing for the reservation.

#AllocatedCapacityReservation
#UnusedCapacityReservation
#Used = OnDemand Pricing

for instanceVal in instanceData["PriceList"]:
    instanceValJson=json.loads(instanceVal)
    if("OnDemand" in instanceValJson["terms"] and len(instanceValJson["terms"]["OnDemand"]) > 0):
        for onDemandValues in instanceValJson["terms"]["OnDemand"].keys():
            for priceDimensionValues in instanceValJson["terms"]["OnDemand"][onDemandValues]["priceDimensions"]:

                 if("Used" in instanceValJson["product"]["attributes"]["capacitystatus"]):
                     instancePrice = (instanceValJson["terms"]["OnDemand"][onDemandValues]["priceDimensions"][priceDimensionValues]["pricePerUnit"])

instanceString = str(instancePrice)
#print (instanceString)

instanceUnitPrice = re.search( r'(\d{1,10}\.\d{1,10})', instanceString, re.S)
#print (instanceUnitPrice)

instanceUnitPrice = instanceUnitPrice.group(1)
print ("Instance Unit Price:   " + (instanceUnitPrice))

instanceHourlyPrice = float(instanceUnitPrice)
print ("Instance Hourly Price: " + str(instanceHourlyPrice))

instanceDailyPrice = (float(instanceUnitPrice) * 24)
print ("Instance Daily Price:  " + str(instanceDailyPrice))

# EBS Storage Attribute Match
storageData = pricing.get_products(
     ServiceCode='AmazonEC2',
     Filters = [
         {'Type' :'TERM_MATCH', 'Field':'location',        'Value':location		   },
         {'Type' :'TERM_MATCH', 'Field':'volumeType',      'Value':volumeType 	   },
     ],
     #MaxResults=100
)

# Return output from pricing API
storageString = str(storageData)
#print (storageString)

for storageVal in storageData["PriceList"]:
    storageValJson=json.loads(storageVal)
    if("OnDemand" in storageValJson["terms"] and len(storageValJson["terms"]["OnDemand"]) > 0):
        for onDemandValues in storageValJson["terms"]["OnDemand"].keys():
            for priceDimensionValues in storageValJson["terms"]["OnDemand"][onDemandValues]["priceDimensions"]:
                storagePrice = (storageValJson["terms"]["OnDemand"][onDemandValues]["priceDimensions"][priceDimensionValues]["pricePerUnit"])

storageString = str(storagePrice)
#print (storageString)

storageUnitPrice = re.search( r'(\d{1,10}\.\d{1,10})', storageString, re.S)
#print (storageUnitPrice)

storageUnitPrice = storageUnitPrice.group(1)
print ("Storage Unit Price:    " + (storageUnitPrice))

# Multiply storageHourlyPrice by GB
storageHourlyPrice = ((float(storageUnitPrice) * 3600) / (86400 * 30))
storageHourlyPrice = round(storageHourlyPrice,10)
print ("Storage Hourly Price:  " + str(storageHourlyPrice))

# Multiply storageDailyPrice by GB
storageDailyPrice = ((float(storageUnitPrice) * 86400) / (86400 * 30))
storageDailyPrice = round(storageDailyPrice,10)
print ("Storage Daily Price:   " + str(storageDailyPrice))
