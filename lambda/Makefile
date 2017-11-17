.PHONY: dist depends test install

#LAMBDA_FUNCTION_NAME=test-image-compare

install: dist
	aws lambda update-function-code --function-name $(LAMBDA_FUNCTION_NAME) --zip-file fileb://`pwd`/dist/lambda.zip

test:
	python test.py

depends:
	python depends.py

dist:
	cp service.py dist
	cd dist && zip -r lambda.zip service.py PIL


