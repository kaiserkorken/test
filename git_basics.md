# Development 101
Just a collection of a few key concepts.

## Git Repository Layout
One general branching strategy is layed out below.

The default branches are:
- `main`: Holds only tested and stable code, clean and comprehensive commit history, generally populated only by merge requests/pull requests
- `develop`: Where active development happens, source for merges to `main` when certain milestones are reached

A generic branching strategy suggests the follwing branches:
- `feature/<CONCISE FEATURE DESCRIPTION/ISSUE REFERENCE>`: branch off, implement feature, merge back onto develop
- `bugfix/<BUG DESCRIPTION>`: branch off, fix bug _(something that is not too urgent and may have been there for a while)_, merge back onto develop 
- `hotfix/<BUG DESCRIPTION>`: branch off, fix bug _(something that needs fixing ASAP)_, merge back onto develop

And finally I suggest we actively work on branches like `enrico/<MYFEATURE>`, `christoph/<MYFEATURE>`, `peter/<MYFEATURE>` and share branches only of we communicate well enough to net get into each others way.

## Styleguide
The problem with code is, that even the code that somebody wrote himself becomes unfamiliar after a quite period of time. Let alone the code others wrote. So in order to ensure better readability _(lets make the analogy of 'speaking the same language')_ teams should align on a coding styleguide.

Each programming language has a ton of styleguides, for Python the standard is [PEP8](https://peps.python.org/pep-0008/). It would be too much to give an extensive summary here but let me give at least some key points:
- Class Names: `CamelCase`
- Function Names: `lower_case`
- Local Variable Names: `lower_case`
- Global Variable Names: `UPPERCASE`
- Functions in global scope are separated by 2 blank lines
- Methods (functions belonging to a class) are separated by 1 blank line

For the part that is mostly formatting, I suggest the tool [black](https://pypi.org/project/black/) which is very minimalistic and thus easy to use. I'll probably supply a guide how to install and set it up as a commit hook.

## Git
Git is the industry standard for version control. It takes quite a bit to get confident with it but you'll get the basics down quickly and shouldn't be indimidated by the more advanced stuff. Let me try to lay out some basics:
- Every object is a summary of changes made to it. Those changes are called `commits` and should come with a concise message that tells why the devloper did what he did.
- Commits are always applied to the `index` which is basically just collection of changes that are made to files.
- Due to its nature, git can only handle text files properly _(Not regarding the file extension, but the content. If you open the file in any text editor and see something that is not gibberish, then you're good to go.)_. Thats also the reason why TU does not want us to upload binary files to GitLab. Occasionally including smaller files is ok though.
- A repository consists of one or more branches that should ideally share the same origin and evolve together. This is not enforced, users can prodoce all sorts of mess
- When working together you might run into `merge conflicts` at some point. This sounds and looks very intimidating at first, but keep your calm.
    - A merge conflict simply means, that git was not able to automatically identify which version of the code should be preferred
    - It is glaringly indicated in the code by some `<<<<<<<`, `=======`, `>>>>>>>` where in between you'll find the two versions of problematic code
    - You can now resolve the conflict by manually replacing the entire chunk from `<<<<<<<` to `>>>>>>>` with one correct version of the code
    - Finally, you just create a new commit which indicates that it was issued in order to resolve the merge conflict
- Tags are a bit difficult to understand, but the key takeaway is, that a tag is mostly the same as a branch that does not evolve; it comes down to a being a pointer to a specific commit
- The most important commands are:
    - `git clone <MY REPOSITORY>`
    - `git pull`: Pulls the most recent version of the repository from GitLab and tries to merge it with your local changes, if not synchronized
    - `git push`: Push your local changes to the server
    - `git add <FILENAME>`: Add a file to the `index`, use the option `-i` if you want to apply only chunks of that file or preferably use your favourite IDE, most of them have GUI support for that
    - `git commit -m <MY COMMIT MESSAGE>`: Apply the commit to all changes in the index
    - `git switch <BRANCHNAME>`: Switch to a branch
    - `git checkout -b <NEW BRANCH NAME>`: Create a new branch
- And to list a few more advanced commands:
  - `git tag -a <TAGNAME> -m <TAG ANNOTATION>`: Tags the current commit with an annotated tag
  - `git fetch`: Gets objects from GitLab, but no source code; objects can be branchnames and commit hashes
  - `git merge`: **Fast-Forward** moves both branches to the tip of the advanced branch; **3 way merge** creates an additional merge commit that ties the diverged branches together; **squash** squashes all commits of the advanced branch into one and applies this to the other branch
  - `git rebase`: Automatically rewrites all commits so that they can be applied to the 'outdated' branch resulting in the state of the emerged branch
  - `git reset <COMMIT HASH>`: Deletes all commits until you're back to the state of `<COMMIT HASH>`; the file contents remain unchanged
  - `git reset --hard <COMMIT HASH>`: Deletes all commits and resets all files so that you're back to the state of `<COMMIT HASH>` 
  - `git reset -- hard origin/<BRANCHNAME>`: Gets you back to the clean state of GitLabs `origin/<BRANCHNAME>`, all local changes are discarded
  - `git revert`: Considered a safer alternative to reset because it issues a new commit that gets you back to the old state
