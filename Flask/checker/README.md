# Execution of the service

You are REQUIRED to provide in the python script data such as telegram codes, emails from which to sends alerts, and so on, or else these functionalities will not work 

To run the app, use the following command in the CLI in the folder of this readme -> `waitress-serve --port 4080 --call flask_app:create_app`

To install the python packages you will need Pip. In this README it is assumed such an utility can be accessed with `pip`

In order to run the app, you'll need both Flask and Waitress: `pip install flask waitress`

You might change the port to something else if you want, it doesn't matter as long as you don't pick something else in use

The application assumes that a MySQL server is listening on localhost:3344; if that is not the case, change the db_configuration json.

If you intend to use the port 3306, remember that the Snap4City database is also using the same port; if you do not want to use the same server it is advised to have the MySQL server for Snap4Sentinel be accessible someplace else

They all say Success or Failure

For Kafka you will need to install a package -> `apt-get install kafkacat`; you might need admin privileges to install it

To generate the pdf you'll need to install the ReportLab package: `pip install reportlab`

To send a telegram message, you need to install the Telegram package: `pip install telegram`

To schedule the background healthchecks, you need to install the Apscheduler package: `pip install apscheduler`

To connect to the MySQL database, you need to install the mysql-connector-python package: `pip install mysql-connector-python`

To create the archive for certification, you'll need to install the zip package: `apt-get install zip`; you might need admin privileges to install it

If this doesn't run be sure to update Python (3.9 minimum), Flask and for python (use apt-get and pip)

# Using the service

The service opens the 4080 port (or whichever you picked if you used another port) and you can reach it by going to [http://localhost:4080/](http://localhost:4080/). You are free to proxy the service behind whatever you like.

The user interface mainly consists of multiple labels which are a summary of a category of multiple containers/processes. Next to each category, a summary status is shown. Clicking the label will open, an subsequentially close, the category into a more detailed control panel. For each container, you may see the current status and resources, you may see the logs of the container and restart/ping the port.
Below the containers, you will see advanced tests which can determine if the platform is working as intended. Below these tests, there's a log window which outputs the current results, and below that, if applicable, more resources are shown.

The navbar offers 3 functions, besides giving information; you may produce a detailed log of the platform as a pdf, you might temporarely stop/restart the periodic update of the status and you might ask for an immediate update

Logs are the sum of the standard out and the standard error; errors are shown in red.

Then you will see the list of the containers running on the machine; the list is taken in real time and lists all containers running, even those which have nothing to do with Snap4City; these not belonging to the native platform are listed in the unknown category

Of course if no functionality is set for a given container, then the button will not work even if not present

You might click a container ID (third column) to see the logs of the chosen container; it will open a new tab in the browser

The last columns of the table are the button for restarting the container, the button for checking if a container is alive/healthy and the latter shows the result of the previous operation (if any)

Some operations require additional data; said data can be inserted in the input fields below the button.

The results of the operations are shown on the second column; it follows the same format of the logs.

# Editing, adding tests

There are 2 kind of tests: on a container (will appear next to the container) and a complex tests

The first kind is supposed to be a ping, in order to see if a given container is alive/healthy

The second kind can be generic bash code

To write a test, go add an entry in the database; to `tests_table` for a container test or add an entry to `complex_tests` for the other kind

For the first table, the first column is the index and you can leave it blank

The second column holds the name of the container and that is the method used to send a certain command; a container can be forced to have a given name by telling it which is it in the docker-compose or the console command; if you are using the latest version (2023/10/30) all the containers are already forced to have a certain name

The third column is the command ran in the console; note that the console depends on the machine on which you run this tool, it could be Windows, \*nix or whatever. Write commands accordingly

For the second table, the first column is once again an index

The second column is the name of the command; such name will appear on the button of the user interface. The name is unique and the database enforces this

The third column is the command ran; the above disclaimer on the platform still applies

The fourth column is an optional declaration of special parameters; as a test might require data to be asked by the user, an interface must be provided. the structure is `data_type_html:name_shown_to_the_user:letter_used_as_console_parameter`

You might require more than one extra parameter; you may put several of these strings separated by a semicolon `;`, no spaces. use only one letter in the third block

The fifth column is the colour of the button in the interface and exists only for UI reasons; it defaults to white

The sixth column provides an additional explanation should one be needed

A seventh column is generated (and thus doesn't exist in the table) as a high contrast colour compared to the colour of the button. The generation of the colour depends on a function inside the database
