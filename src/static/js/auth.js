import { callAPI, showToast } from "./misc.js";
document.addEventListener('DOMContentLoaded', function() {

    if(document.getElementById('register_form') != null){
        document.getElementById('register_form').addEventListener('submit', function(event) {
            event.preventDefault();
            var formData = new FormData(this);
    
            callAPI('POST', '/api/auth/register', formData).then((data)=>{
                console.log(data)
                showToast('Registered successfully', 'success')
                window.location.href = '/'
            }).catch((e)=>{
                console.log(e)
                showToast(e, 'danger')
            })
            
        });
    }

    if(document.getElementById('login_form') != null){
        document.getElementById('login_form').addEventListener('submit', function(event) {
            event.preventDefault();
            var formData = new FormData(this);
    
            callAPI('POST', '/api/auth/signin', formData).then(()=>{
                showToast("Login success", 'success')
                window.location.href = 'index'
            }).catch((e)=>{
                showToast(e, 'danger')
            })
            
        });
    }
    
});