from fastapi import APIRouter, Body, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from .models import SubjectModel, UpdateSubjectModel, LocationModel, UpdateLocationModel

router = APIRouter()

#
# Location
#

@router.post("/locations", response_description="Add new location")
async def create_location(request: Request, location: LocationModel = Body(...)):
    location = jsonable_encoder(location)
    new_location = await request.app.mongodb["locations"].insert_one(location)
    created_location = await request.app.mongodb["locations"].find_one(
        {"_id": new_location.inserted_id}
    )

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_location)


@router.get("/locations", response_description="List all locations")
async def list_locations(request: Request):
    locations = []
    for doc in await request.app.mongodb["locations"].find().to_list(length=100):
        locations.append(doc)
    return locations


@router.get("/locations/{id}", response_description="Get a single location")
async def show_location(id: str, request: Request):
    if (location := await request.app.mongodb["locations"].find_one({"_id": id})) is not None:
        return location

    raise HTTPException(status_code=404, detail=f"location {id} not found")


@router.put("/locations/{id}", response_description="Update a location")
async def update_location(id: str, request: Request, location: UpdateLocationModel = Body(...)):
    location = {k: v for k, v in location.dict().items() if v is not None}

    if len(location) >= 1:
        update_result = await request.app.mongodb["locations"].update_one(
            {"_id": id}, {"$set": location}
        )

        if update_result.modified_count == 1:
            if (
                updated_location := await request.app.mongodb["locations"].find_one({"_id": id})
            ) is not None:
                return updated_location

    if (
        existing_location := await request.app.mongodb["locations"].find_one({"_id": id})
    ) is not None:
        return existing_location

    raise HTTPException(status_code=404, detail=f"Participant {id} not found")


@router.delete("/locations/{id}", response_description="Delete location")
async def delete_location(id: str, request: Request):
    delete_result = await request.app.mongodb["locations"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Participant {id} not found")

#
# Subject
#

@router.post("/subjects", response_description="Add new subject")
async def create_subject(request: Request, subject: SubjectModel = Body(...)):
    subject = jsonable_encoder(subject)
    new_subject = await request.app.mongodb["subjects"].insert_one(subject)
    created_subject = await request.app.mongodb["subjects"].find_one(
        {"_id": new_subject.inserted_id}
    )

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_subject)


@router.get("/subjects", response_description="List all subjects")
async def list_subjects(request: Request):
    subjects = []
    for doc in await request.app.mongodb["subjects"].find().to_list(length=100):
        subjects.append(doc)
    return subjects


@router.get("/subjects/{id}", response_description="Get a single subject")
async def show_subject(id: str, request: Request):
    if (subject := await request.app.mongodb["subjects"].find_one({"_id": id})) is not None:
        return subject

    raise HTTPException(status_code=404, detail=f"subject {id} not found")


@router.put("/subjects/{id}", response_description="Update a subject")
async def update_subject(id: str, request: Request, subject: UpdateSubjectModel = Body(...)):
    subject = {k: v for k, v in subject.dict().items() if v is not None}

    if len(subject) >= 1:
        update_result = await request.app.mongodb["subjects"].update_one(
            {"_id": id}, {"$set": subject}
        )

        if update_result.modified_count == 1:
            if (
                updated_subject := await request.app.mongodb["subjects"].find_one({"_id": id})
            ) is not None:
                return updated_subject

    if (
        existing_subject := await request.app.mongodb["subjects"].find_one({"_id": id})
    ) is not None:
        return existing_subject

    raise HTTPException(status_code=404, detail=f"Participant {id} not found")


@router.delete("/subjects/{id}", response_description="Delete subject")
async def delete_subject(id: str, request: Request):
    delete_result = await request.app.mongodb["subjects"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Participant {id} not found")


