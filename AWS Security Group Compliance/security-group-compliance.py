import boto3
from fpdf import FPDF, HTMLMixin
import json
import botocore
from datetime import datetime
import os
import sys

misconfigured_group= [] #instances with misconfigured security group
no_security_group = {} #instances without security group attached
lst_of_i = [] #list of instances
id_list = [] #list of instance id
sec_id = [] #instance id of group attached
triggername = ''
grpexist = False
invalidrule = []
accountid = ''
extension = ':role/config-role'
#arn_main = ''
#arn_satellite = '' 
arn = 'arn:aws:iam::'


no_secgrp_id_list = {}
no_secgrp_id_list2 = []
table = []
table2 = [] #group id, group name, vpc

regions = ['us-east-1','us-east-2','us-west-1','us-west-2','eu-central-1','eu-west-1','eu-west-2', 'eu-west-3', 'eu-north-1']
client = boto3.client('ec2')
ec2 = boto3.resource('ec2')
#alias = boto3.client('iam').list_account_aliases()['AccountAliases'][0]
alias = ''
class HTML2PDF(FPDF, HTMLMixin):
    def footer(self):
        
                self.set_text_color(0,0,0)
                self.set_y(-15)
                self.set_font('Arial', 'I', 8)
                txt = 'Page %s of %s' % (self.page_no(), self.alias_nb_pages())
                self.cell(0, 10, txt, 0, 0, 'C')
                
        ###################   
        #Report Generation#
        ###################
                
def html2pdf():
    pdf = HTML2PDF()
    pdf.set_fill_color(0, 0, 0)
    pdf.add_page()
    pdf.set_font("Arial",'B', size=20)
    epw = pdf.w - 2*pdf.l_margin
    th = pdf.font_size
    col_width = epw/3
    
    pdf.ln(100)
    pdf.set_text_color(28,92,124)
    pdf.cell(epw, 0.0, 'xxx Security Group Compliance', align='C')
    pdf.ln(2*th)
    pdf.cell(epw, 0.0, '{}'.format(alias), align='C')

    pdf.add_page()

    pdf.ln(.5*th)
    pdf.set_text_color(28,92,124)
    pdf.cell(epw, 0.0, 'Instances without Security Group', align='C')
    pdf.ln(th)
    pdf.set_font("Arial", size=10)
   
   
   
    pdf.set_text_color(0,0,0)
    for row in table:
        for datum in row:
            pdf.cell(col_width, 2*th, str(datum), border=1, align='C')
        pdf.ln(2*th)

    pdf.add_page()

    pdf.set_font("Arial",'B', size=20)
    pdf.ln(.5*th)
    pdf.set_text_color(28,92,124)
    pdf.cell(epw, 0.0, 'Instances with Security Group Misconfigured', align='C')
    pdf.ln(th)
    pdf.set_font("Arial", size=10)
    pdf.set_text_color(0,0,0)
    
    for row in table2:
        for datum in row:
            pdf.cell(col_width, 2*th, str(datum), border=1, align='C')
        pdf.ln(2*th)
        
    global grpexist
    if (len(table2) == 0 and grpexist == False):
        pdf.write(10,'No security group with proper name exists within account')
   
   ####################################File Output/Upload ################################################ 
    x =datetime.now()
    date = x.strftime('%m-%d-%Y_%H-%M')
    filename = '{}_report_{}.pdf'.format(alias,date)
    pdf.output(r'/tmp/{}'.format(filename))
    s3 = boto3.resource('s3')
    s3.meta.client.upload_file(r'/tmp/{}'.format(filename),'xxx-security-services','{}/{}'.format(alias,filename),ExtraArgs={'ACL':'bucket-owner-full-control'})
    os.remove(r'/tmp/{}'.format(filename))


def get_instance_name(instance_id):
    
    ec2instance = ec2.Instance(instance_id)
    instancename = ''
    for tags in ec2instance.tags:
        if instance.tags:
            if tags["Key"] == 'Name':
                instancename = tags["Value"]
                return instancename
    
  
def email():
    sns = boto3.client('sns')
    response = sns.publish(
    TargetArn='arn:aws:sns:us-east-1:313143944495:Security_Group_Compliance',
    Subject='AWS Security Compliance Report',
    Message='A new report has been generated regarding security group compliance. The report is available here: {}.'.format('https://s3.console.aws.amazon.com/s3/buckets/x/?region=us-east-1&tab=overview'),    
)


def run(event, lambda_context):
    global accountid
    compliant = False
    invoking_event = json.loads(event['invokingEvent'])
    
    

    sec_groups = [] 
    
    i  = 0 #counter 1
    i2 = 0 #counter 2
    i3 = 0 #counter 3

    rule_settings = [{'IpProtocol': '-1', 'IpRanges': [{'CidrIp': 'x/32'}], 'Ipv6Ranges': [], 'PrefixListIds': [], 'UserIdGroupPairs': []}]
    
    sts_client = boto3.client('sts')
    #print(event['accountId'])
    #accountid = json.loads(event['accountId'])
    accountid = event['accountId']
    arn_satellite = str(arn) + str(accountid) + str(extension)
   
    assumed_role_object=sts_client.assume_role(RoleArn=arn_satellite,RoleSessionName="AssumeRoleSatellite") 
    credentials=assumed_role_object['Credentials']
    
    #alias = boto3.client('iam').list_account_aliases()['AccountAliases'][0]

    
    while (i < len(regions)):
        try:
            global ec2,client,alias
            ec2 = boto3.resource('ec2', region_name = regions[i],aws_access_key_id=credentials['AccessKeyId'], aws_secret_access_key=credentials['SecretAccessKey'], aws_session_token=credentials['SessionToken'],)
            client = boto3.client('ec2', region_name = regions[i],aws_access_key_id=credentials['AccessKeyId'], aws_secret_access_key=credentials['SecretAccessKey'], aws_session_token=credentials['SessionToken'],)
            iam = boto3.client('iam', region_name = regions[i],aws_access_key_id=credentials['AccessKeyId'], aws_secret_access_key=credentials['SecretAccessKey'], aws_session_token=credentials['SessionToken'],)
            alias = iam.list_account_aliases()['AccountAliases'][0]
            
            
        except botocore.exceptions.ClientError as e:
            i = i + 1
            continue
        
       # print(regions[i])

        
        
        
        ##############################################    
        #Checking for misconfigured security settings#
        ##############################################
    
        callsecgroups = client.describe_security_groups()
        for group in callsecgroups['SecurityGroups']:
            while (i2 < len(callsecgroups['SecurityGroups'])):
                if (callsecgroups['SecurityGroups'][i2]['GroupName'] == 'sgp-security-services'): 
                    test = callsecgroups['SecurityGroups'][i2]['IpPermissions']
                    #print(test) do a try except below
                    if (rule_settings == test or ((rule_settings[0]['IpRanges'][0]['CidrIp'] == test[0]['IpRanges'][0]['CidrIp']) and (rule_settings[0]['IpProtocol'] == test[0]['IpProtocol']))):
                        global grpexist
                        grpexist = True
                        
                    else: 
                        groupid = callsecgroups['SecurityGroups'][i2]['GroupId'] #get group id to find what instances its attatched too
                        groupname = callsecgroups['SecurityGroups'][i2]['GroupName']
                        vpcid = callsecgroups['SecurityGroups'][i2]['VpcId']
                        wrong = []
                        if (test[0]['IpProtocol'] != '-1'):
                            wrong.append('Not TCP/UDP')
                        if (len(test) > 1):
                            wrong.append('Multiple IP Ranges')
                        global invalidrule
                        invalidrule.append(test)
                        global table2
                        table2.append([groupid,groupname,', '.join(wrong)])
                               
                                                                       
                i2 = i2+1
                
        ######################################################
        #Getting all instance names and appending to lst_of_i#
        ######################################################
                
        for instance in ec2.instances.all():
            
            state = instance.state
            if (state['Name'] == 'running' or state['Name'] == 'stopped'):
                
            
                if instance.tags:
                    
        
                    for tag in instance.tags:
                        
                
                        if tag['Key'] == 'Name':
                        
                            iname = tag['Value']
                            lst_of_i.append(iname)
                else:
                    
                    iname = 'no name'
                    lst_of_i.append(instance.instance_id)
                        
               
                        
                    
                
               
             
            ##########################################
            #Getting instances with/without security group#
            ##########################################
                        
                secgroup = instance.security_groups
                i4 = 0
                while ( i4 < len(secgroup) ):
                    
                    if (secgroup[i4]['GroupName'] == 'sgp-security-services'): 
                        #print(iname)
                        sec_groups.append(iname)
                        sec_id.append(instance.instance_id)
                        break
                        
                    if (i4+1 == len(secgroup)):
                        
                        no_secgrp_id_list2.append(instance.instance_id)
                        global table
                        table.append([instance.instance_id,iname,regions[i]])
    
                    i4 = i4+1
                
                id_list.append(instance.instance_id)

        if regions[i] == 'us-east-1':
            
            config = boto3.client('config',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],)
            #response = config.delete_evaluation_results(
            #ConfigRuleName='security-group-compliance'
        #)  
            #print(sec_id)####
            for x in id_list:
                #print(x)######
                if x in sec_id:
                    response = config.put_evaluations(
                        Evaluations=[
                            {
                                'ComplianceResourceType': 'AWS::EC2::Instance', #changed
                                'ComplianceResourceId': x,
                                'ComplianceType': 'COMPLIANT', #changed
                                "Annotation": 'Security group attached.', #changed
                                'OrderingTimestamp': invoking_event['notificationCreationTime'] #changed
                            },
                        ],
                        ResultToken=event['resultToken'])
                        
                else:
                    
                   # print('no group '+x) #gets up to here but does not put the eval for some reason.
                    
                    response = config.put_evaluations(
                        Evaluations=[
                            {
                                'ComplianceResourceType': 'AWS::EC2::Instance', 
                                'ComplianceResourceId': x,
                                'ComplianceType': 'NON_COMPLIANT', 
                                "Annotation": 'Security group not attached.', 
                                'OrderingTimestamp': invoking_event['notificationCreationTime'] 
                            },
                        ],
                        ResultToken=event['resultToken'])           
        i = i + 1
    global no_security_group        
    no_security_group = set(lst_of_i).difference(set(sec_groups)) #Result = What doesn't have the security group name
    no_security_group = list(no_security_group)

    global no_secgrp_id_list
    no_secgrp_id_list = set(id_list).difference(set(sec_id)) 
    no_secgrp_id_list = list(no_secgrp_id_list)
    
    #print(no_secgrp_id_list2) #area I append to table is wrong, no_security_group is correct, 
    #print(table)
    html2pdf()
    table.clear()
    table2.clear()
        
    #invoking_event = json.loads(event['invokingEvent'])
    #configItem = invoking_event["configurationItem"]
    #['resourceId']
    #evaluation = compliance_evalulator(configItem, triggername) #changed
    

                #print(response)
        
    id_list.clear()
   
#Calling Functions#
###################

#email()


    
