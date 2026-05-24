
export GOPROXY := https://proxy.golang.org,direct
export GOSUMDB := sum.golang.org

bootstrap:
	script/bootstrap-macos

clean:
	rm -rf bin
	rm -rf _tools
	go clean -cache -testcache -modcache

build: tidy imports
	script/build.sh

imports:
	bin/goimports -local github.com/jmoody/cem -w cmd internal test

kill:
	lsof -i :9010 -t | xargs -r kill -9

lint: build
	bin/golangci-lint run --max-issues-per-linter=0 --max-same-issues=0 ./...

lint-fix: build
	bin/golangci-lint run --fix --max-issues-per-linter=0 --max-same-issues=0 ./...

test: build
	@echo "Running unit tests (excluding integration tests)"
	bin/gotestsum -- -race -v -cover ./cmd/... ./internal/...

tidy:
	go mod download
	go mod tidy

update:
	go get -u ./...
	go mod tidy

review: bootstrap imports lint-fix test test-integration
