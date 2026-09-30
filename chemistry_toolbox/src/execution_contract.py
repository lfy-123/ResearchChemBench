"""One description of Action execution for catalogs, tools and run prompts."""
import os


def action_execution_description(persistent=None):
    if persistent is None:
        persistent = os.environ.get("RESEARCHCHEMBENCH_RECOVERY_ENABLED") == "1"
    mode = ("In this recovery-enabled run, execute_action returns an asynchronous job_id and submission receipt. "
            if persistent else "execute_action returns an asynchronous job_id when a submission_key is provided; otherwise it returns a synchronous Action result. ")
    return mode + (
        "Use validate_action for input/electronic-state preflight without starting a calculation. "
        "Keep the submission_key and receipt. get_execution_job and wait_execution_jobs expose structured diagnostics, "
        "warnings and usable artifacts. collect_execution_job provides a stable result receipt and a readable full-result reference. "
        "After response loss look up the original submission and job; changed inputs require a new key. "
        "Execution completion does not establish scientific validity."
    )
