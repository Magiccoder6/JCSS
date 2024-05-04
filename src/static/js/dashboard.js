import { callAPI, showToast } from "./misc.js";
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('add_room_form').addEventListener('submit', function(event) {
        event.preventDefault();
        var formData = new FormData(this);
        console.log(formData)

        callAPI('POST', '/api/dashboard/add_room', formData).then((data)=>{
            
            showToast("Room was added successfully!!", 'success')
            setTimeout(()=>{
                document.location.reload()
            }, 2000)
        }).catch((e)=>{
            showToast(e, 'danger')
        })
    });

    if(document.getElementById('appointment_form')!=null){
        document.getElementById('appointment_form').addEventListener('submit', function(event) {
            event.preventDefault();
            var formData = new FormData(this);
            formData.append('date', `${localStorage.getItem('appointmentDate')} ${localStorage.getItem('appointmentTime')} GMT`)
    
            callAPI('POST', '/api/dashboard/add_appoinment', formData).then((data)=>{
                showToast(data.message, 'success')
            }).catch((e)=>{
                showToast(e, 'danger')
            })
        });
    }
});