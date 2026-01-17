using Microsoft.AspNetCore.Mvc;

namespace TimeTableapi.Controllers
{
    [ApiController]
    [Route("api/rooms")]
    public class RoomsController : ControllerBase
    {
        private static List<RoomDto> Rooms = new();

        [HttpPost]
public IActionResult AddRoom(RoomDto room)
{
    // check duplicate room number
    var existingRoom = Rooms.FirstOrDefault(r =>
        r.RoomNumber.ToLower() == room.RoomNumber.ToLower()
    );

    if (existingRoom != null)
    {
        return BadRequest("Room with this room number already exists");
    }

    room.Id = Rooms.Count + 1;
    Rooms.Add(room);
    return Ok(room);
}


        [HttpGet]
        public IActionResult GetAllRooms()
        {
            return Ok(Rooms);
        }

        [HttpPost("{id}/reserve")]
        public IActionResult ReserveRoom(int id)
        {
            var room = Rooms.FirstOrDefault(r => r.Id == id);
            if (room == null) return NotFound();

            room.IsReserved = true;
            return Ok("Room reserved");
        }
    }

    public class RoomDto
    {
        public int Id { get; set; }
        public string RoomNumber { get; set; }
        public string Type { get; set; }
        public int Capacity { get; set; }
        public bool IsReserved { get; set; }
    }
}
