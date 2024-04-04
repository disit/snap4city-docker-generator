# Execution of the service
To run the app, use the following command in the CLI in the folder of this readme -> `waitress-serve --port 4080 --call flask_app:create_app`

You might change the port to something else if you want, it doesn't matter as long as you don't pick something else in use

The current db on this machine is listening on 3344
you might also change it; but don't use the standard 3306; the snap4city database container already uses it and there will be a conflict

You need to change the port in the flask_app.py file, there is one single instance

They all say Success or Failure

For Kafka you will need to install a package -> `apt-get install kafkacat`; you might need admin privileges to install it

If this doesn't run be sure to update Python (3.9 minimum), Flask and mysql-connector-python for python (use apt-get and pip). You will also need reportlab (pip install reportlab).

You will also need docker (not sure which one is enough but 20.whatever wasn't good and 23 was) (again, use apt-get)

# Using the service

The service opens the 4080 port (or whichever you picked if you changed it earlier) and you can reach it by going to [http://localhost:4080/](http://localhost:4080/)

The top part shows a console which outputs logs (which you can drag around) and a checkbox allowing for automatic refreshes (once every 15 seconds).

Logs are the sum of the standard out and the standard error; errors are shown in red.

The timing of the updates isn't synchronised to toggling the checkbox so any change might take less than 15 seconds.

Then you will see the list of the containers running on the machine; the list is taken in real time and lists all containers running, even those which have nothing to do with Snap4City

Of course if no functionality is set for a given container, then the button will not work even if not present

You might click a container ID (third column) to see the logs of the chosen container; it will open a new tab in the browser

The log window doesn't update; if you need to see the newest logs, just refresh the webpage

The last columns of the table are the button for restarting the container, the button for checking if a container is alive/healthy and the latter shows the result of the previous operation (if any)

After this table, there is an addition table which shows a list of operations which are activated by clicking the relative button

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
