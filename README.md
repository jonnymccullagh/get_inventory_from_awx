# get_inventory_from_awx
Python3 script to pull an inventory from the Ansible AWX Server API
 Updated from [rpetti's Gist](https://gist.github.com/rpetti/fb538b1e72c73f25350b944be18d4b0e)


Usage:
```
python ../get_inventory_from_awx.py --url https://awx.domain.com -u admin -p "topsecret" "my-ec2-dev-inventory"
```
The final parameter is the name of the inventory as specified in the AWX UI. 
