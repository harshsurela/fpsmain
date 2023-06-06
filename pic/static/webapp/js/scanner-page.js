// window.onload = function () {
//     $('#admincode').val(localStorage.getItem('admincode'));
// }
// var admincode = localStorage.getItem("admincode");
// window.localStorage.clear();
// window.localStorage.setItem('admincode', admincode)
const webcamElement1 = document.getElementById('camera-left');
const webcamElement2 = document.getElementById('camera-right');
const canvasElement = document.getElementById('canvas');
const snapSoundElement = document.getElementById('snapSound');

// const canvasElement = document.getElementById('canvas');
// const snapSoundElement = document.getElementById('snapSound');
// ,{dest_width: 640},{dest_height: 360}
const webcam1 = new Webcam(webcamElement1, 'environment', canvasElement);
const webcam2 = new Webcam(webcamElement2, 'environment', canvasElement);


// webcam1.set({

//     image_format: 'jpeg',
//     jpeg_quality: 90
// });

webcam1.start()
    .then(result => {
        console.log("webcam started");

    })
    .catch(err => {
        console.log(err);
    });

// webcam2.start()
//     .then(result => {
//         console.log("webcam started");
//     })
//     .catch(err => {
//         console.log(err);
//     });

function flipCamera() {
    webcam1.flip();
    webcam1.start();
};

function reset(position, modal_id) {
    var snap_name = ['L1','L2','L3','L4','L5','R1','R2','R3','R4','R5']
    i = position
    document.getElementById("finger-name").innerHTML = fingers_name[i - 1];
    document.getElementById(modal_id).style.display = "none";
    document.getElementById("myimage" + i).src = "/static/image/white-background image.jpg";
    document.getElementById("snap-text-span" + i).innerHTML = snap_name[i-1];
    document.getElementById("snap-text-span" + i).style.margin = "14px -61px";
    document.getElementById("snap-text-span" + i).style.fontSize = "25px";


    //
    // if (i <= 5) {
    //     right_camera.style.display = "none";
    //     right_camera_border.style.display = "none";
    //     left_camera.style.display = "block";
    //     left_camera_border.style.display = "block";
    //     // document.getElementById("instructions-text").style.right = "0";
    //     // document.getElementById("instructions-text").style.left = "220px";
    //     document.getElementById("instructions-text").style.margin = "0 0 0 220px";

    // } else {
    //     left_camera.style.display = "none";
    //     left_camera_border.style.display = "none";
    //     right_camera.style.display = "block";
    //     right_camera_border.style.display = "block";
    //     document.getElementById("instructions-text").style.margin = "0 220px 0 20px";
    // }
}

// Saving Images and showing registration form
function displayForm() {
    document.getElementById("container").style.display = "none";
    document.getElementById("registration-form").style.display = "block";
    console.log("in next");
    // var status = checkInvalidation();
    // console.log(status);
    // if(status === "invalid"){
    //     alert("Please capture all fingers");
    //     return;
    // }else{
    //     document.getElementById("container").style.display = "none";
    //     document.getElementById("registration-form").style.display = "block";
    // }
    // var i = 1;
    // for (i; i < 11; i++) {
    //     var data_name = 'image' + i;
    //     localStorage.removeItem(data_name)
    //     localStorage.setItem(data_name, document.getElementById(data_name).value);
    // }
    // console.log(localStorage.getItem('image1'));
    // window.location.href = "{% url 'registration' %}";
}


function scannerPage() {
    document.getElementById("registration-form").style.display = "none";
    document.getElementById("container").style.display = "block";
}



function startTorch() {
    var imageCapture = new ImageCapture(videoTrack);
    var photoCapability = imageCapture.getPhotoCapabilities();
    var mediaCapabilities = navigator.mediaDevices.getSupportedConstraints()
    if (mediaCapabilities.torch && photoCapability.fillLightMode.length > 0) {
        console.log("Torch is enabled");
    }
    var torchCheckBox = document.getElementById("torch");
    if (torchCheckBox.checked === true) {
        videoTrack.applyConstraints({
            advanced: [{ torch: true }]
        }).then(function () {
            console.log("Torch is on")
        }).catch(handleError);
    }
    else {
        videoTrack.applyConstraints({
            advanced: [{ torch: false }]
        }).then(function () {
            //success code here
        }).catch(handleError);
    }
}

// Capture Image













// Configure a few settings and attach camera
//     Webcam.set({
//         // video:{facingmode:'user'},
//         width: 240,
//         height: 180,
//         image_format: 'jpeg',
//         jpeg_quality: 90,

//     });
//     // Webcam.flip();
//     // Webcam.start();

//     Webcam.attach('#camera-left');
//     Webcam.attach('#camera-right');


//     // Code to handle taking the snapshot and displaying it
    // var left_camera = document.getElementById("camera-left");
    // var right_camera = document.getElementById("camera-right");
    // var left_camera_border = document.getElementById("scanner-area-left");
    // var right_camera_border = document.getElementById("scanner-area-right");
    // var i = 1;
//     const fingers_list = ['Left Thumb - L1', 'Left Index Finger - L2', 'Left Middle Finger - L3', 'Left Ring Finger - L4', 'Left Little Finger - L5', 'Right Thumb - R1', 'Right Index Finger - R2', 'Right Middle Finger - R3', 'Right Ring Finger - R4', 'Right Little Finger - R5']
//     document.getElementById("finger-name").innerHTML = fingers_list[0];

//     function take_snapshot() {
//         document.getElementById("finger-name").innerHTML = fingers_list[i];
//         if (i <= 4) {
//             right_camera.style.display = "none";
//             right_camera_border.style.display = "none";
//             left_camera.style.display = "block";
//             left_camera_border.style.display = "block";

//         } else {
//             left_camera.style.display = "none";
//             left_camera_border.style.display = "none";
//             right_camera.style.display = "block";
//             right_camera_border.style.display = "block";
//         }

//         if (i > 10) {
//             var message = document.getElementById("message")
//             message.innerHTML = "You have already taken maximum images"
//         } else {
//             // take snapshot and get image data
//             Webcam.snap(function (data_uri) {
//                 // display results in page
//                 // console.log(data_uri)

//                 document.getElementById('finger' + i).innerHTML =
//                     '<img width="91px" height="60" src="' + data_uri + '"/>';
//                 // document.getElementById('image' + i).innerHTML = data_uri;
//                 console.log(i);
//                 $('#image' + i).val(data_uri);
//                 // console.log(document.getElementById('image'+ i).value);
//                 // const data =
//                 // console.log($("#image + i ").val());

//                 i = i + 1;
//             });
//         }
//     }


//     function flipCamera() {
//         Webcam.flip();
//         Webcam.facingmode = "environment";
//         // Webcam.start();
//         // Webcam.attach('#camera-left');
//         // Webcam.attach('#camera-right');
//     }


    // function displayForm() {
    //     var i = 1;
    //     for (i; i < 11; i++) {
    //         var data_name = 'image' + i;
    //         localStorage.setItem(data_name, document.getElementById(data_name).value);
    //     }
    //     // document.getElementById('image-data').style.display = "block";
    //     // document.getElementById('container').style.display = "none";
    //     // registration
    //     console.log(localStorage.getItem('image1'));
    //     window.location.href = "{% url 'registration' %}";
    // }

//     function backPage() {
//         document.getElementById('image-data').style.display = "none";
//         document.getElementById('container').style.display = "block";
//     }


    // function reset(position) {
    //     i = position
    //     document.getElementById("finger-name").innerHTML = fingers_list[i - 1];
    //     if (i <= 5) {
    //         right_camera.style.display = "none";
    //         right_camera_border.style.display = "none";
    //         left_camera.style.display = "block";
    //         left_camera_border.style.display = "block";

    //     } else {
    //         left_camera.style.display = "none";
    //         left_camera_border.style.display = "none";
    //         right_camera.style.display = "block";
    //         right_camera_border.style.display = "block";
    //     }
    // }
//     // var n;
//     // function reset(n) {
//     //     // take snapshot and get image data
//     //     Webcam.snap(function (data_uri) {
//     //         // display results in page
//     //         // console.log(data_uri)

//     //         document.getElementById('finger' + i).innerHTML =
//     //             '<img width="91px" height="60" src="' + data_uri + '"/>';

//     //     });
//     // }






