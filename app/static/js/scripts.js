var video = document.querySelector("#yo_face");

navigator.getUserMedia = navigator.getUserMedia ||
    navigator.webkitGetUserMedia ||
    navigator.mozGetUserMedia ||
    navigator.msGetUserMedia ||
    navigator.oGetUserMedia;

if (navigator.getUserMedia) {
    navigator.getUserMedia({video: true}, handleVideo, videoError);
}

function handleVideo(stream) {
    video.src = window.URL.createObjectURL(stream);
}

function videoError(e) {
    alert("Nope, not going to work");
}

$(function(){
    $("#typed").typed({
        stringsElement: $('#typed-strings'),
        startDelay: 1500,
        typeSpeed: 100
    });
});

function addName(name) {
    if (name.length == 0) {
        return;
    }
    
    $("#typed").append(name[0]);

    var timeoutID = window.setTimeout(addName, 100, name.substring(1, name.length));
}


var video = document.getElementById("yo_face");
var photo = document.getElementById("captured");
var canvas = document.getElementById("canvas");

var width = 720;
var height = 480;

function takepicture() {
    var context = canvas.getContext('2d');
    
    if (width && height) {
        canvas.width = width;
        canvas.height = height;
        context.drawImage(video, 0, 0, width, height);
        
        var data = canvas.toDataURL('image/jpeg');
        photo.setAttribute('src', data);
    } else {
        clearphoto();
    }
}


function clearphoto() {
    var context = canvas.getContext('2d');
    context.fillStyle = "#000";
    context.fillRect(0, 0, canvas.width, canvas.height);
    
    var data = canvas.toDataURL('image/jpeg');
    photo.setAttribute('src', data);
}

var currently_checking = true;

function modal_call() {
    $('#interactModal').modal({show: true, keyboard: false, backdrop: 'static'});
}

function post_success() {
    // MEH
}

function handle_get(data, testStatus, xhr) {
    if (currently_checking && xhr.status == 200){
        var proc_data = JSON.parse(data);
        
        addName(", " + proc_data['name']);

        $("#loc").html(proc_date['location']);
        
        currently_checking = false;
        
        window.setTimeout(modal_call, 2000);
    }
}

function cronjob() {
    if (currently_checking){
        takepicture();
        
        // var img_src = document.getElementById("captured");
        // var fd = new FormData();
        // fd.append( 'image', $("#captured").attr("src") );
        var poo = $("#captured").attr("src");
        
        $.ajax({
            type: "POST",
            url: "/push_face",
            enctype: "image/jpeg",
            contentType: false,
            processData: false,
            data: poo,
            success: post_success
        });

        $.get("/get_face", handle_get);
    }
    
    var t_id = window.setTimeout(cronjob, 500);
}

$(document).ready(function (){window.setTimeout(cronjob, 3500);});


function reset_all() {
    currently_checking = true;
    $("#typed")[0].innerHTML = "Hey there";
    $('#interactModal').modal('hide');
}

