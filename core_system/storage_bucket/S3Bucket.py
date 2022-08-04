class S3Bucket:
    def __init__(self,client,getFiles) -> None:
        self.s3Client=client
        self.getFiles=getFiles
    
    def upload_file(self,path,bucket_name,upload_location):
        
        self.s3Client.upload_file(path,bucket_name,path)
        