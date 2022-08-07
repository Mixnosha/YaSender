    let obj = document.querySelector(".add_mail");
    let file = document.querySelector(".add_file");
obj.onclick = function()
{
    let obj = document.querySelector(".product_right");
    let upload = document.querySelector(".file_form");
    if (obj.style.display == 'none'){
        upload.style.display = "none";
        obj.style.display = "block";
    }
    else{
        obj.style.display = "none";
    }
}

    file.onclick = function()
     {
        let obj = document.querySelector(".file_form");
        let mail = document.querySelector(".product_right");
        if (obj.style.display == 'none'){
            mail.style.display = "none";
            obj.style.display = "block";
        }
        else{
            obj.style.display = "none";
        }
    }
