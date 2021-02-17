# Contributing

Contributing is easy and welcome
 
You can contribute to PyOWM in a lot of ways:

  - reporting a reproducible defect (eg. bug, installation crash, ...)
  - make a wish for a reasonable new feature
  - increase the test coverage
  - refactor the code
  - improve PyOWM reach on platforms (eg. bundle it for Linux distros, managers, coding, testing, packaging, reporting issues) are welcome!
  
And last but not least... use it! Use PyOWM in your own projects, as [lots of people already do](https://github.com/csparpa/pyowm/wiki/Community-Projects-using-PyOWM).


In order to get started, follow these simple steps:

  1. First, meet the community and wave hello! You can join the **[PyOWM public Slack team](https://pyowm.slack.com)** by signing up [here](http://pyowm-slackin.herokuapp.com/)
  2. Depending on how you want to contribute, take a look at one of the following sections
  3. Don't forget tell @csparpa or the community to add yourself to the `CONTRIBUTORS.md` file - or do it yourself if you're contributing on code 


# Reporting a PyOWM bug
That's simple: what you need to do is just open a new issue on GitHub.


## Bug reports - general principles
In order to allow the community to understand what the bug is, *you should provide as much information as possible* on it.
Vague or succinct bug reports are not useful and will very likely result in follow ups needed.

*Only bugs related to PyOWM will be addressed*: it might be that you're using PyOWM in a broader context (eg. a web application)
so bugs affecting the broader context are out of scope - unless they are caused in chain to PyOWM issues.

Also, please do understand that we can only act on *reproducible bugs*: this means that a bug does not exist if it is
not possible to reproduce it by two different persons. So please provide facts, not "smells of a potential bug" 


## What a good bug report should contain
These info are part of a good bug report:
  - brief description of the issue
  - *how to reproduce the issue*
  - what is the impacted PyOWM issue
  - what Python version are you running PyOWM with
  - what is your operating system
  - stacktrace of the error/crash if available
  - if you did a bit of research yourself and/or have a fix in mind, just suggest please :)
  - (optional) transcripts from the shell/logfiles or screenshots


# Requesting for a new PyOWM feature
That's simple as well!

1. Open an issue on GitHub (describe with as much detail as possible the feature you're proposing - and also
2. Depending on the entity of the request:
   - if it's going to be a breaking change, the feature will be scheduled for embedding into the next major release - so no code shall be provided by then
   - if it's only an enhancement, you might proceed with submitting the code yourself!


# Contributing on code
This applies to all kind of works on code (fixing bugs, developing new features, refactoring code, adding tests...)

A few simple steps:
  1. Fork the PyOWM repository on GitHub
  2. Install the development dependencies on your local development setup
  3. On your fork, work on the **development branch** (_not the master branch!!!_) or on a **ad-hoc feature branch**. Don't forget to insert your name in the `CONTRIBUTORS.md` file!
  4. TEST YOUR CODE please!
  5. DOCUMENT YOUR CODE - especially if new features/complex patches are introduced 
  6. Submit a [pull request](https://help.github.com/articles/about-pull-requests/)


## Installing development dependencies
In order to develop code and run tests for PyOWM, you must have installed the dev dependencies. From the project root folder,
just run:

`pip install -r dev-requirements.txt`

It is advised that you do it on a [virtualenv](https://virtualenv.pypa.io/en/stable/).

## Guidelines for code branching
Simple ones:

- the "develop" branch contains work-in-progress code 
- the "master" branch will contain only stable code and the "develop" branch will be merged back into it only when a milestone is completed or hotfixes need to be applied. Merging of "develop" into "master" will be done by @csparpa when releasing - so please **never apply your modifications to the master branch!!!**


## Guidelines for code testing
Main principles:

  - Each software functionality should have a related unit test
  - Each bug should have at least one regression test associated


# Contributing on PyOWM bundling/distributing
Please open a GitHub issue and get in touch to discuss your idea!
