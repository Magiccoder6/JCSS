if(document.getElementById('add-prof-form')!=null){
    document.getElementById('add-prof-form').addEventListener('submit', function(event) {
        event.preventDefault();
        var formData = new FormData(this);

        /*callAPI('POST', '/api/dashboard/add_appoinment', formData).then((data)=>{
            showToast(data.message, 'success')
        }).catch((e)=>{
            showToast(e, 'danger')
        })*/
    });
}