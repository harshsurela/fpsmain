// console.log('hello world')
// const alertBox = document.getElementById('alert-box')
const imageBox = document.getElementById('image-box')
const imageForm = document.getElementById('image-form')
const confirmBtn = document.getElementById('confirmBtn')
var input = document.getElementById('mypic')
var fname= document.getElementById("finger-name").textContent;
var imagId = 0;
const csrf = document.getElementsByName('csrfmiddlewaretoken')

input.addEventListener('change', ()=>{
    // alertBox.innerHTML = ""
    confirmBtn.classList.remove('not-visible')
    const img_data = input.files[0]
    const url = URL.createObjectURL(img_data)

    imageBox.innerHTML = `<img src="${url}" class="img-thumbnail" id="rawimg"   >`
    var $image = $('#rawimg')
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
    
    var cropper = $image.data('cropper');
    console.log("--------------->")
    confirmBtn.addEventListener('click', ()=>{
        cropper.getCroppedCanvas().toBlob((blob) => {
            console.log('confirmed')
            upload(blob)
        })
    });
})
var idResponse = "";
function upload(file) {
    console.log ("=======> in Upload  "+  fname)
    var input = document.querySelector('input[type=file]');
    var fd = new FormData();
    console.log("============cccccccccc=======");
    // Check file selected or not
    
    fd.append('file',file,fname+".png"),
    fd.append('iname',fname)
    // console.log("files")
    
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
            document.querySelector('input[type="file"]').click();
            var canvas = document.getElementById('image-box2');
            var confirmbtn = document.getElementById('conformationBtn');
            confirmbtn.style.display = 'none';
            // Clear the displayed image
            canvas.innerHTML = '';
            // Reset the cropper
            $('#rawimg').cropper('destroy');
            // Reset the imagId
            imagId = 0;
        }
    });
}