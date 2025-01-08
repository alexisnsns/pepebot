source venv/bin/activate
python3 index.py

1/ add 50 pepe

push code to the instance:
scp -i scriptkeys.pem index.py ec2-user@3.143.214.183:/home/ec2-user/

Login to the AWS console:
ssh -i scriptkeys.pem ec2-user@3.143.214.183

edit cronjob:
crontab -e
