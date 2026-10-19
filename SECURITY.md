# Security

This is an early development milestone, not a security-audited hosted service. Only the current development branch is maintained.

Use GitHub private vulnerability reporting on this repository for security issues. Avoid public exploit details or credentials. No response-time guarantee or bug bounty is offered.

The web app and runner must use separate origins. Production deployment must use a separate registrable domain for the runner, not merely a sibling subdomain sharing cookies. Never place authentication, tokens, private files, a backend proxy, or user uploads on the runner origin. It serves only immutable public runtime assets and public evaluators.

Read docs/architecture.md before changing the runner. The server's CSP response headers are mandatory; opening its HTML from a generic server that omits them is not equivalent. The frame permits scripts and same-origin solely because its origin is different from the application. Never host it on the application origin.

Local results are learner-controlled. They must not be trusted for credentials, competitions, or backend authorization. Browser worker termination bounds ordinary run duration but provides no hard browser memory quota. Device resource exhaustion and browser-engine vulnerabilities are residual risks.
