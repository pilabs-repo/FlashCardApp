function showpwd()
{
    var x = document.getElementById('pwd');
    if (x.type === "password")
    {
        x.type = 'text'
    }
    else
    {
        x.type = 'password'
    }
}
function showpwd2()
{
    var x = document.getElementById('pwd');
    var x2 = document.getElementById('pwd2');
    if (x.type === "password")
    {
        x.type = 'text'
        x2.type = 'text'
    }
    else
    {
        x.type = 'password'
        x2.type = 'password'
    }
}

function checkpwd()
{
    var pwd1 = document.signupform.password.value;
    var pwd2 = document.signupform.password2.value;
    if (pwd1 != pwd2)
    {
        alert('Passwords do not match');
        return false;
    }
}

function flipcard()
{
    var x = document.getElementById("cardbackview");
    // var y = document.getElementById("cardshow");
    // var z = document.getElementById("cardshowback");

    if (x.style.display === "none")
    // if(y.style.visibility === "hidden")
    {
        x.style.display = "block";
        // y.style.transform = "rotateY(0deg)";
        // z.style.transform = "rotateY(180deg)";
    }
    else
    {
        x.style.display = "none";
        // y.style.transform = "rotateY(180deg)";
        // z.style.transform = "rotateY(0deg)";
    }
    //rotateY(150deg);
}

