class S3Bucket:
    def __init__(self,client,getFiles) -> None:
        self.s3Client=client
        self.getFiles=getFiles
    
    def upload_file(self,path,bucket_name,upload_location):
        files=self.getFiles(f"{path}")
        for file in files:
            filename=file.split("/")[-1]
            self.s3Client.upload_file(file,bucket_name,f"{upload_location}/{filename}")
        return files