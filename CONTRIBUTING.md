# Contributions

Contributions are welcome in the form of pull requests. We heavily rely on the
contribution guides of [MNE-Python](https://mne.tools/stable/install/contributing.html)

Once the implementation of a piece of functionality is considered to be bug
free and properly documented (both API docs and an example script),
it can be incorporated into the `main` branch.

To help developing `causalscm`, you will need a few adjustments to your
installation as shown below.

## Running tests

### Install development version of CausalSCM
First, you should [fork](https://help.github.com/en/github/getting-started-with-github/fork-a-repo) the `causalscm` repository. Then, clone the fork and install it in
"editable" mode.

    $ git clone https://github.com/<your-GitHub-username>/causalscm
    $ pip install -e ./causalscm


### Install Python packages required to run tests
Install the following packages for testing purposes, plus all optonal causalscm
dependencies to ensure you will be able to run all tests.

    $ pip install -r requirements_testing.txt

### Invoke pytest
Now you can finally run the tests by running `pytest` in the
`causalscm` directory.

    $ cd causalscm
    $ pytest

## Building the documentation

The documentation can be built using sphinx. For that, please additionally
install the following:

    $ pip install -r requirements_doc.text

To build the documentation locally, one can run:

    $ cd doc/
    $ make html

or

    $ make html-noplot

if you don't want to run the examples to build the documentation. This will result in a faster build but produce no plots in the examples.

### Issues with Memory Usage

All documentation examples are built on a CI pipeline that occurs online for free. For example, our docs are built with circleCI perhaps. This limits the ability for us to run large data examples that have a lot of RAM usage. For this reason, many times we crop, downsample, or limit the analysis in some way to reduce RAM usage.

Some good tools for profiling memory are ``mprof``. For example, one can memory profile a specific example, such as:

    mprof run examples/connectivity_classes.py

Then one could plot the memory usage:

    mprof plot