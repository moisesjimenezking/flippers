import os
import boto3, botocore
import base64


def boto(bot_name, product_name, base_64, content_type):
  try:
    session = boto3.session.Session()
    client = session.client(
        's3',
        endpoint_url="https://nyc3.digitaloceanspaces.com",
        region_name="us-east-1",
        aws_access_key_id='DO00BPTU48VMVQGXYQBM', 
        aws_secret_access_key='r+xPnfmtmVyA9bKVA7YAJhf7dj/we/ZQeuxQ9jOwGc4'
    )

    with open(product_name, "wb") as file:
      file.write(base64.b64decode(base_64))
    
    with open(product_name, 'rb') as file:
      encoded_string = file.read()

    response = client.put_object(
        Bucket='flippo',
        Key='{}/{}'.format(bot_name, product_name), # carpeta y nombre del archivo 
        Body= encoded_string,
        ACL='public-read',
        ContentType = content_type,
        CacheControl = 'max-age=60',
        
        Metadata={
            'x-amz-meta-my-key': str(bot_name),
        }
    )
    
    os.remove(product_name)
    url = "https://{}.nyc3.{}.digitaloceanspaces.com/{}/{}".format("flippo", "cdn",bot_name, product_name)
    response = {
        "response":{
            "url": url
        },
        "status_http":200
    }
  except Exception as e:
    response = {
        'response':{
            'message'  : e.args[0] if len(e.args) > 0 else str(e)
        },
        
        'status_http':e.args[1] if len(e.args) > 1 else 404
    }
    
  return response