import { callAPI, showToast, getRandomColor } from "./misc.js";

let schedule;

document.addEventListener('DOMContentLoaded', function() {
    schedule = new EventCalendar(document.getElementById('ec'), {
        view: 'timeGridWeek',
        events: [],
        slotDuration: '00:10',
        slotMinTime: '08:00',
        slotMaxTime: '16:00',
        eventDurationEditable: false,
        editable: false,
        eventStartEditable: false
    });

    loadSchedules(schedule)
})

function loadSchedules(schedule){
    callAPI("GET", "/api/dashboard/get_schedules").then((data)=>{
        let events = []
        for(var i=0;i<data.message.length;i++){
            let startDate = new Date(data.message[i].date.replace(new RegExp("GMT", "g"),""))
            let endDate = new Date(data.message[i].date.replace(new RegExp("GMT", "g"),""))
            endDate.setMinutes(endDate.getMinutes() + 20)

            events.push({
                id: i,
                start: startDate,
                end: endDate,
                title: {html: `<pre>${data.message[i].patient}</pre>`},
                backgroundColor: getRandomColor(),
                display: "auto"
            })
        }
        schedule.setOption("events",events)
    }).catch((err)=>{
        showToast(err, "danger")
    })
}
    