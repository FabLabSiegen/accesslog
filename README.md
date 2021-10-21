# accesslog
Access and Documentation System for the Fab Lab

The Project is based on Django.

## API Endpoints

### users: 
#### GET `http://localhost:8000/api/users/` 
returns all users
### groups: 
#### GET `http://localhost:8000/api/groups/` 
returns all groups
### models: 
#### GET `http://localhost:8000/api/models/` 
returns all models that are owned by the user or shared with the user
#### GET `http://localhost:8000/api/models/?id=MODELID`
returns single model with id provided the user is owner or the model is shared with the user
#### GET `http://localhost:8000/api/models/?name=MODELNAME`
returns all models with that name provided the user is owner or the model is shared with the user
#### GET `http://localhost:8000/api/models/MODELID/`
returns single model with all details
#### POST `http://localhost:8000/api/models/` 
allows adding of new models providing: File, _Previous (optional)_, _SharedWithUser (optional)_
### gcode: 
#### GET `http://localhost:8000/api/gcode/`
returns all gcodes that are owned by the user or shared with the user
#### GET `http://localhost:8000/api/gcode/?id=GCODEID`
returns single gcodes with id provided the user is owner or the model is shared with the user
#### GET `http://localhost:8000/api/gcode/?name=GCODENAME`
returns all gcodes with that name provided the user is owner or the model is shared with the user
#### GET `http://localhost:8000/api/gcode/MODELID/`
returns single model with all details
#### POST `http://localhost:8000/api/gcode/`
allows adding of new models providing: File, UsedFilamentInG, UsedFilamentInMm, _SharedWithUser (optional)_, EstimatedPrintingTime, _ThreeDimensionalModel (optional)_
### slicingconfig: 
#### GET `http://localhost:8000/api/slicingconfig/`
returns all sclicing configs in a list
#### GET `http://localhost:8000/api/slicingconfig/GCODEID`
returns slicing config of gcode in json format
#### POST `http://localhost:8000/api/slicingconfig/`
allows to add new slicing config in json format providing: Config, GCodeID
### printjob:
#### GET `http://localhost:8000/api/printjob/`
returns all PrintJobs in a list owned by logged in User
#### GET `http://localhost:8000/api/printjob/PRINTJOBID`
returns detailed information about a single PrintJob
#### POST `http://localhost:8000/api/printjob/`
allows to add new PrintJobs providing: Machine, GCode, Start, End, State

### Print Media Files:
#### GET `http://localhost:8000/api/mediafiles/`
returns all mediafiles
#### GET `http://localhost:8000/api/mediafiles/PRINTJOBID`
returns detailed information about a single mediafile
#### POST `http://localhost:8000/api/mediafiles/`
allows to add new PrintMediaFiles providing: PrintJobID, File