---
description: Verify the current change against acceptance criteria and affected agent context.
agent: build
---

Load `jinx-verify-change` for the current change only, including affected mandatory layout and central-configuration consumers. Don't initialize a project or repair broad drift. Remediation requires authorization and stays task-scoped; read-only verification makes no edits. Report PASS, FAIL, BLOCKED, or NOT_APPLICABLE per check, separating structural adoption from feature behavior; a blocked or unknown required check isn't a pass.

Additional user instructions:

$ARGUMENTS
