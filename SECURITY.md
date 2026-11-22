# Security policy

## Supported versions

Only the default branch (`main`) is supported. There is no released version yet.

## Reporting a vulnerability

Report it privately through GitHub: open the repository's **Security** tab and choose **Report a vulnerability**. Do not open a public issue or pull request for it.

Include what you found, the steps or input that trigger it, and the commit you tested. You will get a reply from the owner as soon as they can; this is a personal project with no service level.

The simulator is offline: it binds `127.0.0.1` only, sends no outgoing requests and uses synthetic data. Imported scenario and replay files are treated as untrusted input. Reports about either are in scope.
