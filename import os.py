import os
import boto3, botocore
import base64

def main():
  try:
    session = boto3.session.Session()
    client = session.client(
      's3',
      endpoint_url="https://nyc3.digitaloceanspaces.com",
      region_name="us-east-1",
      aws_access_key_id='DO00BPTU48VMVQGXYQBM', 
      aws_secret_access_key='r+xPnfmtmVyA9bKVA7YAJhf7dj/we/ZQeuxQ9jOwGc4'
    )

    # with open('hola.jpeg', "wb") as file:
    #   file.write(base64.b64decode(base_64))
    
    with open('test.jpg', 'rb') as file:
      encoded_string = file.read()
    
    os.remove('test.jpg')
    response = client.put_object(
      Bucket='flippo',
      Key='flippo/complejo10.jpg', # carpeta y nombre del archivo 
      Body=encoded_string, 
      ACL='public-read',
      CacheControl='max-age=60',
      ContentType='image/jpg', 
      Metadata={
        'x-amz-meta-my-key': 'dcshoes',
      }
    )
    print(response)
  except Exception as e:
    print(str(e))
  
if __name__ == '__main__':
  print(main())
