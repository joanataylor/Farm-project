// alert("it works!")
const weather_div = document.querySelector("#weather_div")
console.log(weather_div)

weather_div1.innerHTML = ""
weather_div.innerHTML = ""

console.log(document.querySelector("#searchingbar").value)
function findweather(){
    var zipcode = document.querySelector("#searchingbar").value;
    console.log(zipcode)

    fetch("http://api.weatherapi.com/v1/forecast.json?key=5d2350d5e1224c78993185020222012&q="+zipcode)
      .then((response) => {
        return response.json()
      })
      .then((data) => {
        weather_info = data.current
        weather_information = data.location
        console.log(data)
        weather_div1.innerHTML = weather_information.name
        weather_div.innerHTML = weather_info.temp_c + "&#8451;"
        apiImg.src = weather_info.condition.icon
      })
      
    }



// fetch("http://api.openweathermap.org/data/2.5/weather?q=Galeana,PRT&appid=93fe7499a00821bf7fb59aedf16e2b41&units=metric")
//   .then((response) => {
//     return response.json()
//   })
//   .then((data) => {
//     weather_info = data.main
//     console.log(data)
//     weather_div.innerHTML += weather_info.temp + "&#8451;"
//   })

// fetch("http://api.openweathermap.org/data/2.5/weather?q=Galeana,PRT&appid=93fe7499a00821bf7fb59aedf16e2b41&units=metric")
//   .then((response) => {
//     return response.json()
//   })
//   .then((data) => {
//     weather_info = data.main
//     console.log(data)
//     weather_div1.innerHTML += weather_info.feels_like + "&#8451;"
//   })


// fetch("http://openweathermap.org/img/wn/01d.png")
// .then((response) => {
//   return response.json()
// })
// .then((data) => {
//   weather_info = data.weather
//   console.log(data)
//   weather_icon.innerHTML += weather_info[0].icon
// })

