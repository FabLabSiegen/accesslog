# accesslog
Access and Documentation System for the Fab Lab that logs temperature data of ongoing prints and makes data available through an API and give the possibility to control prints

* Manage existing Printers under http://localhost:8000/manage/ _(is_staff required)_
* Register a new Account http://localhost:8000/register/ and Login to create a session http://localhost:8000/login/
* Access the [REST API](#api-endpoints) in order to ...
  * start/stop prints
  * get data from the system
  * post data to the system
* PrintJobs will be created internally in order to log temperature data of prints

The Project is based on Django.
## Table of contents
* [Local development](#local-development)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [API Endpoints](#api-endpoints)
  * [Start Print Jobs](#start-print-jobs)
  * [Stop/Cancel Print Jobs](#stopcancel-print-jobs)
  * [Users](#users)
  * [Groups](#groups)
  * [Models](#models)
  * [GCode](#gcode)
  * [Slicing Configs](#slicing-configs)
  * [Print Jobs](#print-jobs)
  * [Print Media Files](#print-media-files)
* [Future improvement possibilities](#future-improvement-possibilities)

## Local development

### Prerequisites
1. Latest Version of [Docker](https://www.docker.com/) and a Docker Account
2. Check Python Version
```sh
$ python --version
```
3. If you don't have Python installed, install Python 3.9.0 or higher
### Installation
1. Run the Docker Compose file `docker-compose run --build`
2. Go to http://localhost:5000/ and follow the basic setup wizard and create an account
3. Create a terminal in your 'web'-container and run the following commands:

```sh
$ python manage.py makemigrations
```
```sh
$ python manage.py migrate
```
This will make sure the database has all the models to work with
4. Go to http://localhost:5000/ and under `Settings > OCTOPRINT > Pluginmanager` install the MQTT Plugin _(by Gina Häußge)_
5. Go to http://localhost:8000/register/ and create an Account
6. Run Docker Compose again `docker-compose run --build`

The Api (http://localhost:8000/api/) should now be available to you. In order to access the "Manage Printers"-tab (http://localhost:8000/manage/) you need to access the database directly and change your just created User to is_staff=true and is_superuser=true

## API Endpoints

### Start Print Jobs:
* POST `http://localhost:8000/api/print/`
  * allows to start a new Print Job providing: GCode ID, Machine ID
  * Returns on successful request: `HTTP 201 Create`

Example successful response:
```
{
    "done": false,
    "files": {
        "local": {
            "name": "boat_1HhpkoU.gcode",
            "origin": "local",
            "path": "boat_1HhpkoU.gcode",
            "refs": {
                "download": "http://octoprint:5000/downloads/files/local/boat_1HhpkoU.gcode",
                "resource": "http://octoprint:5000/api/files/local/boat_1HhpkoU.gcode"
            }
        },
        "sdcard": {
            "name": "boat_1~1.gco",
            "origin": "sdcard",
            "path": "boat_1~1.gco",
            "refs": {
                "resource": "http://octoprint:5000/api/files/sdcard/boat_1~1.gco"
            }
        }
    }
}
```
### Stop/Cancel Print Jobs:
* POST `http://localhost:8000/api/stopprint/`
  * allows to stop an ongoing Print Job providing: PrintJob ID
  * Permissions: Owner of Print Job
  * Returns on successful request: `HTTP 204 No Content`

Example successful response:
```
[]
```

### Users: 
* GET `http://localhost:8000/api/users/` 
    * returns all users
    * Returns on successful request: `HTTP 200 Ok`

Example successful response:
```
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "url": "http://localhost:8000/api/users/1/",
            "username": "superuser",
            "email": "",
            "groups": []
        }
    ]
}
```
### Groups: 
* GET `http://localhost:8000/api/groups/` 
    * returns all groups
    * Returns on successful request: `HTTP 200 Ok`

Example successful response:
```
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "url": "http://localhost:8000/api/groups/1/",
            "name": "Testgroup"
        }
    ]
}
```
### Models: 
* GET `http://localhost:8000/api/models/` 
    * returns all models that are owned by the user or shared with the user
    * Returns on successful request: `HTTP 200 Ok`

Example successful response _(Logged in UserID:1)_:
```
[
    {
        "id": 1,
        "Name": "ghost",
        "FileName": "ghost.stl",
        "Size": "3501284",
        "File": "/upload/models/ghost_92lAXd9.stl",
        "Uploaded": "2021-10-19T10:57:44.211590+02:00",
        "Owner": 1,
        "Previous": null,
        "SharedWithUser": null
    },
    {
        "id": 2,
        "Name": "ghost",
        "FileName": "ghost.stl",
        "Size": "3501284",
        "File": "/upload/models/ghost_lsaRxE9.stl",
        "Uploaded": "2021-10-19T10:58:13.225555+02:00",
        "Owner": 1,
        "Previous": null,
        "SharedWithUser": 2
    }
]
```
* GET `http://localhost:8000/api/models/?id=MODELID`
    * returns single model with id provided the user is owner or the model is shared with the user
    * Returns on successful request: `HTTP 200 Ok`

Example successful response _(?id=1, Logged in UserID:1)_:
```
{
    "id": 1,
    "Name": "ghost",
    "FileName": "ghost.stl",
    "Size": "3501284",
    "File": "/upload/models/ghost_92lAXd9.stl",
    "Uploaded": "2021-10-19T10:57:44.211590+02:00",
    "Owner": 1,
    "Previous": null,
    "SharedWithUser": null
}
```
* GET `http://localhost:8000/api/models/?name=MODELNAME`
    * returns all models with that name provided the user is owner or the model is shared with the user
    * Returns on successful request: `HTTP 200 Ok`

Example successful response _(?name=ghost, Logged in UserID:1)_:
```
[
    {
        "id": 1,
        "Name": "ghost",
        "FileName": "ghost.stl",
        "Size": "3501284",
        "File": "/upload/models/ghost_92lAXd9.stl",
        "Uploaded": "2021-10-19T10:57:44.211590+02:00",
        "Owner": 1,
        "Previous": null,
        "SharedWithUser": null
    },
    {
        "id": 2,
        "Name": "ghost",
        "FileName": "ghost.stl",
        "Size": "3501284",
        "File": "/upload/models/ghost_lsaRxE9.stl",
        "Uploaded": "2021-10-19T10:58:13.225555+02:00",
        "Owner": 1,
        "Previous": null,
        "SharedWithUser": 2
    }
]
```
* GET `http://localhost:8000/api/models/MODELID/`
    * returns single model with all details
    * Returns on successful request: `HTTP 200 Ok`

Example successful response _(MODELID=1)_:
```
{
    "id": 1,
    "Name": "ghost",
    "FileName": "ghost.stl",
    "Size": "3501284",
    "File": "http://localhost:8000/upload/models/ghost_92lAXd9.stl",
    "Uploaded": "2021-10-19T10:57:44.211590+02:00",
    "Owner": 1,
    "Previous": null,
    "SharedWithUser": null
}
```
* POST `http://localhost:8000/api/models/` 
    * allows adding of new models providing: File, _Previous (optional)_, _SharedWithUser (optional)_
    * Returns on successful request: `HTTP 201 Created`

Example successful response _(Logged in UserID:1)_:
```
{
    "id": 7,
    "Name": "ghost",
    "FileName": "ghost.stl",
    "Size": "3501284",
    "File": "/upload/models/ghost.stl",
    "Uploaded": "2021-11-16T12:13:06.155228+01:00",
    "Owner": 1,
    "Previous": 4,
    "SharedWithUser": 2
}
```
### GCode: 
* GET `http://localhost:8000/api/gcode/`
    * returns all gcodes that are owned by the user or shared with the user
    * Returns on successful request: `HTTP 200 OK`

Example successful response _(Logged in UserID:1)_:
```
[
    {
        "id": 8,
        "Name": "boat",
        "FileName": "boat.gcode",
        "Size": "562833",
        "File": "/upload/gcode/boat_pWiZ5oi.gcode",
        "Uploaded": "2021-11-15T12:21:47.197334+01:00",
        "UsedFilamentInG": 0.0,
        "Owner": 1,
        "UsedFilamentInMm": 0.0,
        "SharedWithUser": null,
        "EstimatedPrintingTime": "11:21:47.187739",
        "ThreeDimensionalModel": null
    },
    {
        "id": 9,
        "Name": "boat",
        "FileName": "boat.gcode",
        "Size": "562833",
        "File": "/upload/gcode/boat_1HhpkoU.gcode",
        "Uploaded": "2021-11-15T12:26:48.249209+01:00",
        "UsedFilamentInG": 123.0,
        "Owner": 1,
        "UsedFilamentInMm": 2132.0,
        "SharedWithUser": 3,
        "EstimatedPrintingTime": "12:30:00",
        "ThreeDimensionalModel": 1
    }
]
```

* GET `http://localhost:8000/api/gcode/?id=GCODEID`
    * returns single gcodes with id provided the user is owner or the model is shared with the user
    * Returns on successful request: `HTTP 200 OK`

Example successful response _(?id=1, Logged in UserID:1)_:
```
{
    "id": 8,
    "Name": "boat",
    "FileName": "boat.gcode",
    "Size": "562833",
    "File": "/upload/gcode/boat_pWiZ5oi.gcode",
    "Uploaded": "2021-11-15T12:21:47.197334+01:00",
    "UsedFilamentInG": 0.0,
    "Owner": 1,
    "UsedFilamentInMm": 0.0,
    "SharedWithUser": null,
    "EstimatedPrintingTime": "11:21:47.187739",
    "ThreeDimensionalModel": null
}
```
* GET `http://localhost:8000/api/gcode/?name=GCODENAME`
    * returns all gcodes with that name provided the user is owner or the model is shared with the user
    * Returns on successful request: `HTTP 200 OK`

Example successful response _(?name=boat, Logged in UserID:1)_:
```
[
    {
        "id": 8,
        "Name": "boat",
        "FileName": "boat.gcode",
        "Size": "562833",
        "File": "/upload/gcode/boat_pWiZ5oi.gcode",
        "Uploaded": "2021-11-15T12:21:47.197334+01:00",
        "UsedFilamentInG": 0.0,
        "Owner": 1,
        "UsedFilamentInMm": 0.0,
        "SharedWithUser": null,
        "EstimatedPrintingTime": "11:21:47.187739",
        "ThreeDimensionalModel": null
    },
    {
        "id": 9,
        "Name": "boat",
        "FileName": "boat.gcode",
        "Size": "562833",
        "File": "/upload/gcode/boat_1HhpkoU.gcode",
        "Uploaded": "2021-11-15T12:26:48.249209+01:00",
        "UsedFilamentInG": 123.0,
        "Owner": 1,
        "UsedFilamentInMm": 2132.0,
        "SharedWithUser": 3,
        "EstimatedPrintingTime": "12:30:00",
        "ThreeDimensionalModel": 1
    }
]
```
* GET `http://localhost:8000/api/gcode/MODELID/`
    * returns single model with all details
    * Returns on successful request: `HTTP 200 OK`

Example successful response _(MODELID=8)_:
```
{
    "id": 8,
    "Name": "boat",
    "FileName": "boat.gcode",
    "Size": "562833",
    "File": "http://localhost:8000/upload/gcode/boat_pWiZ5oi.gcode",
    "Uploaded": "2021-11-15T12:21:47.197334+01:00",
    "UsedFilamentInG": 0.0,
    "Owner": 1,
    "UsedFilamentInMm": 0.0,
    "SharedWithUser": null,
    "EstimatedPrintingTime": "11:21:47.187739",
    "ThreeDimensionalModel": null
}
```

* POST `http://localhost:8000/api/gcode/`
    * allows adding of new models providing: File, UsedFilamentInG, UsedFilamentInMm, _SharedWithUser (optional)_, EstimatedPrintingTime, _ThreeDimensionalModel (optional)_
    * Returns on successful request: `HTTP 201 Created`

Example successful response _(Logged in UserID:1)_:
```
{
    "id": 10,
    "Name": "boat",
    "FileName": "boat.gcode",
    "Size": "562833",
    "File": "/upload/gcode/boat_H4zM6xZ.gcode",
    "Uploaded": "2021-11-16T13:43:18.135579+01:00",
    "UsedFilamentInG": 123.0,
    "Owner": 1,
    "UsedFilamentInMm": 12323.0,
    "SharedWithUser": 3,
    "EstimatedPrintingTime": "12:33:00",
    "ThreeDimensionalModel": 3
}
```

### Slicing Configs: 
* GET `http://localhost:8000/api/slicingconfig/`
    * returns all sclicing configs in a list
    * Configs in JSON format
    * Returns on successful request: `HTTP 200 OK`

Example successful response:
```
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "Config": [
                {
                    "dummy0": "1-770-736-8031 x56442",
                    "dummy1": 1,
                    "dummy2": "Leanne Graham",
                    "dummy3": "Bret",
                    "dummy4": "Sincere@april.biz"
                }
            ],
            "GCode": 10
        },
        {
            "Config": [
                {
                    "dummy0": "1-770-736-8031 x56442",
                    "dummy1": 1,
                    "dummy2": "Leanne Graham",
                    "dummy3": "Bret",
                    "dummy4": "Sincere@april.biz"
                }
            ],
            "GCode": 9
        }
    ]
}
```
* GET `http://localhost:8000/api/slicingconfig/GCODEID/`
    * returns slicing config of gcode in json format providing `GCODEID`
    * Returns on successful request: `HTTP 200 OK`

Example successful response:
```
[
    {
        "dummy0": "1-770-736-8031 x56442",
        "dummy1": 1,
        "dummy2": "Leanne Graham",
        "dummy3": "Bret",
        "dummy4": "Sincere@april.biz"
    }
]
```
* POST `http://localhost:8000/api/slicingconfig/`
    * allows to add new slicing config in json format providing: Config, GCodeID
    * Returns on successful request: `HTTP 201 Created`

Example successful response (returns saved JSON Config):
```
[
    {
        "dummy0": "1-770-736-8031 x56442",
        "dummy1": 1,
        "dummy2": "Leanne Graham",
        "dummy3": "Bret",
        "dummy4": "Sincere@april.biz"
    }
]
```
### Print Jobs:
* GET `http://localhost:8000/api/printjob/`
    * returns all PrintJobs in a list owned by logged in User
    * Returns on successful request: `HTTP 200 OK`

Example successful response _(Logged in UserID:1)_:
```
[
    {
        "id": 1478,
        "User": 1,
        "Machine": 17,
        "GCode": 9,
        "Start": "2021-11-15T17:12:42.932473+01:00",
        "End": "2021-11-15T17:17:37.710299+01:00",
        "State": 0
    },
    {
        "id": 1479,
        "User": 1,
        "Machine": 17,
        "GCode": 9,
        "Start": "2021-11-15T17:19:38.623075+01:00",
        "End": "2021-11-15T17:24:33.783123+01:00",
        "State": 0
    }
]
```
* GET `http://localhost:8000/api/printjob/PRINTJOBID`
    * returns detailed information about a single PrintJob
    * Returns on successful request: `HTTP 200 OK`

Example successful response _(PRINTJOBID:1476)_:
```
{
    "id": 1476,
    "User": 1,
    "Machine": 17,
    "GCode": 9,
    "Start": "2021-11-15T16:04:04.274812+01:00",
    "End": "2021-11-15T16:04:04.274820+01:00",
    "State": 0
}
```
* POST `http://localhost:8000/api/printjob/`
    * allows to add new PrintJobs providing: Machine, GCode, Start, End, State
    * Returns on successful request: `HTTP 201 Created`
  

Example successful response _(Logged in UserID:1)_:
```
{
    "id": 1494,
    "User": 1,
    "Machine": 12,
    "GCode": 10,
    "Start": "2021-11-17T10:51:00+01:00",
    "End": "2021-11-17T10:53:00+01:00",
    "State": 0
}
```

### Print Media Files:
* GET `http://localhost:8000/api/mediafile/`
    * returns all mediafiles
    * Returns on successful request: `HTTP 200 OK`


Example successful response:
```
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 5,
            "PrintJob": 1478,
            "File": "http://localhost:8000/upload/printmedia/New_York_City_High-Quality_Wallpaper_Pack.jpg",
            "Owner": 1
        }
    ]
}
```
* GET `http://localhost:8000/api/mediafile/MEDIAFILEID`
    * returns detailed information (including download link) about a single Media File providing `MEDIAFILEID`
    * Returns on successful request: `HTTP 200 OK`


Example successful response:
```
{
    "id": 5,
    "PrintJob": 1478,
    "File": "http://localhost:8000/upload/printmedia/New_York_City_High-Quality_Wallpaper_Pack.jpg",
    "Owner": 1
}
```
* GET `http://localhost:8000/api/mediafiles/PRINTJOBID`
    * returns all Media Files related to a PrintJob providing `PRINTJOBID`
    * Returns on successful request: `HTTP 200 OK`


Example successful response:
```
[
    {
        "id": 5,
        "PrintJob": 1478,
        "File": "/upload/printmedia/New_York_City_High-Quality_Wallpaper_Pack.jpg",
        "Owner": 1
    }
]
```
* POST `http://localhost:8000/api/mediafile/`
    * allows to add new PrintMediaFiles providing: PrintJobID, File
    * Logged in User also needs to be owner of related Print Job
    * Returns on successful request: `HTTP 201 Created`


Example successful response _(Logged in UserID:1)_:
```
{
    "id": 5,
    "PrintJob": 1478,
    "File": "http://localhost:8000/upload/printmedia/New_York_City_High-Quality_Wallpaper_Pack.jpg",
    "Owner": 1
}
```

## Future improvement possibilities

* Multithreading
  * Multiple Instances of the paho mqtt client for each Machine
  
* Improvement to the Front-End
  * Mobile responsive
  * Increase User Experience (UX)
  * Language localisation
  * Increase overall visibility