# aws-ec2-pricing
This python script reads the 'Data' worksheet of a formatted Excel workbook based on the included Hosts.xlsx spreadsheet file.  The script uses the CPU, RAM, Storage, and OS values along with command line parameters to assign instance types from the General Purpose family of AWS instances.  After running the script once you may assign any instance type in the 'Instance Final' column and run the script again using the -i switch with 'all' parameter to read existing instance values as input. Pricing is provided as a unit and daily cost in USD via AWS Pricing API.      

## Setup
To use this script you will need an AWS Account, Python, and AWS CLI.

### AWS Account:
1. Setup an AWS account
2. Create a new user with no console access and generate an access and secret key
3. Create an IAM policy named 'PricingFullAccess' using the following JSON code
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "pricing:DescribeServices",
                "pricing:GetAttributeValues",
                "pricing:GetProducts"
            ],
            "Resource": [
                "*"
            ]
        }
    ]
}
```
- Reference: [AWS Billing Permissions Example 11: Find products and prices](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/billing-permissions-ref.html)
4. Create a group named 'PricingOnly' and attach the PricingFullAccess policy
5. Add the user from step 2 to the PricingOnly group to restrict access to pricing information only

### Python for Windows:
1. Download Python3 (https://www.python.org/downloads/)
2. Install Python using the installer and check the box to add Python to PATH
   - Note: You can use Python2 as the script and modules are backwards compatible
3. Use PIP: Python's Package Manager to install required modules
- `C:\>python -V` Display Python version and confirms install
- `C:\>python -m pip list` Lists installed Python modules
- `C:\>python -m pip install argparse` Install the argparse module if not already installed by the installer
- `C:\>python -m pip install boto3` Install the AWS module
- `C:\>python -m pip install openpyxl` Install the Excel read/write module
   
### AWS CLI for Windows:
1. Download AWS CLI (https://s3.amazonaws.com/aws-cli/AWSCLI64.msi)
2. Install AWS CLI using the installer
3. `C:\aws configure` Setup AWS CLI with Access and Secret key for the AWS user
- Paste in the Access and Secret keys
- Set default region to us-east-1.  This region provides access to the Pricing API endpoint
- Set default output format to JSON

### Python3 and AWS CLI for MacOS:
For MacOS use Homebrew to install Python3, PIP, and AWS CLI *Some of the below commands may be optional
1. Install Homebrew using the following command:   
   `/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`
2. `brew list` Lists installed packages
3. `brew install python3` Installs Python3, you should now have python 2.X that ships with MacOS and python3 installed
5. `pip3 install awscli --upgrade --user` Use PIP to install AWS CLI
6. `aws --version` Verify that the AWS CLI is installed correctly  

If command is not found in step 5 you will need to add it to the PATH.
1. `$PATH` Check the current PATH
2. `export PATH=/Users/USERNAME/Library/Python/3.6/bin/:$PATH` Add Python3 bin folder to PATH
3. `$PATH` Check PATH again
4. `vi .bash_profile` Add to bash profile: `export PATH=~/Library/Python/3.6/bin/:$PATH`
5. `sudo vi /etc/path` Add /usr/local/sbin after /usr/local/bin  

## Usage
Place the aws-ec2-pricing.py script and Hosts.xlsx file in the same directory.  Use the -h switch to displays help info and available options.

### Assign initial instance type and price
Example: `C:\>python aws-ec2-pricing.py -f Hosts.xlsx -r us-west-2 -i m5 -v gp2`
- The script inspects the CPU and RAM values and selects an EC2 instance from the m5 family that will support the larger of the 2 variables.  As the script iterates through the rows it will convert storage from MB to GB and inspect the OS and retrieve the pricing matching the instance type, OS, storage and region.

### Read instance value and update pricing
Example: `C:\>python aws-ec2-pricing.py -f Hosts.xlsx -r us-west-2 -i all -v gp2`
- Using the 'all' parameter with the -i switch provides the option to manually assign instance types after initial assignment using any available instance type.  This skips the assignment and reads the value in the 'Instance Final' column and updates pricing accordingly.  

## Assumptions & Considerations
1. The unit pricing for both EC2 and EBS are converted into daily units.
2. Pricing assumes OnDemand, AWS Provided Licensing, No application bundles, Tenancy is shared.  These values can be changed in the script.
3. If the OS can't be matched against Windows, Red Hat, or SUSE (Which have licensing built into the EC2 pricing) the instance will assume Linux as the OS.
4. EC2 instances will match RAM in GB -2 where VM's having 16GB RAM may be assigned EC2 instance with 15GB RAM.  This method was choosen to avoid over-sizing instances.
5. The script does not factor in EBS snapshots which are currently $0.05 per/GB-month for data stored in all regions.  It's a good idea to account for atleast 1 full snapshot for each volume.
6. This script can easily be modified to work with RVTools output or other formats as required.  
