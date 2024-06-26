
export function toggleLoading() {
    var loadingDiv = document.getElementById('loading');
    loadingDiv.style.display = loadingDiv.style.display === 'none' ? 'block' : 'none';
}

export function showToast(message, type){
    var element = document.getElementById('toastr')
    if(type == "danger"){
        element.classList.remove(['bg-success'])
        element.classList.add(['bg-danger'])
    }else{
        element.classList.remove(['bg-danger'])
        element.classList.add(['bg-success'])
    }
    document.getElementById('message').innerHTML = message
    var myToast = new bootstrap.Toast('.toast')
    myToast.show()
}

export function callAPI(requestType, endpoint, formData){
    toggleLoading()
    return new Promise((resolve, reject) => {
        var xhr = new XMLHttpRequest();
        xhr.open(requestType, endpoint);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhr.onload = function() {
            toggleLoading()
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                resolve(response)
            } else {
                var error = JSON.parse(xhr.responseText);
                reject(error.message)
            }
        };
        xhr.send(new URLSearchParams(formData).toString());
    });
}

export const STATUS = ['PENDING','ADMIT','INPROGRESS','DISCHARGE']

export function getRandomColor() {
    // Generate random values for red, green, and blue components
    let red = Math.floor(Math.random() * 256); // Random integer between 0 and 255
    let green = Math.floor(Math.random() * 256);
    let blue = Math.floor(Math.random() * 256);

    // Construct the RGB color string
    let color = `rgb(${red}, ${green}, ${blue})`;

    return color;
}