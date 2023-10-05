# Docker support

## Introduction

This software can be deployed as a group of containers using docker.

The [docker-compose.yaml](docker-compose.yaml) file provided in this folder contains everything needed to run the containers.

## Containers description

The full deployment is composed by 4 containers:

-   `edit-settings`: on this container there are mounted all the settings folder, it should be used to prepare the settings for both onedrive and the Polito Material Download app before they start (please follow the instructions in the log).

    It comes with nano installed as text editor.

    This container terminates either when the `remove_me` file is deleted or after 10 mins.

	The last two containers are started only after this one has completed succesfully, that is that you removed the `remove_me` file.
	Otherwhise, the other containers will not run.

-   `onedrive-print-link`: this container is supposed to start together with the first one, and then immediately crash.

    It is a normal onedrive container, but due to this induced crash it will never sync anything: its purpose is just to print the login link, so that you can use it to get the auth login and paste it into the respective file via the first container.

    In case the whole compose is being recreated, the link will be printed also in case the login was already done, in that case simply ignore it.

-   `onedrive`: this is the final onedrive container, the one that will sync the files to the cloud.

    In case you need to update the onedrive settings, you have to restart it to reload the settings

-   `polito-material-downloader`: this is the container that will download your files.

    It can run either once (if no env variables are passed), or on a cron: in this case you have to pass it an env variable in the format `cronSettings=[cron schedule]`. For example, I use `cronSettings=0 7-21 * * *` as already inserted in the docker-compose.

## First build

What to do when the deployment is done for the first time:

-   Open the link printed by `onedrive-print-link`, paste it into a browser and follow the login process.
-   At the end of the process, you will be redirected to a blank page: copy its full link.
-   Connect via shell to the `edit-settings` container.
-   Enter the `onedrive_settings` folder.
-   Paste the link you previously copied as the sole content of the file `login_link`.
-   Move or copy `default-config` to `config`, and edit it to your will to customize your onedrive (please do not modify the `sync_dir` option, as this is already set to the path where the `onedrive` container will find all the files).
-   Return to the parent folder, and enter the folder `polito_material_download_settings`.
-   Move or copy `sample-settings.yaml` into `settings.yaml` and edit it to your will to customize your polito material download.

    Please do not modify `mainFolderPath` (and if you use `moveDest`, set it as a subdirectory of `mainFolderPath`), otherwhise your files would not be synced by onedrive.

	Also, please do not change `gui` and `waitBeforeQuitting`, as that would generate errors (there is no gui available, and the container logs cannot receive any input).

-   Return to the parent folder, and remove the file `remove_me`, and your installation should be done.

Note: the _move or copy the files_ mechanic is inserted because the default files are recreated every time, so that in case you delete them by mistake they will reappear the next time you launch `edit-settings`.

For this reason, I could not save them with their final file name, as your settings would be overwritten every time.

## Change Polito Material Download settings

If you do not need a new `sample-settings.json`, you can just attach a shell to the `polito-material-download` container and edit the file, at the next cron iteration the new settings will be taken.

Instead, if you need a new `sample-settings.json`, or your `polito-material-download` is not running on a cron, you will have to restart the container `edit-settings`, edit the settings file there, and then save it.

## Update Polito Material Download

Unfortunately, there is currently no way neither to update the app automatically, nor to update the app by changing only the container itself: the only way that I could think about is to recreate the whole docker-compose (if you have suggestions, please open an issue).

In this case, if the docker volumes are not recreated, your settings and files should still be there. The `onedrive-print-link` container will print the link anyway, simply ignore it.

If instead the volumes are erased, you will unfortunately have to redo all the settings: for this eventuality, I suggest you to have a local copy of the settings files, so that if you have to redo them, you can yust copy-and-paste them.

## Change OneDrive settings

If you do not need a new `default-config`, you can just attach a shell to the `onedrive` container to edit the file.

Instead, if you need a new `default-config`, you will have to restart the container `edit-settings`, edit the settings file there, and then save it.

In both cases, you will have to restart the `onenote` container, in order for it to load the new settings.

If the docker volumes are not recreated, your OneDrive should restart immediately, without requiring you to insert the login link again. The `onedrive-print-link` container, if restarted, will print the link anyway: just ignore it.
