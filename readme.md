🐸 PEPE BOT

Tinkering with autonomous Twitter bots and AWS.

Python code that cycles through a set of images stored on an AWS S3 bucket and remembers which one it last posted by persisting the data — ensuring that each run picks up right where the last one left off.

Uses both Twitter API v1.1 (for media upload) and v2 (for tweeting).
Runs automatically via a cron job on an AWS EC2 instance.
