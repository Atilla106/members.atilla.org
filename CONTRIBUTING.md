Contributing
===

Hi there ! Welcome to the contribution documentation of this project !

Developing on members.atilla.org is fairly easy compared to many other Open Source projects, but in order to keep a clean organization and a clean code base, here are some informations and guidelines that we encourage you to follow in your development process.

Project Licensing
---

This project is using a [MIT license](https://opensource.org/licenses/MIT) registered in the name of the Association ATILLA. Therefore, every code addition made on this project repository should agree with this license and, by doing so, the original code author (which can be you !) agrees that he can’t be held liable for the work he has done on the platform (for more resources, see https://tldrlegal.com/license/mit-license).

Issues management
---

Every code added, modified or deleted on the platform should be linked to a GitLab issue. This allows every developer on the project to be kept informed of new features, bugs or proposals.

Please don’t use issues to discuss about a code change you made ; discussions revolving around a patch must be contained in the associated merge request.

Branching model
---

The project is composed of 3 main branches : `master`, `preprod` and `dev`.

* `master` is updated every time a new version or a hotfix is released, every new commit on `master` gets a tag assigned to specify the platform version.
* `preprod` is (sometimes) used to test the platform versions before released.
* `dev` contains the last version of the platform currently in development. Theoretically, every new code added, modified or deleted on the platform should come from a merge request made on `dev`. Then, `dev` is merged onto `preprod` or `master`.

As we need to keep our code base as clean as possible, currently no direct commit are allowed on `dev`, `preprod` or `master` and merge requests can only be accepted if the CI linked to this project does not fail.

The naming of development branches isn’t really restricted, but we encourage you to use prefixes in your branch names such as `feature/` or `fix/` in order to make them more distinguishable.

Syntax
---

Code usually goes through [`pep8`](https://www.python.org/dev/peps/pep-0008/) validation. You can check your code syntax by using `flake8`, a pip package provided in the `requirements-tests.txt` file.

Documentation
---

Currently, we don’t have any guideline regarding code documentation, if we want the project to evolve cleanly, we might have to fix that.

However, if you fell like it, you can contribute to the user / administrator documentation available on [this wiki page](https://wiki.atilla.org/index.php?title=Members.atilla.org) (in french).

Developer workflow guide
===

If you ever feel lost in your development process, here is a simple guide that you can follow :

1. Supposing a bug or a feature has been notified by the users, this has to be reported on the project as an issue with a descriptive description and useful tags.
2. A developer will then create a new branch based on `dev` where he'll make the necessary code changes.
3. In case he needs advice from others, he can publish an early merge request for his branch to land onto `dev`, with the `WIP:` prefix, preventing the branch to be accidentally merged.
4. Discussions revolving around a patch must be contained in the associated merge request.
5. When the feature / bug is ready to review, the assignee is changed to one of the head developer of the project, and the `WIP:` prefix is removed (if present).
6. Comments about the code shall be made directly through the Gitlab code comment feature.
7. People can validate a merge request by posting in the MR comment section "LGTM".
8. When everyone agrees, the MR is accepted.

---

Finally, as a last advice, do not hesitate to contact the project developers if you have any question on this project development. We will be very happy to answer you !

