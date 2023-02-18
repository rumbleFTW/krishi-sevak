// CHECK IF BROWSER SUPPORTS GEOLOCATION
setTimeout(send_loc, 8000);


function send_loc() {
    if('geolocation' in navigator){
        navigator.geolocation.getCurrentPosition(setPosition, showError);
    }else{
        console.log("Error")
        notificationElement.style.display = "block";
        notificationElement.innerHTML = "<p>Browser doesn't Support Geolocation</p>";
    }
}

// SET USER'S POSITION
function setPosition(position){
    let latitude = position.coords.latitude;
    let longitude = position.coords.longitude;
    const request = new XMLHttpRequest()
    request.open('POST', `/get_loc/${JSON.stringify({"latitude": latitude, "longitude": longitude, "area": document.getElementById('quantity').value})}`)
    request.send()
    console.log('Locs sent')
    // alert("Your Latitude: " + latitude + ", Longitude: " + longitude);
}

// SHOW ERROR WHEN THERE IS AN ISSUE WITH GEOLOCATION SERVICE
function showError(error){
    notificationElement.style.display = "block";
    notificationElement.innerHTML = `<p> ${error.message} </p>`;
}