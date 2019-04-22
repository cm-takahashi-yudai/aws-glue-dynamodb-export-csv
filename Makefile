test-unit:
	@python -m pytest -v tests/unit

test-e2e:
	@python -m pytest -v tests/e2e

lint:
	@flake8 src tests
	@pydocstyle src tests

deploy-datastore:
	@aws cloudformation deploy \
		--template-file templates/datastore.yaml \
		--stack-name ${PROJECT_NAME}-${STAGE_NAME}-datastore-stack \
		--parameter-overrides ProjectName=${PROJECT_NAME} StageName=${STAGE_NAME} \
		--no-fail-on-empty-changeset \
		--capabilities CAPABILITY_IAM

deploy-glue:
	@aws cloudformation deploy \
		--template-file templates/glue.yaml \
		--stack-name ${PROJECT_NAME}-${STAGE_NAME}-glue-stack \
		--parameter-overrides ProjectName=${PROJECT_NAME} StageName=${STAGE_NAME} \
		--no-fail-on-empty-changeset \
		--capabilities CAPABILITY_NAMED_IAM

deploy-glue-crawler:
	@aws glue create-crawler \
		--name ${PROJECT_NAME}-${STAGE_NAME}-glue-crawler \
		--role ${PROJECT_NAME}-${STAGE_NAME}-glue-role \
		--database-name ${PROJECT_NAME}-${STAGE_NAME}-glue-database \
		--targets '{"DynamoDBTargets": [{"Path": "${PROJECT_NAME}-${STAGE_NAME}-target"}]}'

deploy-step-functions:
	# Step Functions

deploy-all:
	@make deploy-datastore
	@make deploy-glue
	@make deploy-glue-crawler
	@make deploy-step-functions

delete-stack-all:
	@aws s3 rm s3://${PROJECT_NAME}-${STAGE_NAME}-glue-script --recursive
	@aws s3 rm s3://${PROJECT_NAME}-${STAGE_NAME}-result --recursive
	@aws cloudformation delete-stack --stack-name ${PROJECT_NAME}-${STAGE_NAME}-datastore-stack
	@aws cloudformation delete-stack --stack-name ${PROJECT_NAME}-${STAGE_NAME}-glue-stack
