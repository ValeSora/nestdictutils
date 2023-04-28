# Getting started

## Installing `nestdictutils`

`nestdictutils` is a Python package requiring **Python 3.8 or higher**.

`nestdictutils` has been tested only on Unix-based systems.

Here, we provide instructions for installing `nestdictutils` in a simple Python environment or a `conda` one.

We will show the installation using Python 3.8, but the same steps remain valid for later Python versions.

### Installing in a Python virtual environment

This section guides you in installing the `nestdictutils` package in a virtual environment, meaning an instance of Python that is isolated from the rest of your system.

This is not strictly necessary, and `nestdictutils` may be installed system-wide similarly, following steps 4 to 5.

#### Step 1 - Install `virtualenv`

First, check if the `virtualenv` Python package is installed in your system. This can be done by verifying whether the `virtualenv` command is available to you.

It is usually available as a package in your distribution if you need to install it. For instance, on Debian-based systems (such as Debian or Ubuntu), it is sufficient to install the `python-virtualenv` package.

If you want to install it system-wide, run:

```
sudo apt install python-virtualenv
```

If this is not possible for you, you may still install the `virtualenv` package for just your local user, using `pip`:

```
pip install --user virtualenv
```

If the installation is successful, the `virtualenv` command will be available.

#### Step 2 - Create the virtual environment

Create your virtual environment in a directory of your choice (in this case, it will be `./nestdictutils-env`):

```
virtualenv -p /usr/bin/python3.8 nestdictutils-env
```

You should replace the argument of option `-p` according to the location of your Python installation in the system.

#### Step 3 - Activate the environment

Activate the environment:

```
source nestdictutils-env/bin/activate
```

#### Step 4 - Get `nestdictutils`

Clone the `nestdictutils` source code from its GitHub repository and enter the local copy of the repository.

```
cd ..
git clone https://github.com/MesserMbabu/nestdictutils.git
cd nestdictutils
```

If `git` is unavailable, you can download the repository content as a ZIP file from the `nestdictutils` GitHub repository web page, unzip it, and enter it.

#### Step 5 - Install `nestdictutils`

You can now install `nestdictutils`:

```
python setup.py install
```

`nestdictutils` should now be installed.

Every time you need to run `nestdictutils` after opening a new shell, just run step 3 beforehand.

### Installing with `conda`

#### Step 1 - Install `conda`

Go [here](https://docs.conda.io/en/latest/miniconda.html) for detailed instructions on how to install `conda`.

Installing `miniconda` rather than the full `anaconda` package is advised.

Once `conda` is installed on your system, you can use it to create a virtual environment, similarly to what you would do using the `virtualenv` package, as previously detailed.

#### Step 2 - Create the `conda` environment

You can create your `conda` environment from the provided environment file:

```
conda env create --prefix ./nestdictutils-env
```

In this case, we ask `conda` to create the environment locally (`--prefix`), but this is optional.

#### Step 3 - Activate the environment

You can activate the `conda` environment by running the command line that `conda` suggests at the end of the previous step.

It is usually something like this:

```
conda activate ./nestdictutils-env
```

#### Step 4 - Get `nestdictutils`

Clone the `nestdictutils` source code from its GitHub repository and enter the local copy of the repository.

```
cd ..
git clone https://github.com/MesserMbabu/nestdictutils.git
cd nestdictutils
```

If `git` is unavailable, you can download the repository content as a ZIP file from the `nestdictutils` GitHub repository web page, unzip it, and enter it.

#### Step 5 - Install `nestdictutils`

You can now install `nestdictutils`:

```
python setup.py install
```

`nestdictutils` should now be installed.

Every time you need to run `nestdictutils` after opening a new shell, just run step 3 beforehand.