using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;

namespace JSPromises.Controllers
{
    [ApiController]
    [Route("decorations")]
    public class WeatherForecastController : ControllerBase
    {
        private static readonly string[] Summaries = new[]
        {
            "Freezing", "Bracing", "Chilly", "Cool", "Mild", "Warm", "Balmy", "Hot", "Sweltering", "Scorching"
        };

        private readonly ILogger<WeatherForecastController> _logger;

        public WeatherForecastController(ILogger<WeatherForecastController> logger)
        {
            _logger = logger;
        }

        [HttpGet("bgcolor/{choice}")]
        public string GetBGColor(string choice)
        {
            Task.Delay(3000).Wait();
           if (choice.Equals("a")){
                return "blue";
           }
           else{
                return "green";
           }
        }
        [HttpGet("border/{choice}")]
        public string GetBorder(string choice)
        {
            Task.Delay(3000).Wait();
           if (choice.Equals("a")){
                return "thick dashed red";
           }
           else{
                return "thick dotted orange";
           }
        }
    }
}
