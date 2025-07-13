from fastapi import APIRouter, Depends, HTTPException

from models.request import InstructorCoursesRequest
from models.response import InstructorCoursesResponse

router = APIRouter()

@router.post("/instructor-courses", response_model = InstructorCoursesResponse)
def get_instructor_courses(data: InstructorCoursesRequest) -> InstructorCoursesResponse:

    """
    Returns the list of courses an instructor teaches
    Admins will see all courses.
    """

    # TODO: Replace with real database query
    all_courses = ['TEK102', 'SRF305', 'IHU224', 'LOH116', 'YDF451']
    instructor_courses = ['TEK102', 'IHU224', 'LOH116']

    # TODO: Extract role based on JWT passed in via middleware
    if data.role == 'admin':
        return InstructorCoursesResponse(instructor_courses=all_courses)
    else:
        return InstructorCoursesResponse(instructor_courses=instructor_courses)


