This script looked for a specific security group attached to all AWS instances in our enviornment to ensure it was there for security reasons.

It then created a PDF report based upon what instances did not have the security group and would upload it to a S3 bucket.

Then with SNS it could be used to send out an email to the account owners.
