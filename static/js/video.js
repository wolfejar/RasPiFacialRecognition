const video = document.getElementById('video');

// Queue class
class Queue {
    // Array is used to implement a Queue
    constructor() {
        this.items = [];
    }

    // Functions to be implemented
    enqueue(element) {
        // adding element to the queue
        this.items.push(element);
    }

    // dequeue function
    dequeue() {
        // removing element from the queue
        // returns underflow when called
        // on empty queue
        if (this.isEmpty())
            return "Underflow";
        return this.items.shift();
    }

    // front()
    // isEmpty function
    isEmpty() {
        // return true if the queue is empty.
        return this.items.length == 0;
    }

    // printQueue()
}

Promise.all(
    [
        faceapi.nets.tinyFaceDetector.loadFromUri('./static/weights')
    ]
).then(startVideo)

function startVideo() {
    navigator.getUserMedia(
        {video: {}},
        stream => video.srcObject = stream,
        error => console.error(error)
    )
}

video.addEventListener('play', () => {
    const canvas = faceapi.createCanvasFromMedia(document.getElementById('video'))
    canvas.setAttribute("style", "z-index:1; position:absolute")
    document.body.append(canvas)
    const displaySize = {width: video.width, height: video.height}
    faceapi.matchDimensions(canvas, displaySize)
    var options = new faceapi.TinyFaceDetectorOptions();
    setInterval(async() => {
        console.log("in async");
        console.log(Date.now());
        let detections = await faceapi.detectAllFaces(video, options);
        console.log(detections)
        for(var i in detections) {
            let sendimage = false;
            if (!!detections[i] && detections[i]['score'] > 0.4) {
                // console.log(detections);
                sendimage = true;
            }
            if(sendimage) {
                document.getElementById("timestamp").innerText = Date.now().toString();
                console.log("Sending image to server");
                test(video)
            }
        }
    }, 2000)// wait 2 seconds before giving new inputs to model
});