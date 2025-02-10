//Gemensam URL del
let api_url='http://127.0.0.1:5000/face'
let detection_server_url = 'http://172.17.0.2:8008'

function isDebugMode() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('debug') === 'true';
}

//Getting the the URL data
async function getFace(url){
    try{
        const respons=await fetch(url)
        return await respons.json()
    }catch(error){
        console.log(error)
    }
}

function toggleDebugButtons() {
    const buttons = document.querySelectorAll('button');
    const displayStyle = isDebugMode() ? 'inline-block' : 'none';
    buttons.forEach(button => {
        button.style.display = displayStyle;
    });
}
//HTML ids
let ids=["#inc-mouth","#right-eb","#left-eb","#eye-left","#eye-right"]

let tearval=false;

setInterval(processQueue, 1000); // Adjust the interval as needed

//Function that animates
function animFunction(val){
    console.log("animFunction called with val:", val);
    //Getting all the values from API
    let parts=[val.mouth,val.eb_right,val.eb_left,val.eye_left,val.eye_right]

    //Looping through all the animations and new values
    for(let i=0; i<ids.length; i++){
        let target = document.querySelector(ids[i]);
        console.log(`Animating ${ids[i]} with value:`, parts[i]);
        //animation
        anime({
            targets: target,
            d:[
                {value: parts[i]} 
            ],
            duration:750,
            easing:"easeInQuad",
        })
    }
}

let faceQueue = [];
let currentFace = null;

async function fetchAndAnimateFace(name) {
    let face = await getFace(api_url + "?name=" + name);
    faceQueue.push(face);
}

async function getNextFaceFromQueue() {
    try {
        const response = await fetch(api_url + "/queue/next");
        const data = await response.json();
        if (data.status !== 'empty') {
            faceQueue.push(data);
        }
    } catch (error) {
        console.log(error);
    }
}

function processQueue() {
    if (faceQueue.length > 0 && !currentFace) {
        currentFace = faceQueue.shift();
        animFunction(currentFace);
        setTimeout(() => {
            currentFace = null;
        }, 1000); // Adjust the duration as needed
    }
}

async function getEyeCoordinates() {
    try {
        const response = await fetch(detection_server_url + "/see", {
            mode: 'cors'  // Ensure CORS mode is enabled
        });
        const data = await response.json();
        console.log("Raw data from /see endpoint:", data);
        if (Array.isArray(data) && data.length > 0) {
            const spatialCoordinates = data[0].spatialCoordinates;
            console.log("Spatial coordinates:", spatialCoordinates);
            return { x_cord: spatialCoordinates.x, y_cord: spatialCoordinates.y };
        }
        return { x_cord: 0, y_cord: 0 };
    } catch (error) {
        console.log(error);
        return { x_cord: 0, y_cord: 0 };
    }
}

async function modifyEyePath(face) {
    console.log("modifyEyePath called with face:", face);

    const baseCoordinates = {
        'eye_left': { x: 121.33035, y: 159.60567 },
        'eye_right': { x: 203.91816, y: 159.79463 },
        'eb_left': { x: 85.422617, y: 126.15477 },
        'eb_right': { x: 169.90029, y: 126.15476 },
        'mouth': { x: 97.3423, y: 213.19999 }
    };

    const newCoordinates = await getEyeCoordinates();
    console.log("New Coordinates:", newCoordinates);

    // Define multipliers for eyes and other elements
    const eyeMultiplierX = -0.15;
    const eyeMultiplierY = -0.12;
    const faceMultiplierX = -0.1;
    const faceMultiplierY = -0.1;

    // Calculate offsets
    const eyeXOffset = parseFloat(newCoordinates.x_cord) * eyeMultiplierX;
    const eyeYOffset = parseFloat(newCoordinates.y_cord) * eyeMultiplierY;
    const faceXOffset = parseFloat(newCoordinates.x_cord) * faceMultiplierX;
    const faceYOffset = parseFloat(newCoordinates.y_cord) * faceMultiplierY;

    console.log("Offsets:", { eyeXOffset, eyeYOffset, faceXOffset, faceYOffset });

    const newFace = { ...face };

    // Modify each element
    for (const element in baseCoordinates) {
        const base = baseCoordinates[element];
        let modifiedString = face[element];
        if (element.startsWith('eye')) {
            // Apply larger offsets to eyes
            modifiedString = modifiedString.replace(
                base.x.toString(), (base.x + eyeXOffset).toString()
            ).replace(
                base.y.toString(), (base.y + eyeYOffset).toString()
            );
        } else {
            // Apply smaller offsets to other elements
            modifiedString = modifiedString.replace(
                base.x.toString(), (base.x + faceXOffset).toString()
            ).replace(
                base.y.toString(), (base.y + faceYOffset).toString()
            );
        }
        newFace[element] = modifiedString;
        console.log(`Modified ${element}:`, modifiedString);
    }
    
    return newFace;
}

async function updateEyes() {
    console.log("updateEyes called");
    if (currentFace) {
        const modifiedFace = await modifyEyePath(currentFace);
        console.log("calling animFunction with modifiedFace:", modifiedFace);
        animFunction(modifiedFace);
    }
}

setInterval(getNextFaceFromQueue, 1000); // Adjust the interval as needed
setInterval(processQueue, 1000); // Adjust the interval as needed
setInterval(updateEyes, 100); // Adjust the interval as needed

//Happy face
async function smile(){
   let smile = undefined
   smile= await getFace(api_url+"?name=smile")
   smile=smile
   
   
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

document.addEventListener('DOMContentLoaded', toggleDebugButtons);

//https://animejs.com/documentation/#playPause