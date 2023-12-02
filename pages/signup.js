let signupConent = document.querySelector(".signup-form-container"),
        stagebtn1b = document.querySelector(".stagebtn1b"),
        stagebtn2a = document.querySelector(".stagebtn2a"),
        stagebtn2b = document.querySelector(".stagebtn2b"),
        stagebtn3a = document.querySelector(".stagebtn3a"),
        stagebtn3b = document.querySelector(".stagebtn3b"),
        signupContent1 = document.querySelector(".stage1-content"),
        signupContent2 = document.querySelector(".stage2-content"),
        signupContent3 = document.querySelector(".stage3-content");
        
        signupContent2.style.display = "none"
        signupContent3.style.display = "none"

        function stage1to2(){
            signupContent1.style.display = "none"
            signupContent3.style.display = "none"
            signupContent2.style.display = "block"
            document.querySelector(".stageno-1").innerText = "✔"
            document.querySelector(".stageno-1").style.backgroundColor = "rgb(128 202 135)"
            document.querySelector(".stageno-1").style.color = "#fff"
        }
        function stage2to1(){
            signupContent1.style.display = "block"
            signupContent3.style.display = "none"
            signupContent2.style.display = "none"
        }
        function stage2to3(){
            signupContent1.style.display = "none"
            signupContent3.style.display = "block"
            signupContent2.style.display = "none"
            document.querySelector(".stageno-2").innerText = "✔"
            document.querySelector(".stageno-2").style.backgroundColor = "rgb(128 202 135)"
            document.querySelector(".stageno-2").style.color = "#fff"
        }
        function stage3to2(){
            signupContent1.style.display = "none"
            signupContent3.style.display = "none"
            signupContent2.style.display = "block"
        }