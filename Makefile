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
	@aws s3 sync \
		--exact-timestamps \
		--delete \
		src/glue \
		s3://${PROJECT_NAME}-${STAGE_NAME}-glue-jobs
	@aws glue start-trigger \
		--name ${PROJECT_NAME}-${STAGE_NAME}-create-csv-glue-trigger

deploy-all:
	@make deploy-datastore
	@make deploy-glue

delete-stack-all:
	@aws s3 rm s3://${PROJECT_NAME}-${STAGE_NAME}-glue-jobs --recursive
	@aws s3 rm s3://${PROJECT_NAME}-${STAGE_NAME}-result --recursive
	@aws cloudformation delete-stack --stack-name ${PROJECT_NAME}-${STAGE_NAME}-datastore-stack
	@aws cloudformation delete-stack --stack-name ${PROJECT_NAME}-${STAGE_NAME}-glue-stack

dynamodb-put-sample-items:
	@python src/dynamodb/put_sample_items.py
