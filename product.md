## Product idea

Naomi is an AI assistent for EVE Online capsuleers.  Naomi is embedded in a website that allows users to plan and manage their EVE journey.  Naomi has real-time access to a capsuleer's assets, skills, and location, and markets so she can help you plan exploration runs, missions, hauling contracts, mining operations, and production pipelines.


## Financials

The site is support financially with advertising (that compiles with EVE Online's TOS).

User must bring their own model (provide an API key).

## MVP / Milestones

- website that can authenticate a user against the EVE Online account
- website can handle GDPR requests
- backend has an MCP server like jmoody/vael


## Techincal

### Language + frameworks

- Golang
- Terraform
- bash
- Service runs in Docker noble.

### Golang

- go-chi/chi/v5
- hashicorp/go-retryablehttp
- sony/gobreaker/v2
- kelseyhightower/envconfig
- mark3labs/mcp-go
- stretchr/testify
- go.uber.org/mock


### SaaS

Use Azure for:

- Monitoring / Alerting
- Log aggregation
- Redis
- Database
- Microsoft Foundry for AI
- Secrets

GitHub for:

- hosting
- CI

## Don't forget

- GDPR from the beginning

## Questions

- Hosts or kubernetes?
- Web framework and web language?
- Users must be able to bring their own model.
- Is there a CI/CD pipeline in Azure that I can adopt?
- How to manage website certificates?
- Authn/z between the frontend and the backend service(s)?

