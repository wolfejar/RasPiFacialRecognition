const video = document.getElementById('video')

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

function loadDoc(embeddings) {
    var data = {
        embeddings: []
    };
    for(var i in embeddings) {
        var item = embeddings[i];
        data.embeddings.push(item)
    }
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("demo").innerHTML = this.responseText;
        }
    };
    xhttp.open("POST", "/classify_embeddings", true);
    console.log(JSON.stringify(data));
    xhttp.send(JSON.stringify(data));
}

Promise.all(
    [
        faceapi.nets.tinyFaceDetector.loadFromUri('./static/weights'),
        faceapi.nets.faceLandmark68Net.loadFromUri('./static/weights'),
        faceapi.nets.faceRecognitionNet.loadFromUri('./static/weights')
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
    let queue = new Queue();
    setInterval(async () => {
        detections = await faceapi.detectAllFaces(video, new faceapi.TinyFaceDetectorOptions()).withFaceLandmarks().withFaceDescriptors()
        if (!!detections[0] && detections[0]['detection']['score'] > 0.6) {
            //make ajax call (send the detections and current queue -> response contains friend name and confidence, if friend not in queue already)
            // queue.enqueue(detections[0]['descriptor'])
            loadDoc(detections[0]['descriptor'])
        }
        console.log(queue)
        const resizedDetections = faceapi.resizeResults(detections, displaySize)
        canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height)
        faceapi.draw.drawDetections(canvas, resizedDetections)
    }, 10000)
});