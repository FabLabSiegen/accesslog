# accesslog

## Summary
Access and Documentation System for the Fab Lab

The Project is based on Django.

## Requirements
## Installation

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
* GET `http://localhost:8000/api/slicingconfig/GCODEID`
    * returns slicing config of gcode in json format
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
### Print Jobs:
* GET `http://localhost:8000/api/printjob/`
    * returns all PrintJobs in a list owned by logged in User
* GET `http://localhost:8000/api/printjob/PRINTJOBID`
    * returns detailed information about a single PrintJob
* POST `http://localhost:8000/api/printjob/`
    * allows to add new PrintJobs providing: Machine, GCode, Start, End, State

### Print Media Files:
* GET `http://localhost:8000/api/mediafile/`
    * returns all mediafiles
* GET `http://localhost:8000/api/mediafile/MEDIAFILEID`
    * returns detailed information (including download link) about a single mediafile providing `MEDIAFILEID`
* GET `http://localhost:8000/api/mediafiles/PRINTJOBID`
    * returns all Media Files related to a PrintJob providing `PRINTJOBID`
* POST `http://localhost:8000/api/mediafile/`
    * allows to add new PrintMediaFiles providing: PrintJobID, File
    * Logged in User also needs to be owner of related Print Job

## Future improvement possibilities

* Multithreading
  * Multiple Instances of the paho mqtt client for each Machine