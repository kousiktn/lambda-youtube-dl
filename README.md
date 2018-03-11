# lambda-youtube-dl
This is a thin wrapper over youtube-dl to download youtube videos using AWS Lambda and storing it in S3

# What is this project about?
I find myself downloading youtube videos in my laptop and then... not persisting them/loosing them to clear up space. So I figured I would need these features:
1. Long term storage
2. Ease of access/maintanability
3. Cheap
4. Possibly not be blocked by Youtube in the long run

(1) - Use S3
(2) (3) (4) - use AWS Lambda

And that's exactly what this project does - it creates a AWS lambda function that downloads youtube videos that you pass to it and stores it in the S3 bucket you specify.

# How to use?
```
git clone https://github.com/kousiktn/lambda-youtube-dl
cd youtubedl
zappa deploy dev # Read about how to use/configure zappa at https://github.com/Miserlou/Zappa

# Get URL from the output of the above command - it should be something like https://<id>-execute-api.us-west-2.amazonaws.com/dev
# Make sure your lambda function is able to save to the S3 bucket you configure in the environment variable for "BUCKET_NAME"

curl https://<id>-execute-api.us-west-2.amazonaws.com/dev/download?url=<youtube-url>

# Enjoy the cheap storage and pay-on-demand from S3 and Lambda
```
