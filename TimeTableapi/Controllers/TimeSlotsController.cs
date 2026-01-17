using Microsoft.AspNetCore.Mvc;

namespace TimeTableapi.Controllers;

[ApiController]
[Route("api/timeslots")]
public class TimeSlotsController : ControllerBase
{
    // In-memory rule storage
    private static TimeRule? Rule;

    // ADD / UPDATE TIME RULES
    [HttpPost]
    public IActionResult SetTimeRules(TimeRule rule)
    {
        Rule = rule;
        return Ok(rule);
    }

    // GET CURRENT TIME RULES
    [HttpGet]
    public IActionResult GetTimeRules()
    {
        if (Rule == null)
            return NotFound("Time rules not set yet");

        return Ok(Rule);
    }
}

// RULE MODEL (AI-READY)
public class TimeRule
{
    public string ShiftName { get; set; }        // Morning / Evening
    public string ShiftStart { get; set; }       // 08:00
    public string ShiftEnd { get; set; }         // 16:00

    public string LunchBreakStart { get; set; }  // 13:00
    public string LunchBreakEnd { get; set; }    // 14:00

    public int LectureDurationHours { get; set; } // 1
    public int LabDurationHours { get; set; }     // 2
}
