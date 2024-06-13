//Gemensam URL del
let api_url='http://127.0.0.1:5000/face'

//Getting the the URL data
async function getFace(url){
    try{
        const respons=await fetch(url)
        console.log(respons)
        return await respons.json()
    }catch(error){
        console.log(error)
    }
}

//HTML ids
let ids=["#inc-mouth","#right-eb","#left-eb","#eye-left","#eye-right"]

let tearval=false;



/* function teananim(op, lo,col){
    anime({
        targets:"#tear",
        delay:600,
        opacity:op,
        translateY:35,
        duration: 600,
        backgroundColor:col,
        easing:'linear', //not tested with that just found it
        loop:lo
    }) 
} */



//Function that animates
function animFunction(val){

    //Getting all the values from API
    let parts=[val.mouth,val.eb_right,val.eb_left,val.eye_left,val.eye_right]
    
    //Looping through all the animations and new values
    for(let i=0; i<ids.length; i++){
     //animation
        anime({
            targets: ids[i],
            d:[
                {value: parts[i]} 
            ],
            duration:750,
            easing:"easeInQuad",
        })
        
    }

}




//Happy face
async function smile(){
   let smile= await getFace(api_url+"?name=smile")
   smile=smile[0]
   
   
   animFunction(smile)
}

//Sad face
async function sad(){
    let sad= await getFace(api_url+"?name=sad")
    sad=sad[0]
    
    animFunction(sad)
}

//Original face
async function neutral(){
    let neutral= await getFace(api_url+"?name=neutral")
    neutral=neutral[0]
    
    animFunction(neutral)
}

async function smileH(){
    let hearth = await getFace(api_url+"?name=hearth")
    hearth=hearth[0]
    animFunction(hearth)
}

async function winky(){
    let wink=await getFace(api_url+"?name=wink")
    wink=wink[0]
    animFunction(wink)
}

async function angry(){
    let angry=await getFace(api_url+"?name=angry")
    angry=angry[0]
    animFunction(angry)
}

async function smile3(){
    let smile3=await getFace(api_url+"?name=smile3")
    smile3=smile3[0]
    animFunction(smile3)
}

async function bigSmile(){
    let bigs=await getFace(api_url+"?name=bigsmile")
    bigs=bigs[0]
    animFunction(bigs)
}

async function suprised(){
    let sup=await getFace(api_url+"?name=suprise")
    sup=sup[0]
    animFunction(sup)
}

//Event listeners for the button
document.getElementById('but_happy').addEventListener("click", smile)
document.getElementById('but_sad').addEventListener("click", sad)
document.getElementById('but_neut').addEventListener("click", neutral)
document.getElementById('but_heart').addEventListener("click", smileH)
document.getElementById('but_wink').addEventListener("click", winky)
document.getElementById('but_ang').addEventListener("click",angry)
document.getElementById('but_3').addEventListener("click", smile3)
document.getElementById('but_big').addEventListener("click", bigSmile)
document.getElementById('but_sup').addEventListener("click", suprised)



//https://animejs.com/documentation/#playPause