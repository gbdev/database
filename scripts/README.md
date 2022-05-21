# scripts

Scripts to run batch jobs on the entries. These actions are potentially destructives and they must be audit-able. A rollback can be put in place in case of need, so make sure to:

- log decisions and actions
- commit the script before the application of the batch job
- commit the "effects" of a script in a separate commit, having a message starting with `batch` and putting the output of the script log in the additional git commit "-m" field.

##### DO NOT CHANGE THE NUMBER OF THE SCRIPT AT THE START OF THE FILENAMES

This number is used to reference the job (result) in "batch" commit messages. Don't change it.
