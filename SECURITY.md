# Security Policy

AuditorSecSuite_PRE is a dual-use internal security-audit support tool.

## Supported use

This project is intended for:

- personal use;
- internal company security reviews;
- assets owned by the operator;
- assets with explicit authorization.

It is not intended for unauthorized scanning, exploitation, brute force, destructive testing, destructive actions, or third-party targeting.

## Reporting vulnerabilities

Do not open public issues with secrets, credentials, real audit evidence, logs containing sensitive data, or private target details.

Use a private channel with the repository owner when reporting sensitive vulnerabilities.

## Repository safety rules

The repository must not contain:

- .env files;
- credentials;
- API tokens;
- private keys;
- certificates;
- database dumps;
- runtime logs;
- storage contents;
- real audit evidence;
- customer or third-party data.

Before public pushes, run:

    ./Documentacio/scripts/publication_preflight.sh
