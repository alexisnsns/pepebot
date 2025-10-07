IMPROVE:
1/ generate with prompt instead of hardcoding the images in the bucket

CHEATSHEET:

source venv/bin/activate
python3 index.py

push code to the instance:
scp -i scriptkeys.pem index.py ec2-user@{USERNUMBER}:/home/ec2-user/

Login to the AWS console:
ssh -i scriptkeys.pem ec2-user@{USERNUMBER}

edit cronjob:
crontab -e
