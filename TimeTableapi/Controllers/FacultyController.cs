using Microsoft.AspNetCore.Mvc;

namespace TimeTableapi.Controllers;

[ApiController]
[Route("api/faculty")]
public class FacultyController : ControllerBase
{
    // In-memory storage
    private static List<Faculty> Faculties = new();

    // ADD A TEACHER
    [HttpPost]
    public IActionResult AddFaculty(Faculty faculty)
    {
        faculty.Id = Faculties.Count + 1;
        Faculties.Add(faculty);
        return Ok(faculty);
    }

    // GET ALL TEACHERS
    [HttpGet]
    public IActionResult GetAllFaculty()
    {
        return Ok(Faculties);
    }
}

// Faculty model (memory-based)
public class Faculty
{
    public int Id { get; set; }
    public string Name { get; set; }
    public string Subjects { get; set; } // DSA,OS,DBMS
    public int MaxLecturesPerDay { get; set; }
    public int MaxLecturesPerWeek { get; set; }
    public string AvailableShift { get; set; } // Morning / Evening / Both
}
