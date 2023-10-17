Configuration
=============

Configuration via Environment Variables
---------------------------------------

The application can be configured through several environment variables. Below
is a description of some key variables and their usage:

1. ``PROMPTLY_MAINTENANCE_MODE``
    This variable is used to toggle maintenance mode for the application. When
    maintenance mode is active, the application will respond with a "503 Service
    Unavailable" status for every request. To activate maintenance mode, set the
    variable to a truthy value (e.g., "True" or "1"). The variable can be unset
    or set to a falsy value (e.g., "False" or "0") to deactivate maintenance
    mode.

    Example usage:

    .. code-block:: shell

        $ export PROMPTLY_MAINTENANCE_MODE=True
        $ flask --app runner:app run

2. ``PROMPTLY_SETTINGS``
    This variable points to a configuration file that can hold additional
    configuration settings for the application. The configuration file should be
    a Python file, and only variables defined in uppercase will be read and
    applied.

    Example usage:

    .. code-block:: shell

        $ export PROMPTLY_SETTINGS="/path/to/settings.cfg"
        $ flask --app runner:app run

3. ``PROMPTLY_CONFIG``
    This variable defines the startup mode of the application. Valid values
    include "development", "testing", "production", and "default" (which is an
    alias for "development"). This variable influences how the application is
    initialized, but it is separate from the ``--debug`` flag used with the
    Flask script.

    Example usage:

    .. code-block:: shell

        $ export PROMPTLY_CONFIG=production
        $ flask --app runner:app run

4. ``PROMPTLY_THREAD_TIMEOUT``
    This variable defines the maximum amount of time, in seconds, that the
    :func:`~promptly.utils.threaded_execute` function will wait for the
    completion of the function it is executing in a separate thread. If the
    function does not complete within this time, a TimeoutError will be thrown,
    logged, and the function will be invoked again with the same arguments.

    The default value is 60 seconds, but you can adjust this according to the
    specific requirements of your environment by setting a different value for
    ``PROMPTLY_THREAD_TIMEOUT`` in this configuration file. This timeout setting
    helps in ensuring that the function does not hang indefinitely and consumes
    resources, while providing a mechanism to handle scenarios where the
    function takes longer than expected to execute.

    It's essential to set a reasonable timeout value to balance between giving
    the function enough time to complete its execution and preventing resource
    exhaustion in case of functions that might hang or take an excessive amount
    of time to finish.

    Example usage:

    .. code-block:: shell

        $ export PROMPTLY_THREAD_TIMEOUT=120  # Sets the timeout to 120 seconds.
        $ flask --app runner:app run

These environment variables provide a flexible way to configure the
application's behavior without changing the code. They can be set in the shell
before starting the server or provided through other means depending on the
deployment environment.
