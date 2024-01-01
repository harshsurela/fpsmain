// console.log('hello world')
// const alertBox = document.getElementById('alert-box')
const imageBox = document.getElementById('image-box')
const imageForm = document.getElementById('image-form')
const confirmBtn = document.getElementById('confirmBtn')
var input = document.getElementById('mypic')
var fname= document.getElementById("finger-name").textContent;
var imagId = 0;
const csrf = document.getElementsByName('csrfmiddlewaretoken')

var $image = $('#rawimg').cropper({
    aspectRatio: 7 / 9,
    crop: function (event) {
        console.log('Cropping Details...');
        console.log(event.detail.x);
        console.log(event.detail.y);
        console.log(event.detail.width);
        console.log(event.detail.height);
        console.log(event.detail.rotate);
        console.log(event.detail.scaleX);
        console.log(event.detail.scaleY);
    }
});


input.addEventListener('change', ()=>{

    if ($image.data('cropper')) {
        $image.cropper('destroy');
    }

    // alertBox.innerHTML = ""
    confirmBtn.classList.remove('not-visible')
    const img_data = input.files[0]
    console.log("image_data")
    console.log(img_data)
    const url = URL.createObjectURL(img_data)
    imageBox.innerHTML = `<img src="${url}" class="img-thumbnail" id="rawimg"   >`
    $image = $('#rawimg')
    console.log($image)
    console.log("---------------")
    $image.cropper({
        aspectRatio: 7 / 9,
        crop: function(event) {
            console.log("cropping Deatils...");
            console.log(event.detail.x);
            console.log(event.detail.y);
            console.log(event.detail.width);
            console.log(event.detail.height);
            console.log(event.detail.rotate);
            console.log(event.detail.scaleX);
            console.log(event.detail.scaleY);
        }
    });
    confirmBtn.removeEventListener('click', confirmButtonClickHandler);
    confirmBtn.addEventListener('click', confirmButtonClickHandler);

})

function confirmButtonClickHandler() {
    console.log("Cropper image data")
    console.log($image.data('cropper'));
    $image.cropper('getCroppedCanvas').toBlob((blob) => {
        console.log('Confirmed');
        upload(blob);
    });
}


var idResponse = "";
function upload(file) {
    console.log ("=======> in Upload  "+  fname)
    var input = document.querySelector('input[type=file]');
    var fd = new FormData();
    console.log("============cccccccccc=======");
    // Check file selected or not

    fd.append('file',file,fname+".png");
    fd.append('iname',fname);
    // console.log("files")
    console.log("FD:")
    console.log(fd)
    fd.forEach(function(value, key){
        console.log(key+" "+value)
    });

    var load = document.getElementById("load");
    load.style.display = "block";
    $.ajax({
        url: '/cropimg/',
        type: 'post',
        data: fd,
        contentType: false,
        processData: false,
        success: function(response){
            load.style.display = "none";
           console.log(response.data)
           imagId = response.id;
            //well initialize a new image
            //on load of the image draw it on to canvas
            var canvas = document.getElementById('image-box2');
            var confirmbtn = document.getElementById('conformationBtn');
            confirmbtn.style.display='block';
            console.log("the line is executed");
           canvas.innerHTML = `<img src="/media/`+response.data+`" class="img-thumbnail" id="processedimg"   >`


        }
    });
}


function acceptResponse(){
    nextbtnfinal();
}
function retakeResponse(fno) {
    $.ajax({
        url: '/deleteImg/',
        type: 'post',
        data: { "idi": imagId },
        success: function (response) {
            console.log(response.data);
            imageBox.innerHTML = '';
            if ($image.data('cropper')) {
                $image.cropper('destroy');
            }
            // Reset the imagId
            imagId = 0;

            var canvas = document.getElementById('image-box2');
            var confirmbtn = document.getElementById('conformationBtn');
            confirmbtn.style.display = 'none';
            // Clear the displayed image
            canvas.innerHTML = '';
            // Reset the cropper
            $('#rawimg').cropper('destroy');

            document.querySelector('input[type="file"]').click();


        }
    });
}