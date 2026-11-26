# Architecture and development

UI: `web/` presents tasks, plans, patches and test evidence. Transport: `src/web_runtime.py` accepts same-origin local requests and serializes operations on one worker. Application: `src/web.py` coordinates explicit browser approvals. Domain behavior: `src/manager/` owns workflow state, `src/agents/` owns generation, `src/providers/` owns external model calls, and `src/tools/` owns Git and pytest execution.

Run `python -m src.web` and open `http://forge.localhost:8011`. Provide the absolute path of a clean linked worktree, then create a plan. Approve generation, review the patch, and apply it with tests. Review all changed files, including new files in the target worktree, before committing. Continue advances the plan after a successful commit. Retries forward failure output to OmniRoute. `OMNIROUTE_BASE_URL`, `OMNIROUTE_MODEL`, and `OMNIROUTE_API_KEY` configure the external service. The browser runner never pushes a target repository automatically.

## Engineering conventions

Each repository is independently runnable. Presentation calls a transport adapter, which invokes application behavior. I/O stays at explicit boundaries so tests can replace external providers. Long browser operations have one owner, reject overlapping requests, and report success or failure through the UI. Relay uses async provider requests; video and desktop work use a worker or an existing sequential CLI loop.

New behavior should validate input before touching a user's files or desktop, report partial failures accurately, and have a regression test for a concrete failure mode. Run the repository's checks before committing and document the exact manual checks separately from mocked tests.

The local apps share a request/status pattern, accessible form controls, and a responsive layout. Small standard-library transports are kept inside each repository so they do not require a sixth repository at runtime. The matching transport modules should be updated together when changing that contract.

## Local addresses

The browser resolves `.localhost` names to the loopback interface. These addresses are scoped to this computer. Start the Python process before opening the address. Chrome and Edge support this setup. A distinct port lets each project run alongside the others without an OS hosts-file change.

## Evaluation

Automated checks verify the workflows represented by their fixtures. Real model access, physical microphones and desktop focus still need environment-specific checks. CI is included under `.github/workflows/checks.yml`; its remote result must be checked after pushing.

Remaining work should be driven by observations from real use. Dataset accuracy, provider access and desktop-device behavior cannot be established by a successful test run alone.

## Verification for this change

37 tests passed with one skip. Chrome completed plan, patch review, real pytest execution, selective commit and plan completion in a disposable linked worktree with fake model generation. The live OmniRoute service still needs a separate integration check.
