$ErrorActionPreference = 'Stop'

Write-Host 'Checking compose configuration...'
docker compose config --quiet

Write-Host 'Checking Ansible playbook syntax...'
ansible-playbook -i ansible/inventory.ini ansible/site.yml --syntax-check

Write-Host 'Checking Terraform formatting and validation...'
terraform -chdir=terraform fmt -check
terraform -chdir=terraform init -backend=false
terraform -chdir=terraform validate

Write-Host 'Checking Python syntax...'
python -m compileall app tests
