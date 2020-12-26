sam build --use-container --template-file template.yaml

sam package --s3-bucket cc-final-project-cloudformation --output-template-file packaged.yaml

sam deploy --template-file ./packaged.yaml --stack-name cc-final-project-cloudformation-stack --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND

