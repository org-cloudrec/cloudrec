terraform-plan:
	cd cloudrec/terraform && terraform plan

terraform-apply:
	cd cloudrec/terraform && terraform apply

terraform-destroy:
	cd cloudrec/terraform && terraform destroy

create-zip-function:
	cd cloudrec/terraform/modules/cloud_functions/function_export
	python -m venv env
	env\Scripts\activate
	pip install -r requirements.txt
	pip freeze > requirements.txt
	7z a function.zip *
	cd ../../../../..

create-config:
	@copy cloudrec/terraform/credencials.tfvars.example cloudrec/terraform/credencials.tfvars

pip-install:
	pip install -r requirements.txt
	pip install -r cloudrec/terraform/modules/cloud_functions/function_export/requirements.txt