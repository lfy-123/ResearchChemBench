---
software_id: gaussian
versions: ["16"]
topics: [troubleshooting, errors]
aliases: [Gaussian failed, route error, EOF error]
---
# Gaussian Troubleshooting

## Early EOF or title error
Check the mandatory blank lines and ensure the input ends with a newline. Route, title, molecule specification, and coordinates must be separate sections.

## Route failure
Confirm keyword spelling, parentheses, method/basis syntax, and installed Gaussian revision. Do not copy ORCA-style blocks or shell quoting into the route.

## Resource failure
Match `%NProcShared` and `%Mem` to the scheduler request. Increasing memory does not repair an invalid route or missing input section.
