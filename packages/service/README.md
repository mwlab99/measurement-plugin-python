# Measurement Plug-In SDK Service for Python

- [Measurement Plug-In Service for Python](#measurement-plug-in-sdk-service-for-python)
  - [Introduction](#introduction)
  - [Dependencies](#dependencies)
  - [Documentation](#documentation)
  - [System Configuration](#system-configuration)
    - [Enable Win32 Long Paths](#enable-win32-long-paths)
  - [Examples](#examples)
  - [Developing Measurements: Quick Start](#developing-measurements-quick-start)
    - [Installation](#installation)
    - [Developing a minimal Python measurement](#developing-a-minimal-python-measurement)
  - [Steps to run/debug the measurement service](#steps-to-rundebug-the-measurement-service)
  - [Static Registration of Python Measurements](#static-registration-of-python-measurements)
    - [Create a batch file that runs a Python measurement](#create-a-batch-file-that-runs-a-python-measurement)
    - [Create Executable for Python Scripts](#create-executable-for-python-scripts)
  - [Troubleshooting](#troubleshooting)
    - ["File not found" or "No such file or directory" errors when copying or running a measurement service](#file-not-found-or-no-such-file-or-directory-errors-when-copying-or-running-a-measurement-service)
  - [Appendix: Managing Measurement with Python](#appendix-managing-measurement-with-python)
    - [Create and Manage Python Measurement using Poetry](#create-and-manage-python-measurement-using-poetry)
    - [Create and Manage Python Measurement using `venv`](#create-and-manage-python-measurement-using-venv)
    - [Create and Manage Python Measurement by directly installing `ni-measurement-plugin-sdk` as a system-level package](#create-and-manage-python-measurement-by-directly-installing-ni-measurement-plugin-sdk-as-a-system-level-package)

---

## Introduction

Measurement Plug-In SDK Service for Python (`ni-measurement-plugin-sdk-service`) is a Python
framework that helps you create reusable measurement plug-ins using gRPC
services. Deploy your measurement plug-ins to perform interactive validation in
InstrumentStudio and automated testing in TestStand.

---

## Dependencies

- [Python >= 3.9](https://www.python.org/downloads/release/python-3913/)
- [grpcio >= 1.49.1, < 2.x](https://pypi.org/project/grpcio/1.49.1/)
- [protobuf >= 4.21](https://pypi.org/project/protobuf/4.21.0/)
- [pywin32 >= 303 (Only for Windows)](https://pypi.org/project/pywin32/303/)

---

## Documentation

- [Measurement Plug-In SDK Manual](https://www.ni.com/docs/en-US/bundle/measurementplugins/)
- [API Reference](https://ni.github.io/measurement-plugin-python/)

---

## System Configuration

### Enable Win32 Long Paths

By default, Windows has a path length limit of 260 characters. NI recommends enabling support for long paths when developing and deploying Python measurement services.

There are three ways to do this:
- When installing Python using the Python for Windows installer, click `Disable path length limit` at the end of the installation.
- Set the `Enable Win32 long paths` group policy:
  - Run `gpedit.msc`.
  - Expand `Computer Configuration` » `Administrative Templates` » `All Settings`.
  - Find `Enable Win32 long paths` in the list, double-click it, and set it to `Enabled`.
- In the Windows registry, set `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\FileSystem\LongPathsEnabled` (type: `REG_DWORD`) to 1. For more details, see [Maximum Path Length Limitation](https://learn.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation).

---

## Examples

The `examples` directory contains example measurements for use with InstrumentStudio 2024 Q3 or later.

For more information on setting up and running the example measurements, see the included `README.md` file.

For best results, use the example measurements corresponding to the version of InstrumentStudio
that you are using. Newer examples may demonstrate features that are not available in older
versions of InstrumentStudio.

---

## Developing Measurements: Quick Start

This section provides instructions to develop custom measurement services in Python using Measurement Plug-In SDK for Python.

### Installation

Make sure the system has the recommended Python version installed. Install Measurement Plug-In SDK for Python using [pip](https://pip.pypa.io/).

``` cmd
REM Activate the required virtual environment if any.
pip install ni-measurement-plugin-sdk
```

Check if you have installed the expected version of Measurement Plug-In SDK for Python installed by running the below command:

```cmd
pip show ni-measurement-plugin-sdk
```

### Developing a minimal Python measurement

1. Run the `ni-measurement-plugin-generator` tool. Use command line arguments to specify the `display-name` and optionally the `version`, `measurement-type`, and `product-type`.

    1. Running `ni-measurement-plugin-generator` without optional arguments:

    `ni-measurement-plugin-generator SampleMeasurement`

    'SampleMeasurement' is the display name of your measurement service. Without the optional arguments,
    the other arguments are generated for you based on the display name.

    2. Running `ni-measurement-plugin-generator` with optional arguments for `measurement-version`, `ui-file`,
    `service-class`, and `description-url`:

    `ni-measurement-plugin-generator SampleMeasurement --measurement-version 0.1.0.0 --ui-file MeasurementUI.measui --service-class SampleMeasurement_Python --description-url https://www.example.com/SampleMeasurement.html`

    3. Running `ni-measurement-plugin-generator` with optional argument for `directory-out`

    `ni-measurement-plugin-generator SampleMeasurement --directory-out <new_path_for_created_files>`

    If no output directory is specified, the files will
    be placed in a new folder under the current directory
    named after the display name without spaces.

2. To customize the created measurement, provide metadata of the measurement's configuration (input parameters) and outputs (output parameters) in `measurement.py`.
    1. Use the `configuration()` decorator to provide metadata about the configurations.**The order of the configuration decorator must match with the order of the parameters defined in the function signature.**

        ``` python
        @foo_measurement_service.register_measurement
        #Display Names can not contains backslash or front slash.
        @foo_measurement_service.configuration("DisplayNameForInput1", DataType.String, "DefaultValueForInput1")
        @foo_measurement_service.configuration("DisplayNameForInput2", DataType.String, "DefaultValueForInput2")
        def measure(input_1, input_2):
            ''' A simple Measurement method'''
            return ["foo", "bar"]
        ```

    2. Use the `output()` decorator to provide metadata about the output.**The order of the output decorators from top to bottom must match the order of the values of the list returned by the function.**

        ``` python
        @foo_measurement_service.register_measurement
        @foo_measurement_service.configuration("DisplayNameForInput1", nims.DataType.String, "DefaultValueForInput1")
        @foo_measurement_service.configuration("DisplayNameForInput2", nims.DataType.String, "DefaultValueForInput2")
        @foo_measurement_service.output("DisplayNameForOutput1", nims.DataType.String)
        @foo_measurement_service.output("DisplayNameForOutput2", nims.DataType.String)
        def measure(input_1, input_2):
            return ["foo", "bar"]
        ```

3. Run/Debug the created measurement by following the steps discussed in the section ["Steps to run/debug the measurement service".](#steps-to-rundebug-the-measurement-service)

---

## Steps to run/debug the measurement service

1. Start the discovery service if not already started.

2. (Optional) Activate related virtual environments. Measurement developers can skip this step if they are not using any [virtual environments](#create-and-manage-python-measurement-using-venv) or [poetry-based projects.](#create-and-manage-python-measurement-using-poetry)

    ```cmd
    .venv\scripts\activate
    ```

    - After successful activation, you can see the name of the environment, `(.venv)` is added to the command prompt.
    - If you face an access issue when trying to activate, retry after allowing scripts to run as Administrator by executing the below command in Windows PowerShell:

        ```cmd
        Set-ExecutionPolicy RemoteSigned
        ```

3. [Run](https://code.visualstudio.com/docs/python/python-tutorial#_run-hello-world)/[Debug](https://code.visualstudio.com/docs/python/debugging#_basic-debugging) the measurement Python file.

4. To stop the running measurement service, press `Enter` in the terminal to properly close the service.

5. (Optional) After the usage of measurement, deactivate the virtual environment. Measurement developers can skip this step if they are not using any [virtual environments](#create-and-manage-python-measurement-using-venv) or [poetry-based projects.](#create-and-manage-python-measurement-using-poetry)

    ```cmd
    deactivate
    ```

---

## Static Registration of Python Measurements

The NI Discovery Service provides a registry of other services, and can discover and activate other services on the system. These features allow the discovery service to distinguish, manage, and describe measurement services on the system.

To statically register a measurement service with the NI Discovery Service, do the following:

1. Create a [startup batch file](#create-a-batch-file-that-runs-a-python-measurement) or [executable](#create-executable-for-python-scripts) for the measurement service.

2. Edit the measurement service's `.serviceconfig` file and set the `path` value to the filename of the startup batch file or executable.

3. Copy the measurement service's directory (including the `.serviceconfig` file and startup batch file) to a subdirectory of `C:\ProgramData\National Instruments\Plug-Ins\Measurements`.
> **Note**
> If you are using a virtual environment, do not copy the `.venv` subdirectory&mdash;the virtual environment must be re-created in the new location.

Once your measurement service is statically registered, the NI Discovery Service makes it visible in supported NI applications.

### Create a batch file that runs a Python measurement

The batch file used for static registration is responsible for starting the Python Scripts.

Typical Batch File:

``` cmd
"<path_to_python_exe>" "<path_to_measurement_file>"
```

Examples to start the fictitious file named `foo_measurement.py`:

1. Using the Python system distribution

    ```cmd
    python foo_measurement.py
    ```

2. Using the virtual environment

    ```cmd
    REM Windows
    .\.venv\Scripts\python.exe foo_measurement.py

    REM Linux
    .venv/bin/python foo_measurement.py
    ```

### Create Executable for Python Scripts

To create an executable from a measurement, you can use the [pyinstaller](https://www.pyinstaller.org/) tooling. If you are using a Poetry project, add `pyinstaller` to its `dev-dependencies`. When statically registering the service, install the EXE into a unique directory along with its .serviceconfig and UI files.

Typical PyInstaller command to build executable:

```cmd
pyinstaller --onefile --console --paths .venv\Lib\site-packages measurement.py
```

## Troubleshooting

### "File not found" or "No such file or directory" errors when copying or running a measurement service

If copying or running a measurement service produces "File not found" or "No such file or directory" errors, make sure to [enable Win32 long paths](#enable-win32-long-paths). If you are unable to enable Win32 long paths, consider deploying the measurement service to a directory with a shorter path.

## Appendix: Managing Measurement with Python

A measurement and its related files can be maintained in different ways in Python. The basic components of any Python measurement are:

1. Measurement Python module (`.py` file)
    - This file contains all the details related to the measurement and also contains the logic for the measurement execution.
    - This file is run to start the measurement as a service.

2. UI File
    - UI file for the measurement. Types of supported UI files are:
        - Measurement UI (`.measui`): created using the **Measurement Plug-In UI Editor** application.
        - LabVIEW UI (`.vi`)
    - The path of this file is configured by `ui_file_path` in `measurement_info` variable definition in measurement Python module (`.py`).

Python communities have different ways of managing Python projects and their dependencies. It is up to the measurement developer to decide how to maintain the project and dependencies. Measurement developers can choose from a few common approaches discussed below based on their requirements.

### Create and Manage Python Measurement using Poetry

1. Install `poetry` (one-time setup)

    1. Make sure the system has the recommended Python version installed.

    2. Install `poetry` using the installation steps given in <https://python-poetry.org/docs/#installation>.

2. Create a new Python project and add `ni-measurement-plugin-sdk` as a dependency to the project.

    1. Open a command prompt, and change the working directory to the directory of your choice where you want to create the project.

        ``` cmd
        cd <path_of_directory_of_your_choice>
        ```

    2. Create a Poetry project using the `poetry new` command. Poetry will create boilerplate files and folders that are commonly needed for a Python project.

        ``` cmd
        poetry new <name_of_the_project>
        ```

    3. Add the `ni-measurement-plugin-sdk` package as a dependency using the [`poetry add`](https://python-poetry.org/docs/cli/#add) command.

        ``` cmd
        cd <name_of_the_project>
        poetry add ni-measurement-plugin-sdk
        ```

    4. The virtual environment will be auto-created by poetry.

    5. Create measurement modules as described in ["Developing a minimal Python measurement"](#developing-a-minimal-python-measurement)
        - Any additional dependencies required by measurement can be added using [add command](https://python-poetry.org/docs/cli/#add).

            ``` cmd
            poetry add <dependency_package_name>
            ```

For detailed info on managing projects using poetry [refer to the official documentation](https://python-poetry.org/docs/cli/).

### Create and Manage Python Measurement using `venv`

1. Make sure the system has the recommended Python version installed.

2. Open a command prompt, and change the working directory to the directory of your choice where you want to create a project.

    ``` cmd
    cd <path_of_directory_of_your_choice>
    ```

3. Create a virtual environment.

    ``` cmd
    REM This creates a virtual environment named .venv
    python -m venv .venv
    ```

4. Activate the virtual environment. After successful activation

    ``` cmd
    .venv\scripts\activate
    REM Optionally upgrade the pip within the venv by executing the command
    python -m pip install -U pip
    ```

5. Install the `ni-measurement-plugin-sdk` package into the virtual environment.

    ``` cmd
    pip install ni-measurement-plugin-sdk
    ```

6. Create measurement modules as described in ["Developing a minimal Python measurement"](#developing-a-minimal-python-measurement)
    - Any additional dependencies required by measurement can be added pip install.

        ``` cmd
        pip install <dependency_package_name>
        ```

For detailed info on managing projects with a virtual environment, refer to the [official documentation](https://docs.python.org/3/tutorial/venv.html).

### Create and Manage Python Measurement by directly installing `ni-measurement-plugin-sdk` as a system-level package

Measurement developers can also install `ni-measurement-plugin-sdk` as a system package if necessary.

1. Install the `ni-measurement-plugin-sdk` package from the command prompt

    ``` cmd
    pip install ni-measurement-plugin-sdk
    ```

2. Create measurement modules as described in ["Developing a minimal Python measurement"](#developing-a-minimal-python-measurement)

---
