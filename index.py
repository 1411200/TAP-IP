import json
import boto3
import cfnresponse

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    # TODO implement
    
    if event["RequestType"] != "Delete":
        #copy source files to destination bucket
        print(json.dumps(event))
        source_bucket = event["ResourceProperties"]["SOURCE_BUCKET_STR"]
        target_bucket = event["ResourceProperties"]["TARGET_BUCKET_STR"]
        files = event["ResourceProperties"]["FILE_MAP"]
        print(f"source: { source_bucket }")
        print(f"target: { target_bucket }")
        print(f"files: { json.dumps(files) }")
        
        for s3_file in files:
            print(f"Copying {s3_file[0]} -> {s3_file[1]}")
        
            response = s3_client.copy_object(
                Bucket=target_bucket,
                CopySource=f"{source_bucket}{s3_file[0]}",
                Key=s3_file[1])
            
            print(f"response: {response}")
        
        print("s3-mover complete.")
    else:
        #do nothing
        print("CloudFormation delete event...")
    responseData = {}
    cfnresponse.send(event, context, cfnresponse.SUCCESS, responseData, "CustomResourcePhysicalID")
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
